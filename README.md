# AutoClicker
A program to click faster in games.
Currently only supports Windows. (But I hope I will add Linux support at a convenient time (definitely not soon))
If you want to add linux support, you can add it by forking repo or committing your code it to this repository. (I will check and (I hope) accept commit)

## Installation
To install requirements (For Windows):
```bash
python -m pip install pyWinHook
```
To install run:
```bash
python app.py --install
```
Or run once with:
```bash
python app.py
```
And if you want to add to startup programs
```bash
python app.py --addstartup
```

For more detailed info use
```bash
python app.py -h
```

## Known Issues
- While program running (not only started, if exe or py file running), alt-gr combinations doesn't work properly on Windows.