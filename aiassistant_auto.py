#!/usr/bin/env python3
"""
AI助手 自动换号脚本 — pywinauto UIA + OCR 备用

Qt 应用必须用 UIA 的 invoke() 才能真正点击按钮（PostMessage/OCR 点击无效）。

流程：Cursor 菜单 → 获取账号并登录 → Yes → OK

用法：
    python aiassistant_auto.py           # 执行完整流程
    python aiassistant_auto.py --yes     # 仅点击 Yes（弹窗已打开时）
    python aiassistant_auto.py --scan    # 列出所有按钮
"""

from __future__ import annotations

import argparse
import sys
import time

from pywinauto import Desktop

WINDOW_TITLE_KEYS = ("AI助手", "AI Assistant", "AIassistant", "aiassistant", "AiAssistant")
OK_DELAY_AFTER_YES = 60  # Yes 后等待换号完成（秒）
OK_POLL_TIMEOUT = 120      # 等待 OK 弹窗的最长时间（秒）


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


def is_aiassistant_window(title: str) -> bool:
    t = title.strip().lower().replace(" ", "")
    # 排除快捷方式启动的控制台窗口（标题含"换号"）
    if "换号" in t:
        return False
    return any(k.lower().replace(" ", "") in t or t in k.lower().replace(" ", "") for k in WINDOW_TITLE_KEYS)


def get_main_window():
    desktop = Desktop(backend="uia")
    candidates = []
    for w in desktop.windows():
        try:
            title = w.window_text()
            if not is_aiassistant_window(title):
                continue
            try:
                if not w.is_visible():
                    continue
            except Exception:
                pass
            r = w.rectangle()
            if r.width() <= 100 or r.height() <= 100:
                continue
            area = r.width() * r.height()
            candidates.append((area, w))
        except Exception:
            continue
    if not candidates:
        raise RuntimeError("未找到 AIassistant / AI助手 窗口，请先打开")
    # 按面积降序排列，优先选择包含侧边栏按钮的窗口
    candidates.sort(key=lambda x: x[0], reverse=True)
    sidebar_keywords = {"Cursor", "首页", "充值续费", "使用教程"}
    for area, candidate in candidates:
        try:
            win = desktop.window(handle=candidate.handle)
            for btn in win.descendants(control_type="Button"):
                if btn.window_text().strip() in sidebar_keywords:
                    return win
        except Exception:
            continue
    # 兜底：返回面积最大的
    return desktop.window(handle=candidates[0][1].handle)


SIDEBAR_ITEMS = {"首页", "Cursor", "充值续费", "使用教程"}


def click_sidebar(win, name: str) -> bool:
    """点击左侧菜单。"""
    for btn in win.descendants(control_type="Button"):
        if btn.window_text().strip() == name and name in SIDEBAR_ITEMS:
            log(f"  点击菜单: {name!r}")
            btn.invoke()
            return True
    return False


def click_button(win, title_re: str, exact: str | None = None) -> bool:
    """通过 UIA invoke 点击按钮。"""
    if exact:
        btn = win.child_window(title=exact, control_type="Button")
    else:
        btn = win.child_window(title_re=title_re, control_type="Button")

    if not btn.exists(timeout=3):
        return False

    text = btn.window_text().strip()
    log(f"  点击按钮: {text!r}")
    btn.invoke()
    return True


