# Installation

To install `pv080_crypto` to make it importable in your Python project run
inside your Python virtual environment:
```bash
$ pip install git+https://gitlab.fi.muni.cz/pv080/pv080_crypto.git
```

This command tells Pip to install a package from a Git repository at the
specific URL over HTTPS. You will need to provide your login credentials
for faculty Gitlab. In case you have SSH keys setup for the faculty Gitlab
you can use:
```bash
$ pip install git+ssh://git@gitlab.fi.muni.cz/pv080/pv080_crypto.git
```

# Development

This is a standard Python project.

## Setup

Prepare Python virtual environment, e.g. by running:
```bash
$ python -m venv venv
```
Activate the virtual environment by sourcing the appropriate shell-dependant
variant:
```bash
$ source venv/bin/activate # alter the extension {.fish, .zsh}
```

Finally, install the appropriate requirements (including the dependencies for
testing and docs):
```bash
(venv) $ pip install .[tests,docs]
```

## Testing

To execute the docstring tests run in project root:
```bash
$ pytest --xdoctest
```

## Documentation

```bash
$ cd docs
$ make html
```
And open the file `docs/html/index.html` in your favorite browser. In case there
are any issues you can try running `make clean` and create the documentation
from scratch.

```bash

```

```bash

```

```bash

```
