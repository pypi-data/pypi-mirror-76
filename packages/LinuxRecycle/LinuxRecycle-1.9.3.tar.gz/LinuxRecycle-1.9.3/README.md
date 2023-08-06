# LinuxRecycle
A recycle system for linux
## How to install?
```bash
python setup.py install [--user]
```
or
```bash
pip install LinuxRecycle [--user]
```

## options
* -f remove the file or dictory forcely

## setup your crontab
```
14 4 * * * python /pathto/auto_clear.py
```
```sh
git clone git@github.com:xxmawhu/LinuxRecycle.git
cd LinuxRecycle/core
python3 setCrontab.py
```
