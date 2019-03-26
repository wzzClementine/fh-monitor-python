import requests
import logging
import time
from collections import namedtuple
from multiprocessing.pool import ThreadPool
from requests.auth import HTTPDigestAuth

# TODO These constants should be in a file
NUM_THREADS = 4
STATS_API_PREFIX = 'http://'
STATS_API_SUFFIX = '/cgi-bin/get_miner_status.cgi'
TIME_OUT = 1
USERNAME = 'root'
PASSWORD = 'root'

miner_detail = namedtuple('miner_detail', ['ip','mac','worker','time','stats'])

class Scan:
    def __init__(self, miner_list, maintain_mode = False):
        self.miner_list = miner_list
        self.results = []
        self.maintain_mode = maintain_mode

    def readSingleStats(self, ip_mac):
        miner_ip, miner_mac = ip_mac
        logging.info('Scanning {0}'.format(miner_ip))
        try:
            # send request to get miner stats
            r = requests.get(STATS_API_PREFIX + miner_ip + STATS_API_SUFFIX, auth=HTTPDigestAuth(USERNAME, PASSWORD),
                             timeout=TIME_OUT)
            if r.status_code == 200:
                # Success
                stats = r.json()
                local_time = time.asctime(time.localtime(time.time()))
                worker = stats['pools'][0]['user']

                if self.maintain_mode and worker == 'antminer_1':
                    # TODO make strong notification
                    logging.info('****** FOUND UNCONFIGURED MINER {0} ******'.format(miner_ip))

                # wrap into single tuple
                single_result = miner_detail(miner_ip,miner_mac,worker,local_time,stats)
                self.results.append(single_result)
                logging.info('Successfully got miner info from {0}'.format(miner_ip))
            else:
                logging.error('Cannot get miner info from {0}'.format(miner_ip))
        except:
            logging.error('{0} is not a miner'.format(miner_ip))

    def readAllStats(self):
        logging.info('Spawning {0} threads'.format(NUM_THREADS))
        pool = ThreadPool(NUM_THREADS)  # 线程池 threadpool 进程池 pool
        logging.info('{0} threads spawned, start scanning'.format(NUM_THREADS))
        results = pool.map(self.readSingleStats, self.miner_list)
        pool.close()
        pool.join()
        logging.info('Finished scanning {0}/{1} IP addresses'.format(len(self.results), len(self.miner_list)))
        return self.results
