# _*_ coding:UTF-8 _*_
"""
__author__ = 'shede333'

执行shell命令, 默认参数：shell=True, text=True
如果需要更改当前路径,可以传入"cwd"参数;
"""

import os
import subprocess
from datetime import datetime

from swtermcolor import SWTermColor

# 默认：不打印命令信息
IS_PRINT_COMMAND = False


# env={"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"}  # 为shell添加环境变量
def add_utf8_to_env():
    """设置环境变量"LANG",""LC_ALL的为utf8"""
    # 调用shell时，添加的环境变量，解决shell-command里含有中文等特殊字符的bug
    os.putenv("LANG", "en_US.UTF-8")
    os.putenv("LC_ALL", "en_US.UTF-8")


def _call(func_obj, command, is_check=False, print_command=False, print_log=False,
          error_to_output=True, print_error=True, **kwargs):
    """
    执行shell命令

    Args:
        func_obj: Function对象
        command: shell命令
        is_check: 执行shell发生错误时,是否抛出异常,默认False
        print_command: 是否打印shell命令,默认True
        print_log: 是否打印shell命令执行结果,默认False
        error_to_output: 是否把错误信息stderr重定向到标准输出stdout,默认True
        print_error: 异常时，是否打印错误信息,默认True
    """
    try:
        error_code = 0
        if error_to_output:
            kwargs["stderr"] = subprocess.STDOUT
        if print_command:
            now_time = datetime.now().strftime("command:%Y-%m-%d %H:%M:%S")
            print("[{}] run shell: {}".format(now_time, command))
        # command_output = subprocess.check_output(command, shell=True, **kwargs)
        command_output = func_obj(command, shell=True, text=True, **kwargs)
        if command_output and print_log:
            print(command_output)

    except subprocess.CalledProcessError as e:
        error_code = e.returncode
        command_output = e.output
        now_time = datetime.now().strftime("command:%Y-%m-%d %H:%M:%S")
        error_info = "[{}]error:".format(now_time)
        error_info += "\n\t sh command: {}".format(e.cmd)
        error_info += "\n\t sh error code: {}".format(e.returncode)
        error_info += "\n\t sh error output: {}\n".format(e.output)
        if print_error:
            SWTermColor().c_red().p(error_info)
        if is_check:
            raise e

    return error_code, command_output


def call(command, **kwargs):
    """
    参考subprocess.call

    Args:
        command: shell命令
        kwargs: 其他参数
    """
    if "print_command" in kwargs:
        print_command = kwargs["print_command"]
        del kwargs["print_command"]
    else:
        print_command = IS_PRINT_COMMAND

    def sub_func(*args, **kwargs2):
        return subprocess.call(*args, **kwargs2)

    return _call(sub_func, command, print_command=print_command, **kwargs)


def check_call(command, **kwargs):
    """
    参考subprocess.check_call

    Args:
        command: shell命令
        kwargs: 其他参数
    """
    if "print_command" in kwargs:
        print_command = kwargs["print_command"]
        del kwargs["print_command"]
    else:
        print_command = IS_PRINT_COMMAND

    def sub_func(*args, **kwargs2):
        return subprocess.check_call(*args, **kwargs2)

    return _call(sub_func, command, is_check=True, print_command=print_command, **kwargs)[0]
    # return _call(command, is_check=True, **kwargs)[0]


def check_output(command, **kwargs):
    """
    参考subprocess.check_output

    Args:
        command: shell命令
        kwargs: 其他参数
    """
    if "print_command" in kwargs:
        print_command = kwargs["print_command"]
        del kwargs["print_command"]
    else:
        print_command = IS_PRINT_COMMAND

    def sub_func(*args, **kwargs2):
        return subprocess.check_output(*args, **kwargs2)

    return _call(sub_func, command, is_check=True, print_command=print_command, **kwargs)[1]
    # return _call(command, is_check=True, **kwargs)[1]
