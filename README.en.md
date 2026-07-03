# AIassistant Auto

**Language / 璇█:** **[English](README.en.md)** | [绠€浣撲腑鏂嘳(README.zh-CN.md)

Automates Cursor account rotation inside **AIassistant** on Windows.

## What it does

| Step | Action |
|------|--------|
| 1 | Click **Cursor** in the sidebar (skip if already on Cursor page) |
| 2 | Click **Get account and log in** (waits through cooldown) |
| 3 | Click **Yes** on the confirmation dialog |
| 4 | Wait **60 seconds** (account switch in progress) |
| 5 | Bring AIassistant **to front** (Cursor may steal focus) |
| 6 | Click **OK** on the success dialog |
| 7 | **Minimize** AIassistant |

## Requirements

- Windows 10/11
- Python 3.10+
- AIassistant running (window title: `AI鍔╂墜`, `AIassistant`, or `AI Assistant`)

## Install

```powershell
git clone https://github.com/leehu546-cyber/aiassistant-auto.git
cd aiassistant-auto
pip install -r requirements.txt
```

## Usage

### Full run

```powershell
python aiassistant_auto.py
```

Takes about **1鈥? minutes** (includes 60s wait after Yes).

### Partial runs

```powershell
python aiassistant_auto.py --yes    # Click Yes only
python aiassistant_auto.py --ok     # Click OK and minimize
python aiassistant_auto.py --scan   # List buttons (debug)
```

## Configuration

Edit the top of `aiassistant_auto.py`:

```python
OK_DELAY_AFTER_YES = 60   # Seconds to wait after Yes
OK_POLL_TIMEOUT = 120     # Max seconds to wait for OK dialog
```

## Technical notes

- Uses **pywinauto UIA** `invoke()` for Qt buttons
- Does **not move the mouse**; safe to use while working
- PostMessage / OCR clicks do not work reliably on this Qt app

## References

- [pywinauto/pywinauto](https://github.com/pywinauto/pywinauto)
- [Qt button click Issue #1252](https://github.com/pywinauto/pywinauto/issues/1252)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Window not found | Open AIassistant first |
| Yes/OK not found | Cursor may cover the dialog; try `--ok` |
| Cooldown timer | Script waits up to 90s for 芦Xs remaining禄 |
| Cursor steals focus | Script raises AIassistant before clicking OK |


## Changelog

### 2026-07-03 — Robustness improvements

- **Fixed window selection picking the console window**: The shortcut-launched console window (title containing "换号") is no longer mistaken for the real AIAssistant window.
- **Content-based validation**: After filtering by size, the script now verifies the candidate window has sidebar buttons (Cursor / Home / etc.) before selecting it.
- **Auto-recenter off-screen windows**: If the AIAssistant window is dragged off-screen, the script will move it back to the center of the primary monitor.
- **Increased UIA tree rebuild delay**: After restoring from minimized state, wait time increased from 0.5s to 1.5s.
- **Fixed --scan mode Unicode crash**: safe_repr now falls back gracefully when stdout encoding (GBK) can't handle certain characters.
## License

MIT

