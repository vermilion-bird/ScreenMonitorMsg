from screenshot import screenshot
import socket
from datetime import datetime
import uuid
from qiniu_img import qiniu_upload
from dingding import send_dingding_message
from PIL import Image


def picture_bmptopng(image_path):
    im = Image.open(image_path)
    im.save(image_path.replace('bmp', 'png'))


def create_dir(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path)


def run():
    today_str = datetime.now().strftime("%Y-%m-%d")
    base_dir = f'./temp/screenshot/{today_str}'
    create_dir(base_dir)
    host_name = socket.gethostname()
    uuid_str = str(uuid.uuid4())[:8]
    today_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f'{host_name}_{today_time_str}_{uuid_str}.bmp'
    image_path = f'{base_dir}/{file_name}'
    print(image_path)
    screenshot(image_path)
    picture_bmptopng(image_path)
    file_name = file_name.replace('bmp', 'png')
    # file_name = uuid.uuid4().hex[:16]+'.png'
    image_path = image_path.replace('bmp', 'png')
    qiniu_url = qiniu_upload(file_name, image_path)
    print(qiniu_url)
    dingding_resp = send_dingding_message(qiniu_url, host_name, today_time_str)
    print(dingding_resp)


from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

def my_task():
    print("Task executed!")
    run()

if __name__ == "__main__":
    try:
        scheduler = BlockingScheduler()
        # scheduler.add_job(my_task, 'interval', seconds=60)
        # scheduler.start()
        # scheduler = BackgroundScheduler()
        trigger = IntervalTrigger(seconds=60)
        scheduler.add_job(my_task, trigger)
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        exit()



        
    import pytz
    
    print(len(pytz.all_timezones))
    for timezone in pytz.all_timezones:
        print(timezone)