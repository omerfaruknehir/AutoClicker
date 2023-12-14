# AutoClicker
A program to click faster in games.
Currently only supports Windows. (But I will add Linux support soon)

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