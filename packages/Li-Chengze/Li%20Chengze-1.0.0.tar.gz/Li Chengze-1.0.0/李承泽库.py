#制作人：钟宇轩，李承泽
#版本号码：1.0.0
#更新时间：2020/8.16
#使用请标明！否则将追究责任！


import os,time#李承泽,钟宇轩版权
import time,re#李承泽,钟宇轩版权
import sys,os#李承泽,钟宇轩版权
import urllib.request#李承泽,钟宇轩版权
from os import *#李承泽,钟宇轩版权
from socket import*#李承泽,钟宇轩版权
from random import*#李承泽,钟宇轩版权
import smtplib#李承泽,钟宇轩版权
from re import*#李承泽,钟宇轩版权
import requests#李承泽,钟宇轩版权
from urllib.request import*#李承泽,钟宇轩版权
import time#李承泽,钟宇轩版权
import datetime#李承泽,钟宇轩版权
import requests#李承泽,钟宇轩版权
import pygame#李承泽,钟宇轩版权
import random#李承泽,钟宇轩版权
from pypinyin import pinyin, lazy_pinyin, Style, load_phrases_dict#李承泽,钟宇轩版权
from xingyunlib import *#李承泽,钟宇轩版权
import xingyunlib.print_format#李承泽,钟宇轩版权
#李承泽,钟宇轩版权
def pygame_clear():#李承泽,钟宇轩版权
    print("\033[2J")#李承泽,钟宇轩版权
    print("\033[999999999A",end="")#李承泽,钟宇轩版权
def s(a):#李承泽,钟宇轩版权
    time.sleep(a)#李承泽,钟宇轩版权
def lcz_print(text):#李承泽,钟宇轩版权
    xingyunlib.print_format.print(text)#李承泽,钟宇轩版权
def help():#李承泽,钟宇轩版权
    lcz_print("1.pygame_clear用法")#李承泽,钟宇轩版权
    lcz_print("作用：清屏，用法：pygame_clear()")#李承泽,钟宇轩版权
    print("")#李承泽,钟宇轩版权
    lcz_print("2.lczlib_mp3用法")#李承泽,钟宇轩版权
    lcz_print("作用：播放MP3，用法：lichengzelib_mp3('文件名,mp3')")#李承泽,钟宇轩版权
    print("")#李承泽,钟宇轩版权
    lcz_print("3.lcz_print用法")#李承泽,钟宇轩版权
    lcz_print("作用：逐字输出，用法：lcz_print('内容')")#李承泽,钟宇轩版权
    print("")#李承泽,钟宇轩版权
    lcz_print("4.s用法（我闲的弄得）")#李承泽,钟宇轩版权
    lcz_print("作用：sleep，用法：s(sleep时间)")#李承泽,钟宇轩版权
    print("")#李承泽,钟宇轩版权
    lcz_print("5.huoyan_browser用法")#李承泽,钟宇轩版权
    lcz_print("作用：制作浏览器，用法：huoyan_browser()")
    lcz_print("6.help用法")#李承泽,钟宇轩版权
    lcz_print("作用：获取lczlib库教学，用法：help()")#李承泽,钟宇轩版权
def lczlib_mp3(music, seconds = None):#李承泽,钟宇轩版权
#李承泽,钟宇轩版权
    if not isinstance(music, str):#李承泽,钟宇轩版权
        raise Exception("参数必须为字符串")#李承泽,钟宇轩版权
#李承泽,钟宇轩版权
#李承泽,钟宇轩版权
    pygame.mixer.init()#李承泽,钟宇轩版权
    pygame.mixer.music.load(music)#李承泽,钟宇轩版权
    pygame.mixer.music.play()#李承泽,钟宇轩版权
    if seconds is not None:#李承泽,钟宇轩版权
        time.sleep(seconds)#李承泽,钟宇轩版权
        pygame.mixer.music.stop()#李承泽,钟宇轩版权
    return ""#李承泽,钟宇轩版权
