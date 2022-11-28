# Selenium Browser Controller for apt Firefox on Ubuntu 22.10

[!\[Python 3.10\]\[python_badge\]](https://www.python.org/downloads/release/python-3106/)
[!\[License: AGPL v3\]\[agpl3_badge\]](https://www.gnu.org/licenses/agpl-3.0)
[!\[Code Style: Black\]\[black_badge\]](https://github.com/ambv/black)
[!\[Code Coverage\]\[codecov_badge\]](https://codecov.io/gh/a-t-0/snnalgos)

Initialises a Selenium browser controller for a specific firefox profile on an
Ubuntu 22.10 system for an `apt` installation of Firefox.

Put into a separate pip package to remove boiler-plate code from other
repositories that control the browser.

## Usage

First install this pip package with:

```
pip install browsercontroller
```

Then run:

```py
from browsercontroller.Browsercontroller import Browsercontroller
Browsercontroller(url="startpage.nl",default_profile=True)
```

**Warning:**
Checks whether a `snap` version of Firefox is installed, and if yes, removes it
and installs an `apt` version of Firefox instead. You'll lose browser history,
logins and bookmarks if you don't have an `apt` version of Firefox.

## Updating

Build the pip package with:

```
python3 setup.py sdist bdist_wheel
```

Install the pip package locally with:

```
pip install -e .
```

Upload the pip package to the world with:

```
python -m twine upload dist/\*
```
