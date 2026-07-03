# AIassistant 鑷姩鎹㈠彿

**Language / 璇█:** [English](README.en.md) | **[绠€浣撲腑鏂嘳(README.zh-CN.md)**

Windows 妗岄潰鑷姩鍖栬剼鏈細鍦?**AIassistant锛圓I鍔╂墜锛?* 涓嚜鍔ㄥ畬鎴?Cursor 鎹㈠彿銆?
## 鍔熻兘

| 姝ラ | 鎿嶄綔 |
|------|------|
| 1 | 鐐瑰嚮宸︿晶 **Cursor** 鑿滃崟锛堝凡鍦?Cursor 椤靛垯璺宠繃锛?|
| 2 | 鐐瑰嚮 **鑾峰彇璐﹀彿骞剁櫥褰?*锛堝喎鍗翠腑鑷姩绛夊緟锛?|
| 3 | 鐐瑰嚮 **Yes** 纭鎹㈠彿 |
| 4 | 绛夊緟 **60 绉?*锛堟崲鍙疯繘琛屼腑锛?|
| 5 | 灏?AIassistant **缃《**锛堥伩鍏嶈 Cursor 鎸′綇锛?|
| 6 | 鐐瑰嚮 **OK** 纭鎴愬姛 |
| 7 | **鏈€灏忓寲** AIassistant |

## 鐜瑕佹眰

- Windows 10/11
- Python 3.10+
- AIassistant 宸插畨瑁咃紙绐楀彛鏍囬锛歚AI鍔╂墜` / `AIassistant` / `AI Assistant`锛?
## 瀹夎

```powershell
git clone https://github.com/leehu546-cyber/aiassistant-auto.git
cd aiassistant-auto
pip install -r requirements.txt
```

## 鐢ㄦ硶

### 瀹屾暣娴佺▼

```powershell
python aiassistant_auto.py
```

棰勮 **1~2 鍒嗛挓**锛堝惈 60 绉掓崲鍙风瓑寰咃級銆?
### 鍒嗘杩愯

```powershell
python aiassistant_auto.py --yes    # 浠呯偣鍑?Yes
python aiassistant_auto.py --ok     # 浠呯偣鍑?OK 骞舵渶灏忓寲
python aiassistant_auto.py --scan   # 鍒楀嚭鎵€鏈夋寜閽紙璋冭瘯锛?```

## 閰嶇疆

缂栬緫 `aiassistant_auto.py` 椤堕儴锛?
```python
OK_DELAY_AFTER_YES = 60   # Yes 鍚庣瓑寰呮崲鍙峰畬鎴愮殑绉掓暟
OK_POLL_TIMEOUT = 120     # 绛夊緟 OK 寮圭獥鐨勬渶闀跨鏁?```

## 鎶€鏈鏄?
- 浣跨敤 **pywinauto UIA** 鐨?`invoke()` 鐐瑰嚮 Qt 鎺т欢
- **涓嶇Щ鍔ㄩ紶鏍?*锛屽彲杈圭敤鐢佃剳杈硅繍琛?- PostMessage / OCR 瀵规 Qt 搴旂敤鏃犳晥

## 鍙傝€冮」鐩?
- [pywinauto/pywinauto](https://github.com/pywinauto/pywinauto)
- [Qt 鎸夐挳鐐瑰嚮 Issue #1252](https://github.com/pywinauto/pywinauto/issues/1252)

## 甯歌闂

| 鐜拌薄 | 澶勭悊 |
|------|------|
| 鏈壘鍒扮獥鍙?| 鍏堟墦寮€ AIassistant |
| Yes/OK 鎵句笉鍒?| Cursor 鍙兘鎸′綇绐楀彛锛涚敤 `--ok` 鍗曠嫭澶勭悊 |
| 鎸夐挳鍐峰嵈 | 鏄剧ず銆孹s 鍚庡彲鑾峰彇銆嶆椂鏈€澶氱瓑 90 绉?|
| 鎹㈠彿鍚?Cursor 鎶㈠墠鍙?| 鑴氭湰浼氳嚜鍔ㄧ疆椤?AIassistant 鍐嶇偣 OK |

## 璁稿彲

MIT

