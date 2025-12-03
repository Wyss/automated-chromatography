# automated-chromatography
Development of the automated chromatography rack.  Diagnostics Accelerator / Synthetic Biology. Wyss Institute.

## Requirements
- Python 3.8 - 3.10
  - (Not 3.7-, PyQt5 incompatible)
  - (not 3.11+, PySide2 incompatible)
- Qt 5.15
- `pip install -r requirements.txt`

## Contributors
#### Current
- Dima Ter-Ovanesyan - dmitry.ter-ovanesyan@wyss.harvard.edu
- David Kalish - david.kalish@wyss.harvard.edu
#### Former
- Allen Tat - allen.tat@wyss.harvard.edu
- Adele Nikitina - adele.nikitina@wyss.harvard.edu

## Folders
- The folder `./dev/` is for development and testing.  
- For 8-column SEC (Octasome), go to `./SEC_GUI/` and run `python octasome_gui.py`. To autorun GUI from boot, see below.
- For 24-well plate washing, go to `./Wash_GUI/` and run `python wash_gui.py`.

## Auto-run at RaspPi boot
To auto-run the GUI and disable the screensaver, edit the file `/etc/xdg/lxsession/LXDE-pi/autostart`

And add these lines to the end: 

```sh
@python3 /home/pi/Desktop/SEC_GUI/octasome_gui.py
@xscreensaver -no-splash
```

(or whatever the path to the file is on the first line)
