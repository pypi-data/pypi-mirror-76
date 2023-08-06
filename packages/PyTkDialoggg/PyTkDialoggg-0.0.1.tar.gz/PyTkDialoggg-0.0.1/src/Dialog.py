__author__ = """
Arman Ahmadi
armanagha6@gmail.com
"""
import sys

if sys.version_info[0] != 3:
    raise Exception( \
        f'Python version must be 3, Got python {sys.version_info[0]}')

from tkinter import Tk, Frame, Label, Button

try:
    from PIL import Image, ImageTk
except ImportError:
    raise ImportError( \
        """This module images work with PIL module,
        \ryou should install it with run "<python-path> -m pip install pillow" in tour terminal""") from None
from ctypes import windll


class icons:
    INFORMATION = '.ICONS/INFORMATION.ico'
    QUESTION = '.ICONS/QUESTION.ico'
    CRITICAL = '.ICONS/CRITICAL.ico'
    WARNING = '.ICONS/WARNING.ico'


_DEF_ICON = icons.WARNING
_DEF_TITLE = 'Dialog'
_DEF_TEXT = """This module made by Arman Ahmadi
for messagebox, Everything like text or image or etc
Automatically will place on this window"""
_DEF_TEXT_ANCH = 'left'
_DEF_FONT = 'calibri'
_DEF_FONT_SIZE = 17
_DEF_BG = 'white'
_DEF_BUTTONS_WIDTH = 150
_DEF_BUTTONS_HEIGHT_RATIO = 1.25
_DEF_BUTTON_BORDER_WIDTH = 1
_DEF_BUTTONS_BG = '#e8e8e8'
_DEF_BUTTONS_FRAME_BG = 'gray90'
_DEF_BUTTONS_BORDER_COLOR = '#adadad'
_DEF_CLICK_BUTTON_BORDER_COLOR = '#0078d7'
_DEF_WIDTH = 700
_DEF_HEIGHT = 240
_DEF_RATIO = 35
_SCREEN_WIDTH = windll.user32.GetSystemMetrics(0)
_SCREEN_HEIGHT = windll.user32.GetSystemMetrics(1)


