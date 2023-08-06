# SWRunShell

> 进一步封装了subprocess，Python调用shell命令；  
> 支持 Python2, Python3；

## 安装 Install

```

pip3 install SWRunShell

```

# 使用 
```
from swrunshell import shell_command

command = 'echo "hello, world!"'

# 参数说明：
# print_command: 是否将command 打印到终端，默认False
# print_log: 是否打印shell命令执行结果,默认False
# error_to_output: 是否把错误信息stderr重定向到标准输出stdout,默认True
# print_error: 异常时，是否打印错误信息,默认True

shell_command.call(command, print_command=False)
shell_command.check_call(command)
shell_command.check_output(command)

```
