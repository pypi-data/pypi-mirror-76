# -*- coding: utf-8 -*-

class CliException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