class Dialog:
    @staticmethod
    def __chk__(__key: str, __value):
        if __key in ['x', 'y', 'width', 'height', 'font_size']:
            if not isinstance(__value, int):
                raise ValueError( \
                    f"{__key} must have type <int>, Got type {type(__value)}")
        elif __key == 'ratio':
            if not 0 < __value < 100:
                raise ValueError( \
                    f"ratio should be between 0 and 100, Got {__value}")
        if __key == 'font_type':
            __StaticFontType = ('bold', 'italic', ('bold', 'italic'))
            if __value not in __StaticFontType:
                raise ValueError( \
                    f"font_type must be: '{', '.join(map(str, __StaticFontType))}', Got {__value}")
        elif __key == 'icon':
            if __value.split('.')[-1] != 'ico':
                raise TypeError( \
                    f"icon type should be .ico, Got type {__value.split('.')[-1]}")
        return __value

    def __init__(self, **kwargs):
        for kwarg in kwargs:
            Dialog.__chk__(kwarg, kwargs[kwarg])
        self.__Root = Tk()
        windll.shcore.SetProcessDpiAwareness(1)
        self.__Root.title(kwargs['title'] if 'title' in kwargs else _DEF_TITLE)
        self.__Root.iconbitmap(True, kwargs['icon'] if 'icon' in kwargs else _DEF_ICON)
        self.__Root.resizable(0, 0)
        self.__Root.configure(bg=kwargs['bg'] if 'bg' in kwargs else _DEF_BG)

        def callback(x_y):
            __StaticWidget = self.__Root.winfo_containing(x_y.x_root, x_y.y_root)
            if isinstance(__StaticWidget, Button):
                list(self.__Buttons.values())[0 if __StaticWidget in self.__Buttons['left'].keys() else 1][
                    __StaticWidget][1]['highlightbackground'] = _DEF_CLICK_BUTTON_BORDER_COLOR
            elif isinstance((__StaticWidget.winfo_children()[0] if __StaticWidget.winfo_children() else None)
                            if isinstance(__StaticWidget, Frame) else None, Button):
                __StaticWidget['bg'] = _DEF_CLICK_BUTTON_BORDER_COLOR
            else:
                for _Side in self.__Buttons.values():
                    for _Items in _Side.values():
                        _Items[1]['highlightbackground'] = _Items[2]

        self.__Root.bind('<Motion>', callback)
        self.geometry = {
            'width': kwargs['width'] if 'width' in kwargs else _DEF_WIDTH,
            'height': kwargs['height'] if 'height' in kwargs else _DEF_HEIGHT
        }
        self.geometry.update({
            'static_width': self.geometry['width'],
            'x': int(kwargs['x'] if 'x' in kwargs else ((_SCREEN_WIDTH / 2) - (self.geometry['width'] / 2))),
            'y': int(kwargs['y'] if 'y' in kwargs else ((_SCREEN_HEIGHT / 2) - (self.geometry['height'] / 2))),
            'ratio': kwargs['ratio'] if 'ratio' in kwargs else _DEF_RATIO
        })
        self.__Font = (kwargs['font'] if 'font' in kwargs else _DEF_FONT,
                       kwargs['font_size'] if 'font_size' in kwargs else _DEF_FONT_SIZE,
                       kwargs['font_type'] if 'font_type' in kwargs else '')
        self.__TopHeight = self.geometry['height'] - (self.geometry['height'] / 100 * self.geometry['ratio'])
        self.__BottomHeight = self.geometry['height'] - self.__TopHeight
        self.__TextLabel = Label(self.__Root,
                                 bg=self.__Root['bg'],
                                 text=kwargs['text'] if 'text' in kwargs else _DEF_TEXT,
                                 font=self.__Font,
                                 fg=kwargs['font_color'] if 'font_color' in kwargs else 'black',
                                 justify=kwargs['anchor'] if 'anchor' in kwargs else _DEF_TEXT_ANCH)
        self.__TextLabel.place(x=self.__TopHeight,
                               y=int((self.__TopHeight / 2) - (
                                       (self.__TextLabel['text'].count('\n') + 1) * 2 * self.__Font[1] / 2)))
        self.__Image = ImageTk.PhotoImage(
            Image.open(kwargs['image'] if 'image' in kwargs else _DEF_ICON).resize(
                (int(self.__TopHeight / 4 * 2), int(self.__TopHeight / 4 * 2))))
        Label(self.__Root, bg=self.__Root['bg'], image=self.__Image).place(x=self.__TopHeight / 4,
                                                                           y=self.__TopHeight / 5)
        self.__Buttons = {'left': {}, 'right': {}}
        self.__ButtonsFrame = Frame(self.__Root,
                                    bg=kwargs['buttons_bg'] if 'buttons_bg' in kwargs else _DEF_BUTTONS_FRAME_BG)
        self.__ButtonsFrame.place(x=0,
                                  y=self.__TopHeight,
                                  width=self.geometry['width'],
                                  height=self.geometry['height'] * 100 / self.geometry['ratio'])
        self.set_geometry()

    def add_button(self, text: str, side: str, command=None, **kwargs):
        for arg in kwargs:
            Dialog.__chk__(arg, kwargs[arg])
        if side not in ('left', 'right'):
            raise ValueError( \
                f"side must be 'left' or 'right', Got {side}")
        if command and not callable(command):
            raise TypeError( \
                f"command must be function, Got {type(command)}")
        __StaticWidth = kwargs['width'] if 'width' in kwargs else _DEF_BUTTONS_WIDTH
        __StaticHeight = kwargs['height'] if 'height' in kwargs else ((self.__BottomHeight / 2) -
                                                                      (self.__BottomHeight / 6)) * \
                                                                     _DEF_BUTTONS_HEIGHT_RATIO
        __StaticFrame = Frame(self.__ButtonsFrame,
                              bg=kwargs['bg'] if 'bg' in kwargs else self.__ButtonsFrame['bg'],
                              highlightbackground=kwargs[
                                  'border_color'] if 'border_color' in kwargs else _DEF_BUTTONS_BORDER_COLOR,
                              highlightthickness=kwargs['bd'] if 'bd' in kwargs else _DEF_BUTTON_BORDER_WIDTH,
                              borderwidth=0)

        def __DefPos():
            try:
                self.set_geometry(x=self.__Root.winfo_x(),
                                  y=self.__Root.winfo_y())
            except:
                pass

        __StaticButton = Button(__StaticFrame,
                                text=text,
                                bg=kwargs['bg'] if 'bg' in kwargs else _DEF_BUTTONS_BG,
                                font=(kwargs['font'] if 'font' in kwargs else _DEF_FONT,
                                      int(__StaticHeight / 2),
                                      kwargs['font_type'] if 'font_type' in kwargs else ''),
                                bd=0,
                                command=(lambda: (command(), __DefPos()) if command else None))
        if side == 'left':
            __StaticFrame.place(
                x=(int(self.geometry['width'] / 100 * 3.5) if not self.__Buttons['left'] else 10) +
                  (list(self.__Buttons['left'].values())[-1][-1] if self.__Buttons['left'] else 0),
                y=int(self.__BottomHeight / 6),
                width=__StaticWidth,
                height=__StaticHeight)
            __StaticButton.place(x=0,
                                 y=0,
                                 width=int(__StaticFrame.place_info()['width']) - (
                                         int(__StaticFrame['highlightthickness']) * 2),
                                 height=int(__StaticFrame.place_info()['height']) - (
                                         int(__StaticFrame['highlightthickness']) * 2))
        elif side == 'right':
            __StaticSpace = int(self.geometry['width'] / 100 * 3.5) if not self.__Buttons['right'] else 10
            __StaticFrame.place(
                x=self.geometry['static_width'] - __StaticWidth - __StaticSpace,
                y=int(self.__BottomHeight / 6),
                width=__StaticWidth,
                height=__StaticHeight)
            self.geometry['static_width'] -= (__StaticWidth + __StaticSpace)
            __StaticButton.place(x=0,
                                 y=0,
                                 width=int(__StaticFrame.place_info()['width']) - (
                                         int(__StaticFrame['highlightthickness']) * 2),
                                 height=int(__StaticFrame.place_info()['height']) - (
                                         int(__StaticFrame['highlightthickness']) * 2))
        self.__Buttons[side].update({__StaticButton: (__StaticButton['bg'],
                                                      __StaticFrame,
                                                      __StaticFrame['highlightbackground'],
                                                      int(__StaticFrame.place_info()['width']),
                                                      int(__StaticFrame.place_info()['x']) + int(
                                                          __StaticFrame.place_info()['width']))})

    def set_geometry(self, **kwargs):
        self.__Root.geometry(
            "{}x{}+{}+{}".format(
                Dialog.__chk__('width', kwargs['width']) if 'width' in kwargs else self.geometry['width'],
                Dialog.__chk__('height', kwargs['height']) if 'height' in kwargs else self.geometry['height'],
                Dialog.__chk__('x', kwargs['x']) if 'x' in kwargs else self.geometry['x'],
                Dialog.__chk__('y', kwargs['y']) if 'y' in kwargs else self.geometry['y'])
        )
        return self.geometry

    def config(self, **kwargs):
        for arg in kwargs:
            if arg in self.geometry:
                self.geometry[arg] = Dialog.__chk__(arg, kwargs[arg])
            if arg == 'bg':
                self.__Root['bg'] = arg
            if arg == 'text':
                self.__TextLabel['text'] = kwargs['text']
                self.__TextLabel.place(x=self.__TopHeight,
                                       y=int((self.__TopHeight / 2) - (
                                               (self.__TextLabel['text'].count('\n') + 1) * 2 * self.__Font[1] / 2)))
        self.set_geometry()
        return kwargs

    def destroy(self):
        return self.__Root.destroy()

    def __call__(self, *args, **kwargs):
        self.__Root.update()

        hwnd = windll.user32.GetParent(self.__Root.winfo_id())
        windll.user32.SetWindowLongPtrW(hwnd, -16, windll.user32.GetWindowLongPtrW(hwnd, -16) & ~ 65536 & ~ 131072)
        windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 2 | 1 | 4 | 32)

        while True:
            for func in args:
                if callable(func):
                    func()
            try:
                self.__Root.update()
            except:
                break


if __name__ == '__main__':
    main = Dialog(bg='red')
    main.add_button('Ok', 'right', lambda: main.destroy())


    def Show():
        MyEmail = Tk()
        Label(MyEmail, text='armanagha6@gmail.com').pack()


    main.add_button('my email', 'right', font_type='bold', command=Show)
    main.add_button('TeSt', 'left', font='Comic Sans MS')
    main()
