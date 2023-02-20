import wmi
import hashlib
import base64
import hashlib
from pyDes import *
import os
from dingding import send_dingding_text_message
import socket

register_file_path = "./register.bin"
# encrypted_file="./start.bin"

def get_machine_code():
    m_wmi = wmi.WMI()
    hostname = m_wmi.Win32_ComputerSystem()[0].Name
    cpu_info = m_wmi.Win32_Processor()
    if len(cpu_info) > 0:
        cpu_serial_number = cpu_info[0].ProcessorId
    for network in m_wmi.Win32_NetworkAdapterConfiguration():
        mac_address = network.MacAddress
    disk_info = m_wmi.Win32_PhysicalMedia()
    if len(disk_info) > 0:
        disk_serial_number = disk_info[0].SerialNumber.strip()
    board_info = m_wmi.Win32_BaseBoard()
    if len(board_info) > 0:
        board_id = board_info[0].SerialNumber.strip().strip('.')
    machine_code = f'{hostname}{cpu_serial_number}{mac_address}{disk_serial_number}{board_id}'
    return machine_code


def get_machine_encrypted_code():
    machine_code = get_machine_code()
    combine_byte = machine_code.encode("utf-8")
    # 进行 MD5 编码
    machine_code = hashlib.md5(combine_byte).hexdigest()
    return machine_code.upper()


def Encrypted(code):
    # 使用 DES-CBC加密算法加密机器码
    Des_key = "zmyzmyzm"  #自定义 Key，需八位
    Des_IV = "\x11\2\x2a\3\1\x27\2\0"  # 自定IV向量
    k = des(Des_key, CBC, Des_IV, pad=None, padmode=PAD_PKCS5)
    EncryptStr = k.encrypt(code)
    # 加密结果转 base64 编码
    base64_code = base64.b32encode(EncryptStr)
    # 编码结果使用 MD5 加密
    md5_code = hashlib.md5(base64_code).hexdigest().upper()
    return md5_code

from datetime import datetime,timedelta
def read_permission_conf(pre_type='time'):
    """读取授权的时间，钉钉机器人的 token 和 secret
    pre_type: time, dingding
    """
    # kit.bin下面的内容
    D,H,M=30,0,0
    token,secret='',''
    if os.path.exists('kit.bin'):
        with open('kit.bin', 'r') as f:
            for i in f.readlines():
                if i.split('_')[0]=='#D/H/M':
                    D,H,M=i.split('_')[-1].split('/')
                    D,H,M=int(D),int(H),int(M)
                if i.split('_')[0]=='#base64':
                    _,key,encrypted=i.split('_')
                    token,secret=aes_decrypted(encrypted,key).split('_')
                    # print(token,secret)
    if pre_type=='time':
        return D,H,M
    elif pre_type=='dingding':
        return token,secret
    
def get_key_expired_time():
    D,H,M = read_permission_conf('time')
    timedelta_time = timedelta(days=D, hours=H, minutes=M)
    expired_time = datetime.now()+timedelta_time
    return expired_time.strftime('%Y-%m-%d %H:%M')


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

# def read_encrypted_file():
#     file_path=encrypted_file
#     with open(file_path, "r") as f:
#         return f.read()


def check_activate_code(activate_code):
    try:
        key, encrypted_code = activate_code.split('_')
        de_machine_code =aes_decrypted(encrypted_code, key)
        code ,expired_time=de_machine_code.split("_")
        machine_code = get_machine_encrypted_code()
        # 自己定义 Encrypted 函数进行加密处理
        encrypt_code = Encrypted(machine_code.encode("utf-8"))
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if code == encrypt_code and now_time<=expired_time:
            write_register_file(activate_code)
            return True
        else:
            return False
    except Exception as e:
        # print(str(e))
        return False
    
def login_log(text):
    token, secret = read_permission_conf('dingding')
    send_dingding_text_message(text, token, secret)

