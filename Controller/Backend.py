from Controller.ContentHttpServer import setupContentServer
from Controller.RestApiServer import setupRestApi
from multiprocessing import Process


class Backend:
    def __init__(self):
        self.startContentServer()
        # self.startRestApi()

    def startContentServer(self):
        d1 = Process(name="daemon1", target=setupContentServer)
        d1.daemon = True
        d1.start()

    def startRestApi(self):
        d2 = Process(name="daemon2", target=setupRestApi)
        d2.daemon = True
        d2.start()
