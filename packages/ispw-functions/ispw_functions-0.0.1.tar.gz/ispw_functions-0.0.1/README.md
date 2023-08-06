# ISPW Functions

### Package and upload to pip

```sh
rm -rf build/ dist/ ispw_functions.egg-info/
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