def handle_register():
    machine_code = get_machine_encrypted_code()
    # 自己定义 Encrypted 函数进行加密处理
    encrypt_code = Encrypted(machine_code.encode("utf-8"))
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    expired_time = get_key_expired_time()
    key, encrypt_code_encrypt_code = aes_encrypted(encrypt_code+'_'+expired_time)
    activate_code = f'{key}_{encrypt_code_encrypt_code}'
    # print('加密后的机器码:', encrypt_code)
    host_name = socket.gethostname()
    text = '机器码: ' + machine_code + '\n' + '激活码: ' + activate_code + '\n' + '主机名：' + host_name + '\n'
    if  os.path.exists(register_file_path):
        try:
            de_machine_code, expired_time =de_register_file()
            if encrypt_code == de_machine_code and now_time<=expired_time:
                return True
            else:
                remove_file(register_file_path)
                login_log(text)
                return False
        except Exception as e:
            remove_file(register_file_path)
            login_log(text)
            return False
    else:
        login_log(text)
        return False
    
    # 获取机器码
    machine_code = get_machine_encrypted_code()
    # print('唯一标识: ', machine_code)
    # 自己定义 Encrypted 函数进行加密处理
    encrypt_code = Encrypted(machine_code.encode("utf-8"))
    if not os.path.exists(register_file_path):
        expired_time = get_key_expired_time()
        print(44,expired_time)
    else:
        _, expired_time =de_register_file()
    # '2023-01-01 11:10:00'
    # get_key_expired_time()
    key, encrypt_code_encrypt_code = aes_encrypted(encrypt_code+'_'+expired_time)
    print(11,key+'_'+encrypt_code_encrypt_code)
    # write_register_file(f'{key}_{encrypt_code_encrypt_code}')
    # write_encrypted_file(f'{key}_{encrypt_code_encrypt_code}')
    # 激活码
    # activate_code = f'{encrypt_code_encrypt_code[:16]}{key.upper()[:16]}'
    activate_code = f'{key}_{encrypt_code_encrypt_code}'
    # print('加密后的机器码:', encrypt_code)
    host_name = socket.gethostname()
    text = '机器码: ' + machine_code + '\n' + '激活码: ' + activate_code + '\n' + '主机名：' + host_name + '\n'
    # token = '96030e0b02738e53f06f094b9f01517cad65870594a4d0751c0a2dfdc45a9f66'
    # secret = 'SEC7d26ec49db125d692413521f88a4fe99ebac1d6e321a40a298dc6d54499084d2'
    token, secret = read_permission_conf('dingding')
    send_dingding_text_message(text, token, secret)
    # 读取本地的授权文件
    if os.path.exists(register_file_path):
        # with open(register_file_path, "r") as f:
        #     key_code = f.read()
        #     key, encrypted_code = key_code.split('_')
        #     de_machine_code =aes_decrypted(key, encrypted_code)
        #     code ,expired_time=de_machine_code.split("_")
        #     # 如果机器码经过加密后的值，等于授权码的值，则验证通过，否则验证失败
        #     if machine_code==code and now_time<=expired_time:
        #         return True
        #     else:
        #         # remove_file(encrypted_file)
        #         return False
        de_machine_code, expired_time = de_register_file()
        if encrypt_code==de_machine_code and now_time<=expired_time:
                return True
        else:
                # remove_file(encrypted_file)
                return False
    else:
        # remove_file(encrypted_file)
        return False

def de_register_file():
    # 读取本地的授权文件
    if os.path.exists(register_file_path):
        with open(register_file_path, "r") as f:
            key_code = f.read()
            key, encrypted_code = key_code.split('_')
            de_machine_code =aes_decrypted(encrypted_code, key)
            code ,expired_time=de_machine_code.split("_")
            return code,expired_time
        
def write_register_file(activate_code):
    with open(register_file_path, "w") as f:
        f.write(activate_code)

# def write_encrypted_file(code):
#     file_path=encrypted_file
#     with open(file_path, "w") as f:
#         f.write(code)

from cryptography.fernet import Fernet
import base64

def aes_encrypted(data):
    # 生成密钥
    # key = base64.b64decode('V0FaRDllb0pldVpzcVVUaEtSVmpvWlEydUNpeFZ2dFVsU2ZCQW5BMVlnOD0=') 
    key = Fernet.generate_key()
    # 使用密钥创建Fernet对象
    fernet = Fernet(key)
    # 原始数据
    data = data.encode()
    # 加密数据
    encrypted = fernet.encrypt(data)
    # 将密钥和加密后的数据以base64编码的形式打印出来
    # print("Key:", base64.urlsafe_b64encode(key).decode())
    # print("Encrypted data:", base64.urlsafe_b64encode(encrypted).decode())
    return base64.urlsafe_b64encode(key).decode(), base64.urlsafe_b64encode(encrypted).decode()

def aes_decrypted(encrypted, key):
    key = base64.b64decode(key)
    fernet = Fernet(key)
    encrypted = base64.b64decode(encrypted)
    # 解密数据
    decrypted = fernet.decrypt(encrypted)
    # 打印解密后的数据
    # print("Decrypted data:", decrypted.decode())
    return decrypted.decode()

if __name__ == '__main__':
    pass
    # token = '96030e0b02738e53f06f094b9f01517cad65870594a4d0751c0a2dfdc45a9f66'
    # secret = 'SEC7d26ec49db125d692413521f88a4fe99ebac1d6e321a40a298dc6d54499084d2'
    # aes_encrypted(f'{token}_{secret}')
    # key,encrypted=aes_encrypted('gghhasdhs_jakhdj')
    # aes_decrypted(encrypted,key)
    # read_permission()
    # print(get_key_expired_time())