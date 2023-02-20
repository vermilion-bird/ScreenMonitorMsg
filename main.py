#encoding=utf-8
from screenshot import screenshot
import socket
from datetime import datetime
import uuid
from qiniu_img import qiniu_upload
from dingding import send_dingding_message
from PIL import Image
from config import load_config
import os

config_data = load_config()


def picture_bmptopng(image_path):
    im = Image.open(image_path)
    im.save(image_path.replace('bmp', 'png'))


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)

def get_windows_mac_address():
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
    host_name = socket.gethostname()
    return mac_address, host_name

def check_permission():
    mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]

def run(expired_time):
    if expired_time <= datetime.now().strftime('%Y-%m-%d %H:%M') or expired_time == '':
        print('授权已过期,请重启程序，联系管理员重新获取授权,')
        return
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    base_dir = f'./temp/screenshot/{today_str}'
    create_dir(base_dir)
    host_name = socket.gethostname()
    uuid_str = str(uuid.uuid4())[:8]
    today_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    file_name = f'{host_name}_{today_time_str}_{uuid_str}.bmp'
    image_path = f'{base_dir}/{file_name}'
    # print('图片地址:'image_path)
    screenshot(image_path)
    picture_bmptopng(image_path)
    # 移除bmp文件
    remove_file(image_path)
    file_name = file_name.replace('bmp', 'png')
    # file_name = uuid.uuid4().hex[:16]+'.png'
    image_path = image_path.replace('bmp', 'png')
    qiniu_url = qiniu_upload(file_name, image_path)
    name = config_data.get('name', '空')
    for i in config_data.get('dingding_robot'):
        dingding_resp = send_dingding_message(qiniu_url, name,
                                              today_time_str, i.get('token'),
                                              i.get('secret'))
        if dingding_resp.get('errcode') != 0:
            print(f'钉钉机器人发送失败,错误信息: {dingding_resp}')
        else:
            print(today_time_str,' 钉钉机器人发送成功')
        # print(dingding_resp)


from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.triggers.interval import IntervalTrigger

start_time = config_data.get('date_time').get('start_time')
end_time = config_data.get('date_time').get('end_time')
interval = config_data.get('date_time').get('interval')

# start_time = datetime(2023, 2, 13, 20, 49, 0)
# end_time = datetime(2023, 2, 13, 21, 51, 0)



from permission import handle_register, get_machine_code, write_register_file,get_machine_encrypted_code,check_activate_code,de_register_file
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if __name__ == "__main__":
    while not handle_register():
        print(f'请发送 {get_machine_encrypted_code()} 到管理员,获取激活码注册')
        activate_code = input('请输入激活码：')
        if activate_code:
            # write_register_file(activate_code)
            ispass = check_activate_code(activate_code=activate_code)
            if not ispass:
                print('抱歉，激活码错误,请联系管理员')
                # exit()
            else:
                print('恭喜，激活成功')
                break
        else:
            print('激活码不能为空')
            # exit()
    
    try:
        de_machine_code, expired_time =de_register_file()
        print(f'欢迎使用，软件到期时间:{expired_time}')
        scheduler = BlockingScheduler()
        if start_time and end_time:
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            trigger = IntervalTrigger(seconds=interval, start_date=start_time, end_date=end_time)
        else:
            trigger = IntervalTrigger(seconds=interval)
        scheduler.add_job(run, args=[expired_time], trigger=trigger, next_run_time=datetime.now())
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        exit()