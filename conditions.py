
import operationDB
import time
import logging

logger = logging.getLogger()  # initialize logging class
logger.setLevel(logging.INFO)

class conditions:
    def __init__(self, ip, location):
        self.location = location
        self.ip = ip
        self.operation = operationDB.dbOperations(self.ip, self.location)
        self.item = self.operation.get_miner()

    # TEST PASSED
    def reboot_flag(self):
        reboot_f = int(self.item['rebootingFlag']['N'])
        if reboot_f == 1:
            logger.info('SUCCESS ***opening***')
            return 1
        else:
            logger.info('FAILED ***closed***')
            return 0

    # TEST PASSED
    def count1(self):
        count = int(self.item['count']['N'])
        if count <= 5:
            logger.info('SUCCESS *** count <= 5 ***')
            return 1
        else:
            logger.info('FAILED *** count > 5***')
            return 0

    # TEST PASSED
    def time2(self):
        day = int(self.item['firstTime']['M']['day']['N'])
        local_time = time.localtime(time.time())
        current_day = local_time[2]
        if day == current_day:
            logger.info('SUCCESS *** time <= 24 ***')
            return 1
        else:
            logger.info('FAILED *** time > 24 ***')
            return 0







