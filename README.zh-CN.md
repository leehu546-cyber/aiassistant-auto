# AIassistant 自动换号

**Language / 语言:** [English](README.en.md) | **[简体中文](README.zh-CN.md)**

Windows 桌面自动化脚本：在 **AIassistant（AI助手）** 中自动完成 Cursor 换号。

## 功能

| 步骤 | 操作 |
|------|------|
| 1 | 点击左侧 **Cursor** 菜单（已在 Cursor 页则跳过） |
| 2 | 点击 **获取账号并登录**（冷却中自动等待） |
| 3 | 点击 **Yes** 确认换号 |
| 4 | 等待 **60 秒**（换号进行中） |
| 5 | 将 AIassistant **置顶**（避免被 Cursor 挡住） |
| 6 | 点击 **OK** 确认成功 |
| 7 | **最小化** AIassistant |

## 环境要求

- Windows 10/11
- Python 3.10+
- AIassistant 已安装（窗口标题：`AI助手` / `AIassistant` / `AI Assistant`）

## 安装

```powershell
git clone https://github.com/leehu546-cyber/aiassistant-auto.git
cd aiassistant-auto
pip install -r requirements.txt
```

## 用法

### 完整流程

```powershell
python aiassistant_auto.py
```

预计 **1~2 分钟**（含 60 秒换号等待）。

### 分步运行

```powershell
python aiassistant_auto.py --yes    # 仅点击 Yes
python aiassistant_auto.py --ok     # 仅点击 OK 并最小化
python aiassistant_auto.py --scan   # 列出所有按钮（调试）
```

## 配置

编辑 `aiassistant_auto.py` 顶部：

```python
OK_DELAY_AFTER_YES = 60   # Yes 后等待换号完成的秒数
OK_POLL_TIMEOUT = 120     # 等待 OK 弹窗的最长秒数
```

## 技术说明

- 使用 **pywinauto UIA** 的 `invoke()` 点击 Qt 控件
- **不移动鼠标**，可边用电脑边运行
- PostMessage / OCR 对此 Qt 应用无效

## 参考项目

- [pywinauto/pywinauto](https://github.com/pywinauto/pywinauto)
- [Qt 按钮点击 Issue #1252](https://github.com/pywinauto/pywinauto/issues/1252)

## 常见问题

| 现象 | 处理 |
|------|------|
| 未找到窗口 | 先打开 AIassistant |
| Yes/OK 找不到 | Cursor 可能挡住窗口；用 `--ok` 单独处理 |
| 按钮冷却 | 显示「Xs 后可获取」时最多等 90 秒 |
| 换号后 Cursor 抢前台 | 脚本会自动置顶 AIassistant 再点 OK |

## 许可

MIT
