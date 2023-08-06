# coding: utf-8
try:
    from urllib.parse import urlparse
except:
    from urlparse import urlparse
import grpc
from future.utils import raise_
from .proto.files_pb2_grpc import FileWorkerStub


class FileHandler:

    def __init__(self, req_url):
        self.channel = grpc.insecure_channel(req_url)
        self.stub = FileWorkerStub(self.channel)

    def create_file(self):
        pass

    def describe_file(self):
        pass

    def modify_file(self):
        pass

    def copy_file(self):
        pass

    def move_file(self):
        pass

    def __del__(self):
        if self.channel:
            self.channel.close()