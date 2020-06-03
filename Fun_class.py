# from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication


class App(QApplication):
    pass
    # def notify(self, recevier, evt):
    #     if recevier.inherits("QPushButton") and evt.type() == QEvent.MouseButtonPress:
    #         pass
    #         # print(recevier, evt)
    #     return super().notify(recevier, evt)


class Btn(QPushButton):
    pass
    # def event(self, evt):
    #     if evt.type() == QEvent.MouseButtonPress:
    #         print(evt,"被点击了")
    #     return super().event(evt)
    # def mousePressEvent(self, *args,**kwargs) :
    #     print("鼠标被按下了。。")
    #     return super().mousePressEvent(*args,**kwargs)