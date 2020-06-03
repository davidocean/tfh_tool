import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

from main_ui import Ui_MainWindow
from tfh_calc import *
from GLOBE_CONST import *
from dialog_ui import Ui_Dialog

# 创建对话框类
class dialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def change_text(self, s):
        print(s)

        self.textEdit.setText(s)
    # def show(self):
    #     super().show()


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("学习")
        self.setupUi(self)

    # 根据图幅号获取经纬度的四角坐标
    def ui_get_jwd(self):
        content = self.lineEdit.text()
        content = content.upper()
        result = get_jwd(content)

        if result:
            s0 = content + "的四角坐标为：\n"
            s1 = "经度最小值：" + str(result[LON_MIN]) + "\n"
            s2 = "纬度最小值:" + str(result[LAT_MIN]) + "\n"
            s3 = "经度最大值:" + str(result[LON_MAX]) + "\n"
            s4 = "纬度最大值:" + str(result[LAT_MAX]) + "\n"
            s = s0 + s1 + s2 + s3 + s4
            self.textEdit.setText(s)

        else:
            self.textEdit.setText(content + "错误，" + "请输入标准图幅号。")

    # 根据经纬度获取各比例尺图幅号
    def ui_get_tfh(self):
        content_x = self.lineEdit_3.text()
        content_y = self.lineEdit_4.text()
        if not is_number(content_x):
            print("x is not number")
            self.textEdit_2.setText("经度错误，请重新输入。")
            return
        if not is_number(content_y):
            self.textEdit_2.setText("纬度错误，请重新输入。")
            return
        result = get_tfh(content_x, content_y)
        if not result:
            self.textEdit_2.setText("经纬度范围错误，请输入范围：\n" + "经度：70-150\n" + "纬度：0-56")
        else:
            s = "经度：" + content_x + "  纬度：" + content_y + "  的各比例尺图幅号如下：\n" + "比例尺:图幅号\n"
            for i in result:
                s = s + SCALE_CN[i] + ":" + result[i] + "\n"
            self.textEdit_2.setText(s)

    # 度分秒转十进制
    def ui_DD_Decimal(self):
        content_d = self.lineEdit_5.text()
        content_f = self.lineEdit_6.text()
        content_m = self.lineEdit_7.text()
        result = DD_Decimal(content_d, content_f, content_m)
        s = content_d + "°" + content_f + "′" + content_m + "″"
        if not result:
            self.textEdit_3.insertPlainText(s + "错误," + "请检查并重新输入。\n")
        else:
            s = s + " 的十进制数为：" + str(result)

            self.textEdit_3.insertPlainText(s + "\n")

        # print("ui_DD_Decimal", content_d, content_f, content_m)

    def ui_D2Dms(self):
        content = self.lineEdit_8.text()
        result = D2Dms(content)

        if not result:
            s = content + "错误," + "请检查并重新输入。\n"
            self.textEdit_3.insertPlainText(s)
        else:
            s = content + "的度分秒为：" + result + "\n"
            self.textEdit_3.insertPlainText(s)
        # print("ui_D2Dms", content)


# def dialog_banben_show(Dialog):
#     Dialog.show()


def edition_dialog_show():
    d.setWindowTitle("版本信息")
    d.change_text(BANBEN_INFO)
    d.show()

def help_dialog_show():
    d.setWindowTitle("帮助信息")
    d.change_text(HELP_INFO)
    d.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    d = dialog()
    # 对菜单中的版本信息和帮助信息进行事件绑定
    window.edition_action.triggered.connect(edition_dialog_show)
    window.help_action.triggered.connect(help_dialog_show)

    window.show()

    sys.exit(app.exec_())
