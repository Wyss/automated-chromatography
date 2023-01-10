# automated-chromatography
Development of the automated chromatography rack.  Diagnostics Accelerator / Synthetic Biology.

- David Kalish - david.kalish@wyss.harvard.edu
- Allen Tat - allen.tat@wyss.harvard.edu
- Adele Nikitina - adele.nikitina@wyss.harvard.edu

## Auto-run at RaspPi boot
To auto-run the GUI and disable the screensaver, edit the file `/etc/xdg/lxsession/LXDE-pi/autostart`

And add these lines to the end: 

```sh
@python3 /home/pi/Desktop/SEC_GUI/test4.py
@xscreensaver -no-splash
```

(or whatever the path to the file is on the first line)

