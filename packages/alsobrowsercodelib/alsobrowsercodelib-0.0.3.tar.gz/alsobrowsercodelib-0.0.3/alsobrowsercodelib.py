import time
from socket import*
from email.mime.text import MIMEText
from random import*
import smtplib
import requests
import urllib.request ,re,os
import time
from re import*
import requests
from urllib.request import*
def baidubaike():
    print("\033[91m          【爱搜搜索引擎】       \033[0m")
    print("┌───────────────────────────────────┐")
    print("│                                  🔎│")
    print("└───────────────────────────────────┘")
    print("\033[96m          爱搜一下，你就知道     \033[0m")
    print('\033[3A',end='│')
    url=input('')
    html=urllib.request.urlopen("http://gop.asunc.cn/baike.html").read().decode("utf-8")
    url=html+urllib.parse.quote(url)
    html=urllib.request.urlopen(url).read().decode("utf-8")
    par = '(<meta name="description" content=")(.*?)(">)'
    try:
        os.system("clear")
        data = re.search(par,html).group(2)
        print("爱搜为您找到了以下内容:\n\033[33m",data,"\033[0m")
        input("按任意键继续...")
    except:
        print("很遗憾，爱搜没有找到。。。")
        input("按任意键继续...")
    print("\n")
    os.system("clear")
def translate():
    print("\033[91m          【爱搜翻译引擎】       \033[0m")
    print("┌───────────────────────────────────┐")
    print("│                                  🔎│")
    print("└───────────────────────────────────┘")
    print("\033[96m          爱搜一下，你就知道     \033[0m")
    print('\033[3A',end='│')
    string=input('')
    data = {'doctype': 'json','type': 'AUTO','i':string}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    result = result['translateResult'][0][0]["tgt"]
    os.system("clear")
    print("爱搜为您翻译的结果:\n\033[33m",result,"\033[0m")
    input("按任意键继续...")
    os.system("clear")
def getweather():
    province=input("省(例:广东):")
    city=input("市(例:广州):")
    data = {'doctype': 'json','type': 'AUTO','i':province}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    province = result['translateResult'][0][0]["tgt"]
    data = {'doctype': 'json','type': 'AUTO','i':city}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    city = result['translateResult'][0][0]["tgt"]
    try:
        wurl="https://tianqi.moji.com/weather/china/{}/{}".format(province,city)
        html = urllib.request.urlopen(wurl).read().decode("utf-8")
    except:
        print("毁灭性的错误!\n")
        exit()
    try:
        par = '(<meta name="description" content=")(.*?)(">)'
        data = re.search(par,html).group(2)
        data = data.replace(",","，").replace("。","，").replace("墨迹天气建议您","爱搜天气助手建议您")
        data = data.split("，")
        str1=data[3]+" "+data[4]
        str2=data[5]+" "+data[6]+"\n"
        data[3:5]=[str1]
        data[4:6]=[str2]
        os.system("clear")
        print("\n-----------------------------:\n\033[33m")
    except:
        print("毁灭性的错误!\n")
        exit()
    try:
        for i in range(len(data)):
                data[i]=data[i].lstrip()
                if i==5:
                    print(data[i],end=" ")
                elif "爱搜天气助手"in data[i]:
                    print("\n"+data[i],end=",")
                else:
                    print(data[i])
    except:
        print("毁灭性的错误!\n")
        exit()
    print("\033[0m--------------------------------\n\n")
    input("按任意键继续")
    os.system("clear")
def join_also():
    #password:ntljrawgduutddaa
    #mail:3182305655@qq.com
    SMTPServer="smtp.qq.com"
    Sender="3182305655@qq.com"
    password="ntljrawgduutddaa"
    a=randint(100000,999999)
    recver=input("您的邮箱:")
    message="您的验证码为"+str(a)+",如果不是您本人操作，请不要理他,请不要泄露给他人。"
    msg=MIMEText(message)
    msg["Subject"]="信息"
    msg["From"]="3182305655@qq.com"
    msg["To"]=recver
    server=smtplib.SMTP(SMTPServer,25)
    server.login(Sender,password)
    server.sendmail(Sender,recver,msg.as_string())
    server.quit()
    b=int(input("验证码:"))
    if a==b:
        print("验证码正确")
    else:
        print("不对哦")
def get_news():
    os.system("clear")
    now = time.strftime("%Y-%m-%d", time.localtime())
    print(now,"最新新闻资讯,转载于人民日报。\n")
    now = time.strftime("%Y%m%d", time.localtime())
    now1 = time.strftime("%Y-%m/%d", time.localtime())
    print("今日新闻资讯:")
    for i in range(1,10):
        try:
            url="http://paper.people.com.cn/rmrb/html/"+now1+"/nw.D110000renmrb_"+now+"_3-0"+str(i)+".htm"
            html=urlopen(url).read().decode("utf-8")
            html=html.replace("<br>","")
            html=html.replace("&nbsp;","")
            html=html.replace("<P>","")
            html=html.replace("</P>","")
            a1=html.index("<title>")+len("<title>")
            b1=html.index("</title>")
            a=html.index("<!--enpcontent-->")+19
            b=html.index("<!--/enpcontent-->")
            print(i,".",end="")
            while a1<b1:
                print(html[a1],end="")
                a1+=1
            print("\n")
        except:
            last=i-1
            break
    try:
        number=int(input("您需要的看点:"))
    except:
        print("毁灭性的错误")
        exit()
    if number>last or number<1:
        print("毁灭性的错误")
        exit()
    url="http://paper.people.com.cn/rmrb/html/"+now1+"/nw.D110000renmrb_"+now+"_3-0"+str(number)+".htm"
    html=urlopen(url).read().decode("utf-8")
    html=html.replace("<P>","")
    html=html.replace("</P>","")
    html=html.replace("<br>","")
    html=html.replace("&nbsp;","")
    a1=html.index("<title>")+len("<title>")
    b1=html.index("</title>")
    a=html.index("<!--enpcontent-->")+19
    b=html.index("<!--/enpcontent-->")
    os.system("clear")
    print("标题:")
    while a1<b1:
        print(html[a1],end="")
        a1+=1
    print("\033[33m")
    while a1<b1:
        print(html[a1],end="")
        a1+=1
    print("\033[0m")
    print("\n内容:")
    print("\033[44m",end="  ")
    while a<b:
        print(html[a],end="")
        a+=1
    print("\033[0m")
    input("按任意键退出...")
    exit()
