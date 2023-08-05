import yaml
import os
import subprocess
from sys import platform

class parse(object):

    def __init__(self, rcfile, section='main'):
        rcfile = os.path.expanduser(rcfile)
        raw_yaml = yaml.load(open(rcfile))[section]
        shell_fields = ['password']
        self.yaml = {}

        for field, value in raw_yaml.items():
            if value[0:2] == '$ ':
                #value = os.popen(value[2:]).readline().strip()
                #value = os.popen("TERM=xterm %s" % value[2:], shell=True).readline().strip()
                if platform == "win32":
                    value = os.popen("%s" % value[2:]).readline().strip()
                else:
                    value = os.popen("TERM=xterm %s" % value[2:]).readline().strip()


            self.yaml[field] = value

    def contents(self):
        return self.yaml

    def __getitem__(self, item_name):
        return self.yaml[item_name]