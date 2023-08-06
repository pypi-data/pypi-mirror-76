# coding=utf-8

class Client:

    secret_key = ""
    access_key = ""

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key


def NewClient(access_key, secret_key):
    return Client(access_key, secret_key)
