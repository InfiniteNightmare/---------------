#!/usr/bin/env python3
# # -*- coding: gbk -*-
import requests
import json
import re

def getHTML(url, params=None):
    try:
        headers = {'user-agent':'Chrome/83'}
        r = requests.get(url, params=params, headers=headers)
        r.encoding = 'utf-8'
        r.raise_for_status
        return r.text
    except:
        return ''

def getRuid(roomid):
    try:
        url = 'https://live.bilibili.com/' + str(roomid)
        html = getHTML(url)
        uid = regex_ruid.search(html).group()
        return uid
    except:
        return AssertionError

def getMedal(roomid, ruid):
    try:
        url = 'https://api.live.bilibili.com/rankdb/v1/RoomRank/webMedalRank'
        params = {'roomid': roomid, 'ruid': ruid}
        medalinfo = getHTML(url, params=params)
        match = regex_medal.findall(medalinfo)
        if len(match) > 1:
            return match[1]
        else:
            return ''
    except:
        log.append('����' + str(roomid) + '��ȡʧ��')

medaldict = {}
log = []
regex_ruid = re.compile(r'(?<="uid":)\d*')
regex_medal = re.compile(r'(?<="medal_name":")[^"]*')
print('��������ֱ����˿ѫ����ȡ�ű�')
num1, num2 = map(int, input('��������ȡ�ķ���ŷ�Χ\n').split())
sum = num2 - num1 + 1
print('��ȡ��ʼ')
for i in range(num1, num2 + 1):
    medalname = getMedal(i, getRuid(i))
    if medalname:
        medaldict[medalname] = i
    print('����ȡ{}/{}, {:.2f}% complete\r'.format(i - num1 + 1, sum, (i - num1 + 1) * 100 / sum), end='')
print('\n��ȡ����')
with open('log.json', 'w') as logfile:
    json.dump(log, logfile, ensure_ascii=False)
with open('medal.json', 'w') as f:
    json.dump(medaldict, f, ensure_ascii=False)