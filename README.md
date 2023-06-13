海康威视IVMS任意文件上传exp

免责声明：

利用此文所提供的工具而造成的直接或间接后果和损失，均由使用者本人负责。本文所提供的工具仅用于学习，禁止用于其他！！！

使用方式：

请将webshell文件放在脚本同目录，命名为gsl.jsp，一定是gsl.jsp，如果不是，请更改py脚本的62行与88行的名字

因为是打开本地文件，所以名字必须要正确，然后运行脚本即可

单个url：

python3 hikvision-ivms-exp.py -u http://xx.xx.xx.xx

只要ip和端口，不要添加其他路径

多个url

python3 hikvision-ivms-exp.py -f file.txt

file.txt存放的是url
