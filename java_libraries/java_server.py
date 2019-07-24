import psutil
import subprocess
import os
import time
from common_functions import common_functions
from py4j.java_gateway import JavaGateway


def kill_proc_tree(pid):
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()


def create_command_bat():
    content = "cd java_libraries\n"
    content += '\"' + common_functions.get_java_path() + '\\java.exe\" '
    content += "-Dfile.encoding=UTF-8 -classpath .\\target\\classes;.\\py4j-0.10.8.1.jar;.\\tc2011dist.jar JDSTServer"

    f = open("command.bat", "w")
    f.write(content)
    f.close()


class JavaServer:
    def __init__(self):
        create_command_bat()
        self.process = subprocess.Popen('command.bat')
        time.sleep(5)
        self._apiwrapper = JavaGateway().entry_point

    def get_jds(self, text):
        text = self._apiwrapper.getJDs(text)
        return common_functions.get_info_from_jds_sts(text)

    def get_sts(self, text):
        text = self._apiwrapper.getSTs(text)
        return common_functions.get_info_from_jds_sts(text)

    def close_server(self):
        self._apiwrapper.close()
        kill_proc_tree(self.process.pid)
