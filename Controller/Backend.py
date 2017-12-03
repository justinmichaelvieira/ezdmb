from Model import CreateDBSchema
from Controller import ContentHttpServer
from multiprocessing import Process


class BootstrapAPI():
    def __init__(self):
        Popen("python3 Model/CreateDBSchema.py")
        Popen("python3 Controller/ContentHttpServer.py")
        #CreateDBSchema.CreateDBSchema()