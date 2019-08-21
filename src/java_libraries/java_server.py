import subprocess
import time
from ..common_functions import common_functions
from py4j.java_gateway import JavaGateway
import signal
import os


class JavaServer:
    def __init__(self):
        if os.name == 'nt':
            java = '\"' + common_functions.get_java_path() + '\"'
        else:
            java = 'java'
        command = java + ' -jar server.jar'
        self.process = subprocess.Popen(command, cwd=r'src\java_libraries')
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
                    self.close_server()
                    raise Exception(str(exception))

    def get_jds(self, text):
        text = self._apiwrapper.getJDs(text)
        return common_functions.get_info_from_jds_sts(text)

    def get_sts(self, text):
        text = self._apiwrapper.getSTs(text)
        return common_functions.get_info_from_jds_sts(text)

    def close_server(self):
        self._apiwrapper.close()
        os.kill(self.process.pid, signal.SIGTERM)
