# FunkyChatClient
A funky little chat client made in python

---

## Running from pre-built releases
> Note: Due to a screen access bug, OSX builds are non-functional. To use on OSX, see **Running from source**.
1. Go to [the releases page](https://github.com/koerismo/FunkyChat/releases/latest)
2. Download the latest release
3. Run the executable

## Running from source
1. Clone this repository
2. Run `pip3 install -r src/requirements.txt` *(Optionally inside of a venv.)*
3. Run `python3 src/main.py` to start the program after the modules have finished installing.

## Building from source
1. Complete steps 1 and 2 of **Running from source**
2. Run `pip3 install pyinstaller` to install `PyInstaller`
3. Run `PyInstaller -n FunkyChat --onefile src/main.py` to build
