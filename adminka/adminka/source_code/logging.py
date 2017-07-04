import datetime
import os


class Logging:
    def __init__(self, file_name):
        self._log_file = file_name

    def write_log(self, tag_msg, text_msg):
        try:
            if os.path.isfile(self._log_file):
                fwrite = open(self._log_file, 'a')
            else:
                fwrite = open(self._log_file, 'w')
            fwrite.writelines('%(date)s | %(tag)-12s | %(msg)s\n' % {"date": str(datetime.datetime.now()).split('.')[0],
                                                                     "tag": tag_msg, "msg": text_msg})
            fwrite.close()
        except Exception as e:
            print(str(e))
