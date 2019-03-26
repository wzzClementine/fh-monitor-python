
import boto3
import config
import logging
import time

IDENTITY = 'dynamodb'
REGION_NAME = config.dynamodb_config['region_name']
ACCESS_KEY = config.dynamodb_config['aws_access_key_id']
SECRET_KEY = config.dynamodb_config['aws_secret_access_key']
logger = logging.getLogger()  # initialize logging class
logger.setLevel(logging.INFO)

class dbOperations:
    def __init__(self, ip, location):
        self.ip = ip
        self.location = location
        self.client = boto3.client(IDENTITY,
                              region_name=REGION_NAME, aws_access_key_id=ACCESS_KEY,
                              aws_secret_access_key=SECRET_KEY)

    # test passed
    def get_miner(self):
        result = self.client.get_item(
            TableName='miner',
            Key={
                "Location": {
                    'S': str(self.location)
                },
                "ID": {
                    'S': str(self.ip)
                }
            }
        )
        return result['Item']  # result为字典格式

    # test passed
    def update_count(self):
        item = self.get_miner()
        count = int(item['count']['N'])
        count = count + 1
        count0 = {
            'N': str(count)
        }
        try:
            self.client.update_item(
                TableName='miner',
                Key={
                    "Location": {
                        'S': str(self.location)
                    },
                    "ID": {
                        'S': str(self.ip)
                    }
                },
                ExpressionAttributeNames={
                    "#count": "count"
                },
                ExpressionAttributeValues={
                    ":count": count0
                },
                UpdateExpression="SET #count = :count",
                ReturnValues="UPDATED_NEW"
            )
            logger.info('***COUNT*** updated.')
        except:
            logger.error('dynamodb update COUNT error!')

    # test passed
    def update_time(self):
        local_time = time.localtime(time.time())
        current_day = local_time[2]
        current_hour = local_time[3]
        try:
            self.client.update_item(
                TableName='miner',
                Key={
                    "Location": {
                        'S': str(self.location)
                    },
                    "ID": {
                        'S': str(self.ip)
                    }
                },
                ExpressionAttributeNames={
                    "#time": "firstTime"
                },
                ExpressionAttributeValues={
                    ":time": {
                        "M": {
                            "hour": {
                                "N": str(current_hour)
                            },
                            "day": {
                                "N": str(current_day)
                            }
                        }
                    }
                },
                UpdateExpression="SET #time = :time",
                ReturnValues="UPDATED_NEW"
            )
            logger.info('***TIME*** updated.')
        except:
            logger.error('dynamodb update TIME error!')

    # test passed
    def close(self):
        reboot = {
            'N': "0"
        }
        try:
            self.client.update_item(
                TableName='miner',
                Key={
                    "Location": {
                        'S': str(self.location)
                    },
                    "ID": {
                        'S': str(self.ip)
                    }
                },
                ExpressionAttributeNames={
                    "#reboot": "rebootingFlag"
                },
                ExpressionAttributeValues={
                    ":reboot": reboot
                },
                UpdateExpression="SET #reboot= :reboot",
                ReturnValues="UPDATED_NEW"
            )
            logger.info('***rebooting operation was closed.***')
        except:
            logger.error('dynamodb ClOSE error!')

    def open(self):
        pass
