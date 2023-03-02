import requests
import json
import logging
import time


user_name_list = [
    ' '
]

log = ''

def submit(user_name, is_pk):
    global log
    headers = {
        'Host': 'iptv.hbtv.com.cn',
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.7(0x13070010) Safari/605.1.15 NetType/WIFI',
        'accept-language': 'zh-CN,zh-Hans;q=0.9',
        'referer': 'https://iptv.hbtv.com.cn/app/wx-answer/',
    }
    requests_url = f'https://iptv.hbtv.com.cn/wxcms3/iptv-answering/api/v1/questionnaire/{user_name}'

    if not is_pk:
        params = {'type': 'daily'}
    else:
        params = {'type': 'pk'}

    response = requests.get(
        requests_url,
        params=params,
        headers=headers,
    )

    msg = response.json()

    if msg['code'] != 200:
        log = log + user_name + 'ERROR ' + msg['message'] + '\n'
        # print(user_name + 'ERROR ' + msg['message'])
    else:
        submit_data = []
        for question in msg['data']:
            answer = {"groupId": question['groupId'],
                      "questionId": question['id'], "answer": question['answer']}
            submit_data.append(answer)
        if not is_pk:
            submit_url = f'https://iptv.hbtv.com.cn/wxcms3/iptv-answering/api/v1/questionnaire/submit/{user_name}'
        else:
            submit_url = f'https://iptv.hbtv.com.cn/wxcms3/iptv-answering/api/v1/questionnaire/submit-pk/{user_name}'
        response = requests.put(
            submit_url,
            headers=headers,
            json=submit_data,
        )
        msg = response.json()
        if msg['code'] != 200:
            log = log + user_name + 'ERROR ' + msg['message'] + '\n'
            # print(user_name + 'ERROR ' + msg['message'])
        else:
            log = log + user_name + msg['message'] + '\n'
            # print(user_name + msg['message'])

def send_wechat(msg):
    title = '答题_log'
    token = ' '
    content = msg
    url = f"https://www.pushplus.plus/send?token={token}&title={title}&content={content}"
    r = requests.get(url=url)

if __name__ == "__main__":
    for name in user_name_list:
        submit(name, True)
        time.sleep(2)
        submit(name, False)
    print(log)
    send_wechat(log)

