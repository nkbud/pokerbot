# Window detector
> I haven't found a cross-platform solution for this. Windows-only.

> I haven't found a Python-only solution for this. I'm relying on a tool called "AutoHotkey".

## Download + Install AutoHotkey 

> Download from: https://www.autohotkey.com/.
> If you save it C:\Program Files\AutoHotkey, it saves you a step later.
 
![img.png](_ahk.png)

## Run WindowSpy

> `py spy.py`

Or, if you installed AutoHotkey elsewhere:

> `py spy.py --ahk_path "C:\Program Files\AutoHotkey"`

## Run a Pokerstars game window

> Observe a table

## Look at its WindowSpy properties

Here's mine:
```
ahk_class GLFW30
ahk_exe PokerStars.exe
```
![spy.png](_spy.png)


## Test whether you can find your window

> `py window.py`

Or if you found different window properties, you can one or both of them

> `py window.py --ahk_exe "PokerStars.exe" --ahk_class "GLFW30"`





