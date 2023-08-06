from emp_utils import rainbow
from emp_utils import print_as_a_list_item
from emp_utils import selection
from emp_utils import _const
from emp_utils import config_path
import os
import machine

BOOT_MODE = _const()
BOOT_MODE.WITH_NOTHING = 0
BOOT_MODE.WITH_WIFI_STARTUP = 1
BOOT_MODE.EASY_DEVELOP = 2

BOOT_MODE.WITH_WIFI_STARTUP_CODE = '''from emp_wifi import Wifi

if __name__ == '__main__':
    Wifi.connect()'''

BOOT_MODE.EASY_DEVELOP_CODE = '''from emp_wifi import Wifi
from emp_webrepl import WebREPL
from emp_utils import webrepl_pass
from emp_utils import post_ip

if __name__ == '__main__':
    print()
    print('       ---------------------------')
    print('       - Python YI MicroPython   -')
    print('       -      version 1.0.4      -')
    print('       -     by YI               -')
    print('       ---------------------------')
    print()
    Wifi.connect()
    try:
        post_ip(Wifi.ifconfig()[0][0])
    except ImportError:
        pass
    WebREPL.start(password=webrepl_pass())
    from emp_ide import *'''


def reboot():
    print(rainbow('Reboot', color='red'))
    machine.reset()


def set_boot_mode():
    print(
        print_as_a_list_item(
            0, '清除模式',
            '注意: 清除引导程序 boot.py, 这将导致程序无法启动!'))
    print(
        print_as_a_list_item(
            1, 'WiFi模式',
            '此选项适合稳定程序使用！'))
    print(
        print_as_a_list_item(
            2, '开发者模式',
            '启动连接WIFI热点，并开启WebREPL开发模式'
        ))

    mode = selection('请选择模式 [0-2]: ', 2)

    with open('boot.py', 'w') as f:
        if mode == BOOT_MODE.WITH_NOTHING:
            boot_code = ''
            f.write(boot_code)
            print(rainbow('已设置为清除模式', color='green'))
        elif mode == BOOT_MODE.WITH_WIFI_STARTUP:
            boot_code = BOOT_MODE.WITH_WIFI_STARTUP_CODE
            f.write(boot_code)
            print(rainbow('已设置为WiFi模式', color='green'))

        elif mode == BOOT_MODE.EASY_DEVELOP:
            config_path()
            if not 'webrepl.pass' in os.listdir('config'):
                with open('config/webrepl.pass', 'w') as c:
                    c.write('123456')
            boot_code = BOOT_MODE.EASY_DEVELOP_CODE
            f.write(boot_code)
            print(rainbow('已设置为开发者模式', color='green'))

    reboot()


def set_web_repl():
    pw = input(rainbow('请输入新的WebREPL密码：', color='blue'))
    config_path()
    with open('config/webrepl.pass', 'w') as c:
        c.write(pw)
    print(rainbow('已重新设置WebREPL密码，重启之后可用！！！', color='green'))
