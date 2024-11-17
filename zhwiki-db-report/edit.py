# ！/usr/bin/env python
# -*-coding:Utf-8 -*-
# Time: 17 Oct 2024 11:22
# Name: edit.py
# Author: CHAU SHING SHING HAMISH

import pywikibot
import re
import subprocess
import os
import time
import datetime


def time_record(t):
    user_page = pywikibot.Page(site, "User:Hamish-bot")
    user_page_text = user_page.text
    user_page_text = re.sub(r'<!-- T8rs -->(.*)<!-- T8re -->', '<!-- T8rs -->' + t + '<!-- T8re -->', user_page_text, flags=re.M)
    user_page_text = re.sub(r'<!-- T8os -->(.*)<!-- T8oe -->', '<!-- T8os -->' + t + '<!-- T8oe -->', user_page_text, flags=re.M)
    pywikibot.showDiff(user_page.text, user_page_text)
    user_page.text = user_page_text
    user_page.save(summary = "Updating task report", minor = False)

os.environ['TZ'] = 'UTC'
print('Starting at: ' + time.asctime(time.localtime(time.time())))

dir_path = os.path.dirname(os.path.realpath(__file__))
'''
sh_script = os.path.join(dir_path, 'run.sh')
process = subprocess.Popen(['bash', sh_script, 'report'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


while True:
    output = process.stdout.readline()
    if output == b'' and process.poll() is not None:
        break
    if output:
        if "Completed report generation" in output.decode('utf-8'):
            print("Report cooked")
            break

'''
page_text = '* 生成時間：~~~~~\n'

bad_pattern = re.compile(r'\{\{(受限[制製]文件|[Bb]ad\s?image|[Rr]estricted use)\}\}')
site = pywikibot.Site('zh', 'wikipedia')
site.login()

file_path = os.path.join(dir_path, 'reports/report1.txt')
file_list = ''

with open(file_path, 'r') as infile:
    for line in infile:
        line = line.strip()
        print(line, end='\t')
        file_page = pywikibot.Page(site, 'File:'+line)
        if file_page.isRedirectPage():
            continue
        file_list += f'# [[:File:{line}]]'
        if bad_pattern.search(file_page.text):
            file_list += '（受限制文件）'
            print('R')
        file_list += '\n'
        print()

if not file_list:
    raise ValueError('No file found')
else:
    new_text = page_text + file_list
    report_page = pywikibot.Page(site, 'Wikipedia:資料庫報告/檔案描述頁')
    pywikibot.showDiff(report_page.text, new_text)
    report_page.text = new_text
    report_page.save('[[Wikipedia:机器人/申请/Hamish-bot/8|T8]]：生成本地存在檔案描述的維基共享資源文件列表')
    time_record(str((datetime.datetime.now() + datetime.timedelta(hours=8)).__format__('%d/%m/%y %H:%M')))