def wait_button(win, title_re: str, exact: str | None = None, timeout: float = 60):
    """等待按钮出现。"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if exact:
            btn = win.child_window(title=exact, control_type="Button")
        else:
            btn = win.child_window(title_re=title_re, control_type="Button")
        if btn.exists(timeout=0.5):
            return btn
        time.sleep(0.8)
    return None


def is_on_cursor_page(win) -> bool:
    for btn in win.descendants(control_type="Button"):
        if "获取账号" in btn.window_text():
            return True
    return False


def find_dialog_button(win, label: str):
    """查找弹窗中的 Yes/OK 按钮（同名可能有多个，取弹窗区域）。"""
    candidates = []
    for btn in win.descendants(control_type="Button"):
        if btn.window_text().strip() == label:
            try:
                candidates.append((btn, btn.rectangle()))
            except Exception:
                candidates.append((btn, None))

    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0][0]

    def score(item):
        btn, r = item
        if r is None:
            return -9999
        cy = (r.top + r.bottom) // 2
        cx = (r.left + r.right) // 2
        return cy * 2 + cx

    return max(candidates, key=score)[0]


def bring_to_front() -> None:
    """把 AIassistant 提到最前（换号后 Cursor 可能挡住弹窗）。"""
    import win32api
    import win32con
    import win32gui
    import win32process

    win = get_main_window()
    hwnd = win.handle

    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        0,
        0,
        0,
        0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW,
    )
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_NOTOPMOST,
        0,
        0,
        0,
        0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW,
    )

    fg = win32gui.GetForegroundWindow()
    if fg != hwnd:
        fg_tid = win32process.GetWindowThreadProcessId(fg)[0]
        target_tid = win32process.GetWindowThreadProcessId(hwnd)[0]
        cur_tid = win32api.GetCurrentThreadId()
        attached = False
        try:
            if cur_tid != target_tid:
                win32process.AttachThreadInput(cur_tid, target_tid, True)
                attached = True
            win32gui.BringWindowToTop(hwnd)
            try:
                win32gui.SetForegroundWindow(hwnd)
            except Exception:
                try:
                    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
                    try:
                        win32gui.SetForegroundWindow(hwnd)
                    except Exception:
                        pass
                    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
                except Exception:
                    pass
        finally:
            if attached:
                win32process.AttachThreadInput(cur_tid, target_tid, False)

    try:
        win.set_focus()
    except Exception:
        pass
    time.sleep(0.4)
    log("AIassistant 已置顶到最前")


def ensure_visible() -> None:
    """若窗口最小化则恢复。若窗口在屏幕外则移回屏幕中央。"""
    import win32con
    import win32gui
    import win32api

    win = get_main_window()
    hwnd = win.handle
    if win32gui.IsIconic(hwnd):
        log("窗口已最小化，正在恢复...")
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(1.5)
    # 检查窗口是否在屏幕外，移回屏幕中央
    try:
        r = win.rectangle()
        sw = win32api.GetSystemMetrics(0)
        sh = win32api.GetSystemMetrics(1)
        margin = 200
        is_offscreen = (
            r.left + r.width() < -margin
            or r.top + r.height() < -margin
            or r.left > sw + margin
            or r.top > sh + margin
        )
        if is_offscreen:
            log("窗口在屏幕外，移回屏幕中央...")
            new_left = max(0, (sw - r.width()) // 2)
            new_top = max(0, (sh - r.height()) // 2)
            win32gui.SetWindowPos(
                hwnd, 0, new_left, new_top, 0, 0,
                win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW,
            )
            time.sleep(0.5)
    except Exception:
        pass


def minimize_window() -> bool:
    """将 AI助手 最小化到任务栏。"""
    import win32con
    import win32gui

    win = get_main_window()
    hwnd = win.handle
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    log("AI助手 已最小化")
    return True


def click_yes_only() -> bool:
    win = get_main_window()
    deadline = time.time() + 15
    while time.time() < deadline:
        yes = find_dialog_button(win, "Yes")
        if yes:
            log(f"  找到 Yes @ {yes.rectangle()}")
            yes.invoke()
            log("Yes 已点击")
            return True
        time.sleep(0.8)
    log("未找到 Yes 按钮，请确认「确认换号」弹窗已打开")
    return False


def wait_for_dialog_button(win, label: str, timeout: float) -> object | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        bring_to_front()
        win = get_main_window()
        btn = find_dialog_button(win, label)
        if btn:
            return btn
        remaining = int(deadline - time.time())
        if remaining % 10 == 0 or remaining < 5:
            log(f"  等待「{label}」... ({remaining}s)")
        time.sleep(2.0)
    return None


def click_ok_and_minimize(wait_before: int = 0) -> bool:
    ensure_visible()

    if wait_before > 0:
        log(f"等待换号完成 {wait_before}s...")
        time.sleep(wait_before)

    log("置顶 AIassistant，准备点击 OK")
    bring_to_front()
    win = get_main_window()

    ok = wait_for_dialog_button(win, "OK", OK_POLL_TIMEOUT)
    if not ok:
        log("未找到 OK 按钮（换号成功弹窗）")
        return False

    bring_to_front()
    log(f"  找到 OK @ {ok.rectangle()}")
    ok.invoke()
    log("OK 已点击")
    time.sleep(0.5)
    minimize_window()
    return True


def click_ok_only(minimize: bool = False) -> bool:
    ensure_visible()
    bring_to_front()
    win = get_main_window()
    ok = find_dialog_button(win, "OK")
    if ok:
        log("OK 弹窗已出现，立即点击")
        return click_ok_and_minimize(wait_before=0)
    log(f"OK 尚未出现，等待 {OK_DELAY_AFTER_YES}s...")
    return click_ok_and_minimize(wait_before=OK_DELAY_AFTER_YES)


def safe_repr(text: str) -> str:
    try:
        return text.encode("utf-8", "replace").decode("utf-8")
    except Exception:
        return text.encode("gbk", "replace").decode("gbk", "replace")


def list_buttons() -> None:
    win = get_main_window()
    log("当前可见按钮：")
    for btn in win.descendants(control_type="Button"):
        text = btn.window_text().strip()
        if text:
            try:
                print(f"  {safe_repr(text):30} {btn.rectangle()}")
            except Exception:
                print(f"  {safe_repr(text)}")


def run_full() -> bool:
    log("=" * 50)
    log("AI助手 自动换号（从头开始）")
    log("=" * 50)

    ensure_visible()
    bring_to_front()
    time.sleep(1.0)
    win = get_main_window()

    # 1. Cursor 菜单
    if not is_on_cursor_page(win):
        log("步骤 1: 点击 Cursor 菜单")
        if not click_sidebar(win, "Cursor"):
            log("失败：找不到 Cursor 菜单")
            return False
        time.sleep(1.0)
        win = get_main_window()

    # 2. 获取账号并登录
    log("步骤 2: 点击「获取账号并登录」")
    btn = wait_button(win, ".*获取账号.*", timeout=30)
    if not btn:
        log("失败：按钮不可用（可能在冷却中）")
        return False
    text = btn.window_text()
    if "后可获取" in text or "秒" in text:
        log(f"按钮冷却中: {text!r}，等待...")
        deadline = time.time() + 90
        while time.time() < deadline:
            btn = wait_button(win, ".*获取账号.*", timeout=2)
            if btn and "后可获取" not in btn.window_text():
                break
            time.sleep(2)
        else:
            log("冷却超时")
            return False
    btn.invoke()
    log("  已点击获取账号")
    time.sleep(1.0)

    # 3. Yes 确认
    log("步骤 3: 点击 Yes")
    deadline = time.time() + 30
    yes = None
    while time.time() < deadline:
        yes = find_dialog_button(win, "Yes")
        if yes:
            break
        time.sleep(0.8)
    if not yes:
        log("失败：未出现 Yes 弹窗")
        return False
    yes.invoke()
    log("  已点击 Yes")
    time.sleep(1.0)

    # 4. OK 完成（换号需时间，先等 1 分钟）
    log(f"步骤 4: 等待 {OK_DELAY_AFTER_YES}s 后点击 OK")
    if not click_ok_and_minimize(wait_before=OK_DELAY_AFTER_YES):
        log("失败：未出现 OK 弹窗")
        return False

    log("=" * 50)
    log("全部完成！")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="AI助手 自动换号")
    parser.add_argument("--yes", action="store_true", help="仅点击 Yes")
    parser.add_argument("--ok", action="store_true", help="仅点击 OK 并最小化")
    parser.add_argument("--scan", action="store_true", help="列出所有按钮")
    args = parser.parse_args()

    try:
        if args.scan:
            list_buttons()
            sys.exit(0)
        if args.yes:
            sys.exit(0 if click_yes_only() else 1)
        if args.ok:
            sys.exit(0 if click_ok_only(minimize=True) else 1)
        sys.exit(0 if run_full() else 1)
    except RuntimeError as e:
        log(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
