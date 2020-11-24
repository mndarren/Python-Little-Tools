# Python-Little-Tools
Collecting all useful tools for Python
## How to reduce memory
```
1. range() return generator
2. d.items() return generator
3. __slot__ = []
4. create generator
```
## How to check memory size
```
sys.getsizeof(var)
```
## Commands for Developers
```
test:
    python -m pytest --cov . tests/
    python -m coverage html
    # python3 for mac since both python2 and 3 exist in mac

install:
    pip install -r requirements.txt --upgrade
    pip install -e .
    # for mac
    pip3 install xxx

venv:
    # for Windows
    virtualenv --python python3.8 venv
    venv\Scripts\activate
    venv\Scripts\deactivate.bat
    # for mac
    source venv/bin/activate
```