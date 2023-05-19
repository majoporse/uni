# Setup instructions

## Working on a B117 or your Windows machine

1. Open PowerShell (press Windows key and type `powershell`).
1. Change into the directory, where you have cloned this seminar repository.
1. Execute the startup script:
```
.\StartNotebook_Windows.ps1
```

This should open the Jupyter Notebook on the B117 machines. It can fail
on your *own* machines for various reasons, in that case you need to go
through the setup on the following lines *manually*.

## Working on your Linux or MacOS machines

1. Open a terminal window:
    - On Linux usually Ctrl + Alt + t
    - On MacOS search for /Applications/Utilities/Terminal
1. Change into the directory, where you have cloned this seminar repository.
1. Execute the startup script:
```
./StartNotebook_Linux_or_MacOS.sh
```

This can fail for various reasons, in that case you need to go
through the setup on the following lines *manually*.

## Working on your own machine (manual steps)
You need to set up everything manually.

### Set up a virtual environment
On Linux (Bash) or MacOS (Zsh), for non-Bash shell you need
to source the `activate` script with the appropriate extension,
e.g. `source env/bin/activate.zsh`:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

On Windows (PowerShell):
```
py -m venv env
.\env\Scripts\activate.ps1
pip install -r requirements.txt
```

### Install jupyter extensions
```shell
jupyter contrib nbextension install --sys-prefix
jupyter nbextension enable contrib_nbextensions_help_item/main
jupyter nbextension enable hide_input/main
jupyter nbextension enable exercise/main
jupyter nbextension enable exercise2/main
jupyter nbextension enable collapsible_headings/main
jupyter nbextension enable init_cell/main
```

### Open the notebook
To open the Jupyter notebook, run:
```
jupyter notebook
```

### Deactivate virtual environment
After the seminar, deactivate the virtual environment:
```
deactivate
```
