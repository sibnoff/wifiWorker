import datetime
import os


class Logging:
    def __init__(self, file_name):
        self._log_file = file_name

    def write_log(self, tag_msg, text_msg):
        try:
            if os.path.isfile(self._log_file):
                fwrite = open(self._log_file, 'a')
                fwrite.writelines("{} --->>> {} --->>> {}\n".format(str(datetime.datetime.now()), tag_msg, text_msg))
                fwrite.writelines('')
            else:
                fwrite = open(self._log_file, 'w')
                fwrite.writelines("{} --->>> {} --->>> {}\n".format(str(datetime.datetime.now()), tag_msg, text_msg))
                fwrite.writelines('')
        except Exception as e:
            print(str(e))