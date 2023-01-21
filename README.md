# automated-chromatography
Development of the automated chromatography rack.  Diagnostics Accelerator / Synthetic Biology. Wyss Institute.

- Dima Ter-Ovanesyan - dmitry.ter-ovanesyan@wyss.harvard.edu
- David Kalish - david.kalish@wyss.harvard.edu
- Allen Tat - allen.tat@wyss.harvard.edu
- Adele Nikitina - adele.nikitina@wyss.harvard.edu

## Folders

The folder `./dev/` is for development and testing.  
The folder `./SEC_GUI/` is what must be on the Raspberry Pi.  Run `python Octasome_GUI.py`. To autorun GUI from boot, see below.

## Auto-run at RaspPi boot
To auto-run the GUI and disable the screensaver, edit the file `/etc/xdg/lxsession/LXDE-pi/autostart`

And add these lines to the end: 

```sh
@python3 /home/pi/Desktop/SEC_GUI/Octasome_GUI.py
@xscreensaver -no-splash
```

(or whatever the path to the file is on the first line)
