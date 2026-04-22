# automated-chromatography
Development of the automated chromatography rack.  Diagnostics Accelerator / Synthetic Biology. Wyss Institute.

- Dima Ter-Ovanesyan - dmitry.ter-ovanesyan@wyss.harvard.edu
- David Kalish - david.kalish@wyss.harvard.edu
- Allen Tat - allen.tat@wyss.harvard.edu
- Adele Nikitina - adele.nikitina@wyss.harvard.edu

## Folders

- To run Octasome system, navigate to `./SEC_GUI/` folder.  Run `python octasome_gui.py`. To autorun GUI from boot, see below.
- To run 24-well wash system, navigate to `./Wash_GUI/` folder.  Run `python wash_gui.py`. To autorun GUI from boot, see below.
- The folder `./dev/` is for development and testing.

## Auto-run at RaspPi boot
To auto-run the GUI and disable the screensaver, edit the file `/etc/xdg/lxsession/LXDE-pi/autostart`

For Octasome, add these lines to the end:

```sh
@python3 path/to/automated-chromatography/SEC_GUI/octasome_gui.py
@xscreensaver -no-splash
```

For Wash system, add these lines to the end:

```sh
@python3 path/to/automated-chromatography/Wash_GUI/wash_gui.py
@xscreensaver -no-splash
```

(replace `path/to` with the actual path)

