# -*- coding: utf-8 -*-
# ============================================================================ #
# Created on: 2023/04/21 11:10
# Author: 王高亮
# Description: 控制打开浏览器的小软件,可瞎掰王游戏减少人力,当做上帝使用,打开charGTP,询问问题并回答
# ============================================================================ #
import sys
import keyboard
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class talkNonsenseWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(talkNonsenseWidget, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(500, 200)

        self.quizButton = QtWidgets.QPushButton(self)
        self.quizButton.setGeometry(0, 10, 100, 20)
        self.quizButton.setText("获取问题")
        self.quizButton.clicked.connect(self.quizVocabulary)

        self.getDarkButton = QtWidgets.QPushButton(self)
        self.getDarkButton.setGeometry(0, 40, 100, 20)
        self.getDarkButton.setText("天黑请闭眼")
        self.getDarkButton.clicked.connect(self.getDarkResult)

        self.countDown = QtCore.QTimer(self)
        self.countDown.setInterval(1000)  # 设置一秒执行一次
        self.countDown.timeout.connect(self.onCountDownTime)

        label = QtWidgets.QLabel(self)
        label.setText("老实人睁眼时间:")
        label.adjustSize()
        label.move(self.quizButton.x() + self.quizButton.width() + 10, 10)

        self.countDownMixTime = 20  # 老实人最大睁眼时间 暂定20秒
        self.countDownConst = self.countDownMixTime

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(label.x() + label.width() + 5, label.y() - 3, 40, 20)
        self.lineEdit.setValidator(QtGui.QIntValidator(5, 100))  # 设置输入范围
        self.lineEdit.textChanged.connect(self.onTextChanged)
        self.lineEdit.setText(str(self.countDownMixTime))

        self.daybreakMusicStartPlayer = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile("daybreakMusicStart.mp3")
        content = QMediaContent(url)
        self.daybreakMusicStartPlayer.setMedia(content)

        self.daybreakMusicPlayer = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile("daybreakMusic.mp3")
        content = QMediaContent(url)
        self.daybreakMusicPlayer.setMedia(content)

        self.countDownStartPlayer = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile("countDownStart.mp3")
        content = QMediaContent(url)
        self.countDownStartPlayer.setMedia(content)

        self.countDownStopPlayer = QMediaPlayer()
        url = QtCore.QUrl.fromLocalFile("countDownStop.mp3")
        content = QMediaContent(url)
        self.countDownStopPlayer.setMedia(content)

        self.driver = None
        self.playgroundInput = None

        self.FirstQuestion = False

        self.initChrome()

    # 开启浏览器
    def initChrome(self):
        url = 'https://gpt-api-demo.hz.netease.com/#'
        options = webdriver.ChromeOptions()
        options.add_argument('--enable-logging')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        # 设置等待条件：等待元素可见
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.ID, 'corp_id_for_corpid')))

        if not element:
            return

        # 登录
        # 输入内容
        username_field = self.driver.find_element(By.ID, 'corp_id_for_corpid')  # 找到指定ID的输入框元素
        username_field.clear()
        username_field.send_keys('')

        # 输入内容
        password_field = self.driver.find_element(By.ID, 'corp_id_for_corppw')  # 找到指定ID的输入框元素
        password_field.clear()
        password_field.send_keys('')

        keyboard.press_and_release('enter')

        element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'ant-modal-body')))
        if not element:
            return
        keyboard.press_and_release('esc')

        checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox']")
        checkbox.click()

    def quizVocabulary(self):
        self.driver.maximize_window()  # 如果最小化状态 还原
        if not self.playgroundInput:
            self.playgroundInput = self.driver.find_element(By.CSS_SELECTOR, '.ant-input.playground-image-input')
        if not self.playgroundInput:
            return
        if not self.FirstQuestion:
            text = """
                    你现在是一位《瞎掰王》桌游制作员
                    给我一个冷门且有趣的专有词语或者一段话，词语可以是世界范围，并给出两个通过字面含义会联想到的领域和一个正确的领域，三个领域需要不同方向的。
                    第一次回答时不需要告诉我哪个领域是正确的，我在再次向你提问：公布答案 时候向我展示这个专有名词的解释和正确的领域。
                    示例：血刃科技
                    领域：风险/动漫/医疗
            """
            self.FirstQuestion = True
        else:
            text = "下一题"

        self.playgroundInput.send_keys(text)
        self.playgroundInput.send_keys(Keys.CONTROL + Keys.ENTER)

    def onCountDownTime(self):
        if not self.countDownConst:
            self.countDown.stop()
            self.driver.minimize_window()  # 最小化浏览器
            # 这里播放老实人闭眼的音乐
            self.countDownStopPlayer.play()
            QtCore.QTimer.singleShot(3000, self.daybreakMusic)

            return
        self.countDownConst -= 1
        self.update()

    def daybreakMusic(self):
        self.countDownConst = self.countDownMixTime
        # 这里播放天亮的音乐
        self.daybreakMusicPlayer.play()
        self.update()

    def getDarkResult(self):
        # 这里播放天黑请闭眼的音乐
        self.daybreakMusicStartPlayer.play()
        # 三秒后 开启老实人睁眼
        QtCore.QTimer.singleShot(3000, self.daybreakResult)

    def daybreakResult(self):
        if not self.playgroundInput:
            return
        # 先公布答案
        self.driver.maximize_window()  # 如果最小化状态 先还原
        self.playgroundInput.send_keys('公布答案')
        self.playgroundInput.send_keys(Keys.CONTROL + Keys.ENTER)
        # 这里播放老实人睁眼的音乐
        self.countDownStartPlayer.play()
        # 开启倒计时给老实人提示
        self.countDown.start()

    def onTextChanged(self, text):
        if not text:
            return
        self.countDownMixTime = int(text)
        self.countDownConst = self.countDownMixTime

    def paintEvent(self, event):
        Painter = QtGui.QPainter(self)

        Painter.save()
        Painter.setRenderHints(
            QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing | QtGui.QPainter.SmoothPixmapTransform)
        Painter.rotate(-10)

        # 画文字
        ft = QtGui.QFont("Microsoft YaHei", 50, QtGui.QFont.Bold)
        Painter.setFont(ft)
        if self.countDownConst <= 0:
            text = "老实人请闭眼"
        elif self.countDownConst < self.countDownMixTime:
            text = str(self.countDownConst)
        else:
            text = "天亮了"
        inRect = QtCore.QRect(0, 80, self.width() - 100, 20)
        fm = QtGui.QFontMetrics(ft)
        rt = fm.boundingRect(inRect, QtCore.Qt.AlignRight, text)
        path = QtGui.QPainterPath()
        path.addText(rt.bottomLeft(), ft, text)
        Painter.strokePath(path, QtGui.QPen(QtGui.QColor("#3F1212"), 2))
        Painter.fillPath(path, QtGui.QBrush(QtGui.QColor("#FFED8F")))
        Painter.restore()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wnd = talkNonsenseWidget(None)
    wnd.show()
    sys.exit(app.exec_())
