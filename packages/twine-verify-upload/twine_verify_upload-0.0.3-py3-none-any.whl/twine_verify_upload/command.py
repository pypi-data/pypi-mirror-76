import os
import sys
import hashlib
import argparse
from typing import List, Tuple, Callable, Any, cast, Union
from twine.utils import (EnvironmentDefault,
                         normalize_repository_url,
                         get_repository_from_config)
from twine.commands import _find_dists as find_dists
from twine.package import PackageFile
from pypi_simple import PyPISimple, parse_filename
from packaging.version import parse as parse_version
from colorama import Fore, Style


def print_header(api_endpoint: str) -> None:
    print(f"Using API endpoint at {api_endpoint}.\n")


# TODO: Refactor so that this displays package name instead
def print_dist(dist_path: str) -> None:
    print(f"Looking for {dist_path}.")


# TODO: Also print remote URL for convenience
# TODO: Also print hash types
def print_result(local_hash: str, remote_hash: str, has_failed: Any) -> None:
    color = (Fore.RED if has_failed
             else Fore.YELLOW if (
                 remote_hash != local_hash and remote_hash is not None
             )
             else Fore.GREEN)
    if remote_hash is None:
        remote_hash = "<NOT FOUND>"
    print(color, end='')
    print(f"\tLocal:\t{local_hash}")
    print(f"\tRemote:\t{remote_hash}")
    print(Style.RESET_ALL, end='')


failure_conditions = {
    "absent": lambda local, remote: remote is None,
    "exists": lambda local, remote: remote is not None,
    "different": lambda local, remote: remote is not None and local != remote,
    "miss": lambda local, remote: remote is None or local != remote,
}
default_failure_condition = "miss"
assert default_failure_condition in failure_conditions


class UnsupportedAPIError(Exception):
    """Raised, if the repository's Simple API returns an unsupported hash
    doesn't support hashes"""


def versions_equal(ver_a: str, ver_b: str):
    return parse_version(ver_a) == parse_version(ver_b)


def hash_file(path: str, hashlib_cls: Callable):
    BUF_SIZE = 2**16
    hasher = hashlib_cls()

    with open(path, 'rb') as f:
        while True:
            chunk = f.read(BUF_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


# TODO: ensure PyPIClient raises on 404 errors
def get_hashes(dist_path: str, simple_url: str) -> Tuple[str, Union[str, None]]:
    """Get local and remote hashes for a distribution

    Returns a pair (local_hash, remote_hash).

    The algorithm for the hashes returned is based on the information provided
    by remote's Simple API. Based on PEP 503, the API can return any type of a
    hash, as long as it is supported by the builtin hashlib module.

    If the Simple API doesn't return any hash, raises UnsupportedAPIError.

    If the package couldn't be found, an md5 has of local package is returned
    along with a None, i.e. ('<md5>', None).
    """
    client = PyPISimple(simple_url)
    package = PackageFile.from_filename(dist_path, comment=None)
    name = package.safe_name

    filename = os.path.basename(dist_path)
    _, local_version, local_package_type = parse_filename(filename,
                                                          project_hint=name)

    remote_dists = client.get_project_files(name)

    for remote_dist in remote_dists:
        if (versions_equal(local_version, remote_dist.version)
                and remote_dist.package_type == local_package_type):
            break
    else:
        return hash_file(dist_path, hashlib.md5), None
    try:
        algo, remote_hash = url_hash_fragment(remote_dist.url)
    except Exception as exc:
        raise UnsupportedAPIError("API doesn't support hashes.") from exc

    if algo not in hashlib.algorithms_guaranteed:
        raise UnsupportedAPIError(f"API returned an unsupported hash: {algo}.")

    hashlib_cls = getattr(hashlib, algo)
    local_hash = hash_file(dist_path, hashlib_cls)

    return local_hash, remote_hash


def get_simple_url(repository_url: str) -> str:
    """Given repository uploads URL, return the URL of Simple API endpoint"""
    if repository_url.endswith('://upload.pypi.org/legacy/'):
        repository_url = 'https://pypi.org'
    return repository_url.rstrip('/') + '/simple'


# TODO: hash-compatible APIs should not be required for 'missing' / 'exists' opt
# TODO: implement --quiet
def exists(dists: List[str],
           repository_url: str,
           failure_checker: Callable[[str, str], Any],
           *,
           quiet: Any) -> None:
    # TODO: this should check whether any dists were found
    dists = [fn for fn in find_dists(dists) if not fn.endswith(".asc")]
    assert dists
    simple_url = get_simple_url(repository_url)

    print_header(simple_url)
    failed = False
    for dist in dists:
        print_dist(dist)
        local_hash, remote_hash = get_hashes(dist, simple_url)
        bad_dist = failure_checker(local_hash, remote_hash)
        print_result(local_hash, remote_hash, has_failed=bad_dist)
        failed |= bad_dist
    return failed


def url_hash_fragment(distribution_url: str) -> Tuple[str, str]:
    """Given a distribution URL, return (hashname, hashvalue) tuple.

    If hash fragment is not present, return ('', '')."""
    algo_type, hash_value = distribution_url.split('#')[1].split('=')
    return algo_type, hash_value


def main(args: List[str]) -> None:
    # TODO: repository auth
    parser = argparse.ArgumentParser(
        prog="twine exists",
        description="Check existence of distribution on the remote, compare "
        "and validate hashes."
    )
    parser.add_argument(
        "dists",
        nargs="+",
        metavar="dist",
        help="The distribution files to check, usually dist/*",
    )
    parser.add_argument(
        "-r",
        "--repository",
        action=EnvironmentDefault,
        env="TWINE_REPOSITORY",
        default="pypi",
        help="The repository (package index) to check the package against. "
        "Should be a section in the config file (default: "
        "%(default)s). (Can also be set via %(env)s environment "
        "variable.)",
    )
    parser.add_argument(
        "--repository-url",
        action=EnvironmentDefault,
        env="TWINE_REPOSITORY_URL",
        default=None,
        required=False,
        help="The repository (package index) URL to check the package against. "
        "This overrides --repository. "
        "(Can also be set via %(env)s environment variable.)",
    )
    parser.add_argument(
        "--config-file",
        default="~/.pypirc",
        help="The .pypirc config file to use.",
    )
    # TODO: reword below
    # TODO: formatting of the list below
    # TODO: mention the fact, that for exists and missing the API doesn't have
    # to return hashes.
    parser.add_argument(
        "--fail-when",
        choices=failure_conditions.keys(),
        default=default_failure_condition,
        required=False,
        action="store",
        help="Set the condition by which exit status different than 0 is "
        "returned. Possible choices are: "
        "missing - when a package is absent, "
        "exists - when a package is present, "
        "different - when cheksums doesn't match, "
        "miss (default) - when hashes doesn't match or the package is absent."
    )
    parser.add_argument(
        "-q",
        "--quiet",
        default=False,
        required=False,
        action="store_true",
        help="Do not write anything to standard output."
    )

    parsed_args = parser.parse_args(args)

    repository_url = get_repository_from_config(
        parsed_args.config_file,
        parsed_args.repository,
        parsed_args.repository_url
    )["repository"]
    repository_url = cast(str, repository_url)
    repository_url = normalize_repository_url(repository_url)

    condition = failure_conditions[parsed_args.fail_when]

    if parsed_args.quiet:
        sys.stdout = open(os.devnull, 'a')
        sys.stderr = open(os.devnull, 'a')

    return exists(parsed_args.dists, repository_url, failure_checker=condition,
                  quiet=parsed_args.quiet)
