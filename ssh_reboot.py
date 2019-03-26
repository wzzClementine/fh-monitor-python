
import paramiko
import config
import logging
import operationDB
import conditions


PORT = config.ssh_config['port']
USER_NAME = config.ssh_config['username']
PASSWORD = config.ssh_config['password']

COMMAND = config.ssh_config['reboot_command']

logger = logging.getLogger()  # initialize logging class
logger.setLevel(logging.INFO)


class sshAndReboot:
    def __init__(self, ip, location):
        self.location = location
        self.ip = ip
        self.ssh_client = paramiko.SSHClient()
        self.conditions = conditions.conditions(self.ip, self.location)
        self.operations = operationDB.dbOperations(self.ip, self.location)

    def ssh_reboot(self):
        # test passed
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=self.ip,
                                port=PORT, username=USER_NAME,
                                password=PASSWORD)
        stdin, stdout, stderr = self.ssh_client.exec_command(COMMAND)
        logger.info(self.ip + '' + 'reboot sucessfully：' + stdout.read())
        self.ssh_client.close()

    def judgements(self):
        try:
            # 判断是否满足重启条件  test passed
            reboot_flag = self.conditions.reboot_flag()
            if reboot_flag == 1:
                count1 = self.conditions.count1()
                if count1 == 1:  # 可以重启
                    time2 = self.conditions.time2()
                    if time2 == 1:
                        self.ssh_reboot()
                        self.operations.update_count()
                    else:
                        logger.info('time will be updated...')
                        self.operations.update_time()
                        self.ssh_reboot()
                        self.operations.update_count()
                else:
                    logger.info('reboot failed ***count >= 5***')
                    self.operations.close()
            else:
                logger.info('reboot failed ***rebootingFlag == 0***')
        except:
            logger.error(self.ip + '' + 'ssh connection error.')








