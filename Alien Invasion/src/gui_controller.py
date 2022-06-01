from _winapi import SW_HIDE
from cefpython3 import cefpython as cef
import sys
import ctypes

from win32con import SW_SHOW


class GuiController():

    def __init__(self, settings):
        sys.excepthook = cef.ExceptHook
        cef.Initialize(settings={"multi_threaded_message_loop": True})
        #cef.MessageLoop()
        self.browser = []
        self.hwnd = []
        self.js = cef.JavascriptBindings()
        self.js.SetObject('settings', settings)

    def browser_create(self, url, window_info=cef.WindowInfo(), title="untitled", show=True):
        browser = cef.CreateBrowserSync(url=url, window_info=window_info, window_title=title)
        browser.SetJavascriptBindings(self.js)
        browser.SetFocus(False)
        self.browser.append(browser)
        self.hwnd.append(browser.GetWindowHandle())
        if show:
            ctypes.windll.user32.ShowWindow(browser.GetWindowHandle(), SW_SHOW)
        else:
            ctypes.windll.user32.ShowWindow(browser.GetWindowHandle(), SW_HIDE)

    def browser_embed(self, url, target, width, height, title="untitled", show=True):
        window_info = cef.WindowInfo()
        #window_info.SetAsChild(int(target), [0, 0, width, height])
        window_info.SetAsPopup(int(target), "test")
        cef.PostTask(cef.TID_UI, self.browser_create, url, window_info,  title, show)

    def browser_refresh(self):
        for browser in self.browser:
            browser.Reload()


