# fermi

A program to make fermi problems eaiser and more vivid

### How to run

Make sure you have the Canopy virtualenv sourced (otherwise GUI toolkits won't be found). I.e. install Canopy, and then to be sure you are in that venv:
```
source /Users/<home>/Library/Enthought/Canopy_64bit/User/bin/activate
```

Once cloned, just run `python fermi_script.py` from top directory

for a specific view:

	`export ETS_TOOLKIT=qt4`

	from the top directory (top `fermi/`) run the following in ipython

			`run -m fermi.view.database_view`