#李承泽,钟宇轩版权
def huoyan_browser():#李承泽,钟宇轩版权
    while 1:#李承泽,钟宇轩版权
        print("\033[91m            【火焰搜索】       \033[0m")#李承泽,钟宇轩版权
        print("┌───────────────────────────────────┐")#李承泽,钟宇轩版权
        print("│                                  🔎│")#李承泽,钟宇轩版权
        print("└───────────────────────────────────┘")#李承泽,钟宇轩版权
        print("\033[96m            增加动画片啦~     \033[0m")#李承泽,钟宇轩版权
        print('\033[3A',end='│')#李承泽,钟宇轩版权
        url=input('')#李承泽,钟宇轩版权
        if url == "动画片":#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            time.sleep(1)#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            for i in range(24):#李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            for i in range(22):#李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            print("      /\      ")#李承泽,钟宇轩版权
            print("     /  \     ")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            for i in range(20):#李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            print("      /\      ")#李承泽,钟宇轩版权
            print("     /  \     ")#李承泽,钟宇轩版权
            print("    /    \    ")#李承泽,钟宇轩版权
            print("   /      \   ")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权#李承泽,钟宇轩版权
            for i in range(18):#李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            print("      /\      ")#李承泽,钟宇轩版权
            print("     /  \     ")#李承泽,钟宇轩版权
            print("    /    \    ")#李承泽,钟宇轩版权
            print("   /      \   ")#李承泽,钟宇轩版权
            print("  /  ====  \  ")#李承泽,钟宇轩版权
            print("  |  |  |  |  ")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            for i in range(16):#李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            print("      /\      ")#李承泽,钟宇轩版权
            print("     /  \     ")#李承泽,钟宇轩版权
            print("    /    \    ")#李承泽,钟宇轩版权
            print("   /      \   ")#李承泽,钟宇轩版权
            print("  /  ====  \  ")#李承泽,钟宇轩版权
            print("  |  |  |  |  ")#李承泽,钟宇轩版权
            print("  |  ====  |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            for i in range(14):#李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            print("      /\      ")#李承泽,钟宇轩版权
            print("     /  \     ")#李承泽,钟宇轩版权
            print("    /    \    ")#李承泽,钟宇轩版权
            print("   /      \   ")#李承泽,钟宇轩版权
            print("  /  ====  \  ")#李承泽,钟宇轩版权
            print("  |  |  |  |  ")#李承泽,钟宇轩版权
            print("  |  ====  |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  ==========  ")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            for i in range(12):#李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            print("      /\      ")#李承泽,钟宇轩版权
            print("     /  \     ")#李承泽,钟宇轩版权
            print("    /    \    ")#李承泽,钟宇轩版权
            print("   /      \   ")#李承泽,钟宇轩版权
            print("  /  ====  \  ")#李承泽,钟宇轩版权
            print("  |  |  |  |  ")#李承泽,钟宇轩版权
            print("  |  ====  |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  ==========  ")#李承泽,钟宇轩版权
            print("   \033[43m        \033[0m")#李承泽,钟宇轩版权
            print("    \033[43m      \033[0m")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            for i in range(10):#李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            print("      /\      ")#李承泽,钟宇轩版权
            print("     /  \     ")#李承泽,钟宇轩版权
            print("    /    \    ")#李承泽,钟宇轩版权
            print("   /      \   ")#李承泽,钟宇轩版权
            print("  /  ====  \  ")#李承泽,钟宇轩版权
            print("  |  |  |  |  ")#李承泽,钟宇轩版权
            print("  |  ====  |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  ==========  ")#李承泽,钟宇轩版权
            print("   \033[43m        \033[0m")#李承泽,钟宇轩版权
            print("    \033[43m      \033[0m")#李承泽,钟宇轩版权
            print("     \033[43m    \033[0m")#李承泽,钟宇轩版权
            print("      \033[43m   \033[0m")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            for i in range(8):#李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            print("      /\      ")#李承泽,钟宇轩版权
            print("     /  \     ")#李承泽,钟宇轩版权
            print("    /    \    ")#李承泽,钟宇轩版权
            print("   /      \   ")#李承泽,钟宇轩版权
            print("  /  ====  \  ")#李承泽,钟宇轩版权
            print("  |  |  |  |  ")#李承泽,钟宇轩版权
            print("  |  ====  |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  ==========  ")#李承泽,钟宇轩版权
            print("   \033[43m        \033[0m")#李承泽,钟宇轩版权
            print("    \033[43m      \033[0m")#李承泽,钟宇轩版权
            print("     \033[43m    \033[0m")#李承泽,钟宇轩版权
            print("      \033[43m  \033[0m")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            for i in range(6):#李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            print("      /\      ")#李承泽,钟宇轩版权
            print("     /  \     ")#李承泽,钟宇轩版权
            print("    /    \    ")#李承泽,钟宇轩版权
            print("   /      \   ")#李承泽,钟宇轩版权
            print("  /  ====  \  ")#李承泽,钟宇轩版权
            print("  |  |  |  |  ")#李承泽,钟宇轩版权
            print("  |  ====  |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  ==========  ")#李承泽,钟宇轩版权
            print("   \033[43m        \033[0m")#李承泽,钟宇轩版权
            print("    \033[43m      \033[0m")#李承泽,钟宇轩版权
            print("     \033[43m    \033[0m")#李承泽,钟宇轩版权
            print("      \033[43m  \033[0m")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            for i in range(4):    #李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            print("      /\      ")#李承泽,钟宇轩版权
            print("     /  \     ")#李承泽,钟宇轩版权
            print("    /    \    ")#李承泽,钟宇轩版权
            print("   /      \   ")#李承泽,钟宇轩版权
            print("  /  ====  \  ")#李承泽,钟宇轩版权
            print("  |  |  |  |  ")#李承泽,钟宇轩版权
            print("  |  ====  |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  ==========  ")#李承泽,钟宇轩版权
            print("   \033[43m        \033[0m")#李承泽,钟宇轩版权
            print("    \033[43m      \033[0m")#李承泽,钟宇轩版权
            print("     \033[43m    \033[0m")#李承泽,钟宇轩版权
            print("      \033[43m  \033[0m")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
                #李承泽,钟宇轩版权
            for i in range(2):#李承泽,钟宇轩版权
                print("")#李承泽,钟宇轩版权
            print("      /\      ")#李承泽,钟宇轩版权
            print("     /  \     ")#李承泽,钟宇轩版权
            print("    /    \    ")#李承泽,钟宇轩版权
            print("   /      \   ")#李承泽,钟宇轩版权
            print("  /  ====  \  ")#李承泽,钟宇轩版权
            print("  |  |  |  |  ")#李承泽,钟宇轩版权
            print("  |  ====  |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  ==========  ")#李承泽,钟宇轩版权
            print("   \033[43m        \033[0m")#李承泽,钟宇轩版权
            print("    \033[43m      \033[0m")#李承泽,钟宇轩版权
            print("     \033[43m    \033[0m")#李承泽,钟宇轩版权
            print("      \033[43m  \033[0m")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            print("    /    \    ")#李承泽,钟宇轩版权
            print("   /      \   ")#李承泽,钟宇轩版权
            print("  /  ====  \  ")#李承泽,钟宇轩版权
            print("  |  |  |  |  ")#李承泽,钟宇轩版权
            print("  |  ====  |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  ==========  ")#李承泽,钟宇轩版权
            print("   \033[43m        \033[0m")#李承泽,钟宇轩版权
            print("    \033[43m      \033[0m")#李承泽,钟宇轩版权
            print("     \033[43m    \033[0m")#李承泽,钟宇轩版权
            print("      \033[43m  \033[0m")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            print("  /  ====  \  ")#李承泽,钟宇轩版权
            print("  |  |  |  |  ")#李承泽,钟宇轩版权
            print("  |  ====  |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  ==========  ")#李承泽,钟宇轩版权
            print("   \033[43m        \033[0m")#李承泽,钟宇轩版权
            print("    \033[43m      \033[0m")#李承泽,钟宇轩版权
            print("     \033[43m    \033[0m")#李承泽,钟宇轩版权
            print("      \033[43m  \033[0m")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            print("  |  ====  |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  ==========  ")#李承泽,钟宇轩版权
            print("   \033[43m        \033[0m")#李承泽,钟宇轩版权
            print("    \033[43m      \033[0m")#李承泽,钟宇轩版权
            print("     \033[43m    \033[0m")#李承泽,钟宇轩版权
            print("      \033[43m  \033[0m")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            print("  |        |  ")#李承泽,钟宇轩版权
            print("  ==========  ")#李承泽,钟宇轩版权
            print("   \033[43m        \033[0m")#火焰-爱搜浏览器 ©火焰版权所有#李承泽,钟宇轩版权
            print("    \033[43m      \033[0m")#李承泽,钟宇轩版权
            print("     \033[43m    \033[0m")#李承泽,钟宇轩版权
            print("      \033[43m  \033[0m")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            print("   \033[43m        \033[0m")#李承泽,钟宇轩版权
            print("    \033[43m      \033[0m")#李承泽,钟宇轩版权
            print("     \033[43m    \033[0m")#李承泽,钟宇轩版权
            print("      \033[43m  \033[0m")#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#火焰-爱搜浏览器 ©火焰版权所有#李承泽,钟宇轩版权
            #李承泽,钟宇轩版权
            print("     \033[43m    \033[0m")#李承泽,钟宇轩版权
            print("      \033[43m  \033[0m")#火焰-爱搜浏览器 ©火焰版权所有#李承泽,钟宇轩版权
            time.sleep(0.5)#李承泽,钟宇轩版权
            pygame_clear()#李承泽,钟宇轩版权
            input("按任意键继续...")#李承泽,钟宇轩版权
        if url != "动画片": #李承泽,钟宇轩版权
            html=urllib.request.urlopen("http://gop.asunc.cn/baike.html").read().decode("utf-8")#火焰-爱搜浏览器 ©火焰版权所有#李承泽,钟宇轩版权
            url=html+urllib.parse.quote(url)#李承泽,钟宇轩版权
            html=urllib.request.urlopen(url).read().decode("utf-8")#火焰-爱搜浏览器 ©火焰版权所有
            par = '(<meta name="description" content=")(.*?)(">)' #李承泽,钟宇轩版权
            try:#李承泽,钟宇轩版权
                pygame_clear()#李承泽,钟宇轩版权
                data = re.search(par,html).group(2)#李承泽,钟宇轩版权
                print("为您找到了以下内容:\n\033[33m",data,"\033[0m")#李承泽,钟宇轩版权
                input("按任意键继续...")#火焰-爱搜浏览器 ©火焰版权所有#李承泽,钟宇轩版权
            except:#李承泽,钟宇轩版权
                print("很遗憾，没有找到。。。非常抱歉。。。")#火焰-爱搜浏览器 ©火焰版权所有#李承泽,钟宇轩版权
                input("按任意键继续...")#李承泽,钟宇轩版权
        pygame_clear()#李承泽,钟宇轩版权