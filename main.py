# -*- coding: utf-8 -*-
# ============================================================================ #
# Created on: 2023/04/21 11:10
# Author: 王高亮
# Description: 控制打开浏览器的小软件,可瞎掰王游戏减少人力,当做上帝使用,打开charGTP,询问问题并回答
# ============================================================================ #
import sys
import textwrap

from post_chat import post_chat
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


app_id = "5779dab9-8d51-4f8d-b7cc-cc26bc843dad"
app_key = "mrke45mm6jnvi64db8q58timadq771"


class talkNonsenseWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(talkNonsenseWidget, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(1020, 1000)

        self.quizButton = QtWidgets.QPushButton(self)
        self.quizButton.setGeometry(0, 10, 100, 20)
        self.quizButton.setText("获取问题")
        self.quizButton.clicked.connect(self.quizVocabulary)

        self.getDarkButton = QtWidgets.QPushButton(self)
        self.getDarkButton.setGeometry(0, 40, 100, 20)
        self.getDarkButton.setText("天黑请闭眼")
        self.getDarkButton.clicked.connect(self.getDarkResult)
        self.getDarkButton.setEnabled(False)

        self.publishAnswerButton = QtWidgets.QPushButton(self)
        self.publishAnswerButton.setGeometry(0, 70, 100, 20)
        self.publishAnswerButton.setText("公布答案")
        self.publishAnswerButton.clicked.connect(self.onPublishAnswer)
        self.publishAnswerButton.setEnabled(False)

        self.emptyButton = QtWidgets.QPushButton(self)
        self.emptyButton.setGeometry(0, 100, 100, 20)
        self.emptyButton.setText("清空问题")
        self.emptyButton.clicked.connect(self.onEmptyButton)

        self.sendingProblem = QtWidgets.QPushButton(self)
        self.sendingProblem.setGeometry(775, 140, 100, 20)
        self.sendingProblem.setText("发送问题")
        self.sendingProblem.clicked.connect(self.onSendingProblem)

        self.countDown = QtCore.QTimer(self)
        self.countDown.setInterval(1000)  # 设置一秒执行一次
        self.countDown.timeout.connect(self.onCountDownTime)

        label = QtWidgets.QLabel(self)
        label.setText("老实人睁眼时间:")
        label.adjustSize()
        label.move(self.quizButton.x() + self.quizButton.width() + 10, 10)

        self.assistantText = ""
        self.countDownMixTime = 20  # 老实人最大睁眼时间 暂定20秒
        self.countDownConst = self.countDownMixTime

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(label.x() + label.width() + 5, label.y() - 3, 40, 20)
        self.lineEdit.setValidator(QtGui.QIntValidator(5, 100))  # 设置输入范围
        self.lineEdit.textChanged.connect(self.onTextChanged)
        self.lineEdit.setText(str(self.countDownMixTime))

        self.inTextEdit = QtWidgets.QTextEdit(self)
        self.inTextEdit.setGeometry(self.lineEdit.x() + self.lineEdit.width() + 5, self.lineEdit.y(), 500, 150)
        self.inTextEdit.setFont(QtGui.QFont("Microsoft YaHei", 10))

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

        self.FirstQuestion = False

        self.messages = []

    def quizVocabulary(self):
        if not self.FirstQuestion:
            Text = """   你现在是一位《瞎掰王》桌游制作员给我一个冷门且有趣的专有词语或者一段话，词语可以是世界范围，并给出两个通过字面含义会联想到的领域和一个正确的领域，三个领域需要不同方向的。第一次回答时不需要告诉我哪个领域是正确的，我在再次向你提问：公布答案 时候向我展示这个专有名词的解释和正确的领域。\n示例：血刃科技\n领域：风险/动漫/医疗"""
            self.FirstQuestion = True
        else:
            Text = "下一题"
        self.inTextEdit.setPlainText(Text)

    def onCountDownTime(self):
        if not self.countDownConst:
            self.countDown.stop()
            # 这里播放老实人闭眼的音乐
            self.countDownStopPlayer.play()
            QtCore.QTimer.singleShot(3000, self.daybreakMusic)
            messages = self.messages[-3]
            if messages:
                self.assistantText = messages.get("content", "")
                self.update()
            return
        self.countDownConst -= 1
        self.update()

    def daybreakMusic(self):
        self.countDownConst = self.countDownMixTime
        # 这里播放天亮的音乐
        self.daybreakMusicPlayer.play()
        self.publishAnswerButton.setEnabled(True)
        self.update()

    def getDarkResult(self):
        # 这里播放天黑请闭眼的音乐
        self.daybreakMusicStartPlayer.play()
        # 三秒后 开启老实人睁眼
        QtCore.QTimer.singleShot(3000, self.daybreakResult)
        self.getDarkButton.setEnabled(False)

    def onPublishAnswer(self):
        if not self.messages:
            return
        messages = self.messages[-1]
        self.assistantText = messages.get("content", "")
        self.publishAnswerButton.setEnabled(False)
        self.update()

    def onEmptyButton(self):
        self.FirstQuestion = False
        self.messages = []
        self.assistantText = ""
        self.countDownConst = self.countDownMixTime
        self.inTextEdit.setText("")
        self.update()

    def getPostChatAppendMessages(self):
        response = post_chat(app_id, app_key, self.messages, 'gpt-3.5-turbo', 200, 0.7, 1, None, 0, 0)
        detail = response.get("detail", {})
        choices = detail.get("choices", [])
        for val in choices:
            messages = val.get("message", {})
            if not messages:
                continue
            self.assistantText = messages.get("content", "")
            self.messages.append(messages)
        self.update()

    def onSendingProblem(self):
        text = self.inTextEdit.toPlainText()
        if not text:
            return
        messages = {
                "role": "user",
                "content": text
            }
        self.messages.append(messages)
        self.getPostChatAppendMessages()
        self.getDarkButton.setEnabled(True)

    def daybreakResult(self):
        # 先公布答案
        messages = {
                "role": "user",
                "content": "公布答案"
            }
        self.messages.append(messages)
        self.getPostChatAppendMessages()
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

        # 画文字
        ft = QtGui.QFont("Microsoft YaHei", 30, QtGui.QFont.Bold)
        Painter.setFont(ft)
        if self.countDownConst <= 0:
            text = "老实人请闭眼"
        elif self.countDownConst < self.countDownMixTime:
            text = str(self.countDownConst)
        else:
            text = "天亮了"
        inRect = QtCore.QRect(self.inTextEdit.x() + self.inTextEdit.width(), 0, 250, 50)
        fm = QtGui.QFontMetrics(ft)
        rt = fm.boundingRect(inRect, QtCore.Qt.AlignHCenter, text)
        path = QtGui.QPainterPath()
        path.addText(rt.bottomLeft(), ft, text)
        Painter.strokePath(path, QtGui.QPen(QtGui.QColor("#3F1212"), 2))
        Painter.fillPath(path, QtGui.QBrush(QtGui.QColor("#FFED8F")))

        if not self.assistantText:
            Painter.end()
            return
        inRect = QtCore.QRect(10, 195, 985, 445)
        # 设置换行文本的宽度
        lineWidth = 500
        lines = fm.elidedText(self.assistantText, QtCore.Qt.ElideRight, lineWidth)
        lineRect = fm.boundingRect(lines)

        # 设置文本换行
        wrappedText = textwrap.fill(self.assistantText, width=int(lineWidth / fm.averageCharWidth()))

        path = QtGui.QPainterPath()
        yPos = 195
        for line in wrappedText.splitlines():
            rt = QtCore.QRectF(inRect.x(), inRect.y() + yPos, lineWidth, lineRect.height())
            path.addText(rt.bottomLeft(), ft, line)
            yPos += lineRect.height()

        Painter.strokePath(path, QtGui.QPen(QtGui.QColor("#3F1212"), 2))
        Painter.fillPath(path, QtGui.QBrush(QtGui.QColor("#FFED8F")))
        Painter.end()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wnd = talkNonsenseWidget(None)
    wnd.show()

    sys.exit(app.exec_())
