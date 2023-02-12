from cgitb import handler
import pywinauto
import pywinauto.timings

pywinauto.timings.Timings.window_find_timeout = 10

app = pywinauto.Application().connect(class_name="StandardFrame_DingTalk")# app.Properties.print_control_identifiers()
# dlg= app.window(best_match='FloatActionBar', top_level_only=False)
# app.UntitledNotepad.draw_outline()
# # 等待钉钉窗口出现
main = app.window(class_name="StandardFrame_DingTalk")
# main.print_control_identifiers()
main.draw_outline()
main.wait("visible")
chat = main.child_window(class_name="DingChatWnd")
chat.draw_outline()
cef = chat.child_window(class_name="Chrome_RenderWidgetHostHWND")
cef.draw_outline()
cef.type_keys("pywinauto Works!", with_spaces = True)
# ce = chat.child_window(handle="00000000000106AA")
# ce.draw_outline()
# chat['CefBrowserWindow2'].draw_outline()
from pywinauto.keyboard import send_keys
send_keys("AAA")
chat.print_control_identifiers()


# dlg = app.window(handle="0000000000F10000")
# window = findwindow(title = "Untitled - Notepad", class = "Notepad")

# 等待钉钉窗口出现
# dlg = app.window(title_re="钉钉")
# dlg.wait("visible")
# 关闭钉钉窗口
# dlg.close()

# from pywinauto.application import Application
# app = Application(backend="uia").start('notepad.exe')

# # 描述Notepad.exe进程内的窗口
# # dlg_spec = app.UntitledNotepad
# dlg_spec = app.window(title_re="无标题 - 记事本")

# # 等到窗户真的开着
# actionable_dlg = dlg_spec.wait('visible') 
# actionable_dlg.close()