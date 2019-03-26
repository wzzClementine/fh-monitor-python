
import config
import discover
import iot
import scan
import urllib
import logging
from config import farmLocation
import json

url = 'http://www.baidu.com'
logger = logging.getLogger()  # initialize logging class
logger.setLevel(logging.INFO)


class Hub:
    def __init__(self, caller):
        self.caller = caller

    def discoverRound(self):
        try:
            status = urllib.request.urlopen(url).code
            if status == 200:
                logger.info('***Starting Scanning Round***')
                #  获取所有矿机的IP和MAC地址
                miner_list = discover.Discover().discoverNetwork()  # [(ip, mac)]
                #  获取矿机运行数据
                s = scan.Scan(miner_list=miner_list, maintain_mode=True)
                results = s.readAllStats()
                for result in results:
                    reslist = {
                        'general': {
                            "location": farmLocation,
                            "ip": result.ip,
                            "mac": result.mac,
                            "worker": result.worker,
                            "timestamp": result.time
                        },
                        'pools': result.stats[u'pools']
                    }
                    if self.caller == 'scheduler':
                        iot.publish_scheduled_miner_details(json.dumps(reslist))
        except:
            logger.error('Cannot connect to Internet')








