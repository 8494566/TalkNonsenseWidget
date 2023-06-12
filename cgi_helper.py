#-*- encoding:utf-8 -*-
import itertools
import json
from PyQt5 import QtCore, QtNetwork, QtWidgets

PROPERTY_UNIQUE_ID = "PROPERTY_UNIQUE_ID"
PROPERTY_CONTEXT = "PROPERTY_CONTEXT"

class CgiHelper(QtCore.QObject):
    def __init__(self, parent=None):
        super(CgiHelper, self).__init__(parent)
        self.uniqueId = itertools.count()
        next(self.uniqueId)
        self.uniqueId2callBack = {}
        self.networkManager = QtNetwork.QNetworkAccessManager(self)
        self.networkManager.finished.connect(self.onNetworkReply)
        self.isStop = False

    def request(self, url, callback, queryDict=None, context=None):
        """
        :param url: url
        :param callback: f(isSuccess, byteArrayData, uniqueId, context)
        :param queryDict:{"name":"Tom", ...}
        """
        if self.isStop:
            return False

        targetUrl = QtCore.QUrl(url)
        if not targetUrl.isValid():
            return False

        urlQuery = QtCore.QUrlQuery()
        if isinstance(queryDict, dict) and queryDict:
            for key, value in list(queryDict.items()):
                urlQuery.addQueryItem(str(key), str(value))
            targetUrl.setQuery(urlQuery)

        request = QtNetwork.QNetworkRequest(targetUrl)
        return self.get(request, callback, context)

    def requestPost(self, url, headers, data, callback, queryDict=None, context=None):
        if self.isStop:
            return False

        targetUrl = QtCore.QUrl(url)
        if not targetUrl.isValid():
            return False

        urlQuery = QtCore.QUrlQuery()
        if isinstance(queryDict, dict) and queryDict:
            for key, value in list(queryDict.items()):
                urlQuery.addQueryItem(str(key), str(value))
            targetUrl.setQuery(urlQuery)

        request = QtNetwork.QNetworkRequest(targetUrl)
        for key, value in headers.items():
            request.setRawHeader(key.encode('utf-8'), value.encode('utf-8'))
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        return self.post(request, json_data, callback, context)

    def get(self, request, callback, context=None):
        reply = self.networkManager.get(request)
        return self.setupReply(reply, callback, context)

    def post(self, request, byteArray, callback, context=None):
        reply = self.networkManager.post(request, byteArray)
        return self.setupReply(reply, callback, context)

    def setupReply(self, reply, callback, context=None):
        uniqueId = next(self.uniqueId)
        reply.setProperty(PROPERTY_UNIQUE_ID, uniqueId)
        self.uniqueId2callBack[uniqueId] = callback

        if context is not None:
            reply.setProperty(PROPERTY_CONTEXT, "{}".format(context))

        return uniqueId

    def onNetworkReply(self, reply):
        reply.deleteLater()

        uniqueId = reply.property(PROPERTY_UNIQUE_ID)
        context = reply.property(PROPERTY_CONTEXT)
        httpStatus = reply.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute)
        if httpStatus is not None and 300 <= httpStatus < 400:
            targetUrl = reply.attribute(QtNetwork.QNetworkRequest.RedirectionTargetAttribute)
            if targetUrl.isValid():
                baseUrl = reply.url()
                url = baseUrl.resolved(targetUrl)
                newReply = self.networkManager.get(QtNetwork.QNetworkRequest(url))
                newReply.setProperty(PROPERTY_UNIQUE_ID, uniqueId)
                newReply.setProperty(PROPERTY_CONTEXT, context)
                return

        callBack = self.uniqueId2callBack.get(uniqueId)
        if callBack:
            del self.uniqueId2callBack[uniqueId]
            context = str("")
            callBack(reply.error() == QtNetwork.QNetworkReply.NoError,
                     reply.readAll(), uniqueId, context)

    def release(self):
        self.isStop = True
        self.uniqueId2callBack = {}


if "__main__" == __name__:
    import sys
    from PyQt5 import QtGui, QtWidgets
    def callBack(isSuccess, data):
        pass

    app = QtWidgets.QApplication(sys.argv)
    cgi = CgiHelper()
    cgi.request("http://www.baidu.com", callBack)
    cgi.request("http://www.baidu.com", callBack)
    cgi.request("http://www.baidu.com", callBack)
    cgi.request("http://www.baidu.com", callBack)
    app.exec_()
