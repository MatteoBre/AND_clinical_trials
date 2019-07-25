import psutil
import subprocess
import time
from ..common_functions import common_functions
from py4j.java_gateway import JavaGateway


def kill_proc_tree(pid):
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()


def create_run_java_server_bat():
    content = "cd src\\java_libraries\n"
    content += '\"' + common_functions.get_java_path() + '\\java.exe\" '
    content += "-Dfile.encoding=UTF-8 -classpath .\\compiled\\classes;.\\py4j-0.10.8.1.jar;.\\tc2011dist.jar JavaServer"

    f = open("run_java_server.bat", "w")
    f.write(content)
    f.close()


def create_compile_java_server_bat():
    content = 'cd src\\java_libraries\n'
    content += '\"' + common_functions.get_java_path() + '\\javac.exe\" '
    content += '-cp tc2011dist.jar;py4j-0.10.8.1.jar '
    content += 'src\\APIWrapper.java '
    content += 'src\\JavaServer.java '
    content += '-d compiled\\classes'

    f = open("compile_java_server.bat", "w")
    f.write(content)
    f.close()


class JavaServer:
    def __init__(self):
        create_compile_java_server_bat()
        create_run_java_server_bat()

        compile_server = subprocess.Popen('compile_java_server.bat')
        while compile_server.poll() is None:
            time.sleep(0.1)
        self.process = subprocess.Popen('run_java_server.bat')
        self._apiwrapper = JavaGateway().entry_point
        # Until it's not set up, wait
        while True:
            try:
                # I need to wait until it's set up
                self._apiwrapper.getJDs('')
                break
            except Exception as exception:
                if type(exception).__name__ == 'Py4JNetworkError':
                    print('not yet connected')
                    time.sleep(0.1)
                else:
                    raise Exception(str(exception))

    def get_jds(self, text):
        text = self._apiwrapper.getJDs(text)
        return common_functions.get_info_from_jds_sts(text)

    def get_sts(self, text):
        text = self._apiwrapper.getSTs(text)
        return common_functions.get_info_from_jds_sts(text)

    def close_server(self):
        self._apiwrapper.close()
        kill_proc_tree(self.process.pid)
