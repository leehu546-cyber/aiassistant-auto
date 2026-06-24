# AIassistant Auto · Cursor 换号自动化

**Language / 语言:** **[English](README.en.md)** | **[简体中文](README.zh-CN.md)**

---

Windows desktop automation for **AIassistant** (AI助手): one-click Cursor account rotation.

| | |
|---|---|
| **Stack** | [pywinauto](https://github.com/pywinauto/pywinauto) (UIA) + pywin32 |
| **Platform** | Windows 10/11 |
| **Python** | 3.10+ |

## Quick start

```powershell
pip install -r requirements.txt
python aiassistant_auto.py
```

## Commands

| Command | Description |
|---------|-------------|
| `python aiassistant_auto.py` | Full flow (~1–2 min) |
| `python aiassistant_auto.py --yes` | Click **Yes** only |
| `python aiassistant_auto.py --ok` | Click **OK** and minimize |
| `python aiassistant_auto.py --scan` | List UI buttons (debug) |

---

📖 **Full documentation:** [English](README.en.md) · [简体中文](README.zh-CN.md)
