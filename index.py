# test passed

from apscheduler.schedulers.background import BackgroundScheduler
import time
import hub


def heart_beat():
    print('发送心跳包 刷新keepalive')


if __name__ == '__main__':
    timer = BackgroundScheduler(timezone='MST')
    # 函数这里只写名字 没有括号！！！！！！！
    timer.add_job(hub.Hub('scheduler').discoverRound, trigger='interval', id='discover', hours=8)
    timer.start()

    while(True):
        heart_beat()
        time.sleep(2)



