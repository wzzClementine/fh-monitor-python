import socket
import nmap
import logging
import platform

# Determine os type
OS = platform.system()

# NOTE: run sudo apt-get install nmap to use python-nmap
class Discover:
    def __init__(self, DNS='223.5.5.5', discover_argument='-sP', log_level=logging.INFO):
        # Aliyun DNS server 223.5.5.5
        self.DNS = DNS
        self.discover_argument = discover_argument
        logging.basicConfig(level=log_level)

    def getMyIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((self.DNS, 80))
        IP = s.getsockname()[0]
        s.close()
        logging.info('Got localhost IP = {0}'.format(IP))
        return IP

    def discoverNetwork(self):
        logging.info('Start discovering local devices')
        my_ip = self.getMyIP()
        nm_scanner = nmap.PortScanner()
        # Miners have port 22 open by default
        nm_scanner.scan(hosts=my_ip + '/24', arguments=self.discover_argument,
                        sudo=False if OS=='Windows' else True)
        stats = nm_scanner.scanstats()
        logging.info('Finished discovering, hosts alive = {0}/{1}, time used =  {2}s'.format(stats['uphosts'],
                                                                                             stats['totalhosts'],
                                                                                             stats['elapsed']))
        result = nm_scanner._scan_result['scan'].items()
        # mac address not always present in result
        hosts_list = [(ip, info['addresses']['mac']) for ip, info in result if len(info['addresses'])>1]
        '''
            (ip, info['addresses']['mac']) for ip, info in result if len(info['addresses'])>1 等价于
              for ip,info in result
                if len(info['addresses'])>1:
                    [(ip, info['addresses']['mac']),.....]
        '''
        return hosts_list

