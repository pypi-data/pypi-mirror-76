# twine-verify-upload

Adds an "verify-upload" command to (PyPA's
Twine)[https://github.com/pypa/twine/], that lets you check if the distribution
files have been uploaded already, and whether the hashes of the local files
match those from the repository.

## Installation

```
pip install twine-verify-upload
```

*Note: this package does not use `twine` as a requirement. As a result, you'll
need to install Twine yourself.*

## Usage example

```
> twine verify-upload dists/* --fail-when=different
Looking for dist/my-package-4.8.3.dev0-py2.py3-none-any.whl.
        Local:  5b5e5bf19f75487d60ea872d678b408c                   
        Remote: <NOT FOUND>                                        
Looking for dist/my-package-4.8.3-py2.py3-none-any.whl.     
        Local:  bca9059278b9f4b082bb97d6d7843782                   
        Remote: bca9059278b9f4b082bb97d6d7843782                   
Looking for dist/my-package-4.8.4-py2.py3-none-any.whl.     
        Local:  1a384341f51335bbb386fe59bf86516e                   
        Remote: e1f7c623bf98a862c02ea9ee6e53718a                   
Looking for dist/my-package-4.8.3.dev0.tar.gz.              
        Local:  ad954ed1fc0c0ab38634f6cdb2ec7a1a                   
        Remote: <NOT FOUND>                                        
Looking for dist/my-package-4.8.3.tar.gz.                   
        Local:  530bbc6bb9bdcd04472cfe3e813a0182                   
        Remote: 68851845bad137a2ab3a2442ae331822                   
Looking for dist/my-package-4.8.4.tar.gz.                   
        Local:  0a19fcda21530c31964474ea4b33e327                   
        Remote: e982b6f6f9df5eab32158437485613d5                   
```
