#coding=utf-8
from multiprocessing.managers import BaseManager
import traceback

class queueManager():
    def __init__(self, server_addr = '127.0.0.1'):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        self.manager = BaseManager(address=(server_addr, 5000), authkey=b'abc')
    def connect(self):
        print('Connectting to server... ')
        self.manager.connect()
        self.task = self.manager.get_task_queue()
        self.result = self.manager.get_result_queue()
        print('Connectted to server!!! ')
    def read(self):
        return self.task.get()
    def write(self, data):
        self.result.put(data)
