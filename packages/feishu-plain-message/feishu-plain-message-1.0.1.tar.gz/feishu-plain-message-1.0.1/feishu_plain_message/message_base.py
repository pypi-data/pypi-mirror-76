# coding: utf-8
"""
@Author: Robby
@Module name: message_base.py
@Create date: 2020-06-06
@Function: 
"""

import json
import requests



class FeishuBase:

    def __init__(self, user_mobile: object, app_id: object, app_secret: object):
        self.tenant_access_token = self._get_tenant_access_token(app_id, app_secret)
        self.chat_id = self._get_chat_id(self.tenant_access_token)
        self.user_id = self._get_user_id(self.tenant_access_token, user_mobile)

    def _get_tenant_access_token(self, *args, **kwargs):
        raise Exception("Please Implement This Method")

    def _get_user_id(self, tenant_access_token, user_mobile):
        mobiles = user_mobile
        userurl = "https://open.feishu.cn/open-apis/user/v1/batch_get_id?mobiles=%s" % mobiles
        headers = {"Authorization": "Bearer %s" % tenant_access_token}
        request = requests.get(url=userurl, headers=headers)
        response = json.loads(request.content)['data']['mobile_users'][mobiles][0]['user_id']
        return response

    def _get_chat_id(self, tenant_access_token):
        chaturl = "https://open.feishu.cn/open-apis/chat/v4/list?page_size=20"
        headers = {"Authorization": "Bearer %s" % tenant_access_token, "Content-Type": "application/json"}
        request = requests.get(url=chaturl, headers=headers)
        response = json.loads(request.content)['data']['groups'][0]['chat_id']
        return response

    # 发送告警消息
    def send_message(self, title, content):
        send_url = "https://open.feishu.cn/open-apis/message/v4/send/"
        headers = {"Authorization": "Bearer %s" % self.tenant_access_token, "Content-Type": "application/json"}
        data = {
            "chat_id": self.chat_id,
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "un_escape": True,
                                    "text": content
                                },
                                {
                                    "tag": "at",
                                    "user_id": self.user_id

                                },
                            ],
                        ]
                    }
                }
            }
        }

        requests.post(url=send_url, headers=headers, json=data)