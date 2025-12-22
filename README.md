# Key Show

A simple Tkinter visualization of a keyboard with adaptive key heights and an optional headerless window.

## Run

```powershell
& .\.venv\Scripts\Activate.ps1
python .\main.py
```

## Headerless Window

- Disable the Windows title bar by default using a borderless window.
- Drag the window by holding the left mouse button anywhere.
- Press Escape to quit.
- To restore the title bar, set `hide_titlebar=False` when creating `HighPerfKeyboard` in [main.py](main.py).

## Notes

- Requires the `keyboard` package (declared in [pyproject.toml](pyproject.toml)).
