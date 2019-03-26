
# test passed

from apscheduler.schedulers.background import BackgroundScheduler
import time


def testJob():
    print('定时任务，每3s执行一次')


def heart_beat():
    print('发送心跳包 每隔1min')


if __name__ == '__main__':
    testJob()
    timer = BackgroundScheduler(timezone='MST')
    # 函数这里只写名字 没有括号！！！！！！！
    timer.add_job(testJob, trigger='interval', id='test', seconds=3)
    timer.start()

    while(True):
        heart_beat()
        time.sleep(10)



