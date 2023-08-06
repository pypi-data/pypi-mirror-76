"""
    @author: xuanke
    @time: 2020/8/14
    @function: 封装请求各种平台的请求API
"""
import requests
import json


class zentao(object):
    def __init__(self, url, account, password, override=False):
        self.url = url
        self.account = account
        self.password = password
        self.session_override = override
        self.base_url = 'http://erp.mxbc.net:19994'
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, "
                                      "like Gecko) Chrome/80.0.3987.162 Safari/537.36",
                        "Content-Type": "application/x-www-form-urlencoded"}

    def __str_to_json(self, content):
        json_content = json.loads(content)
        return json_content

    def get_session_id(self):
        url = '{}/zentao/api-getsessionid.json'.format(self.base_url)
        response = requests.get(url, headers=self.headers)
        return self.__str_to_json(response.json()['data'])['sessionID']

    def login_with_account_pwd(self, session_id):
        """
        使用用户名和账号登录
        """
        url = '{}/user-login.json?zentaosid={}'.format(self.base_url, session_id)
        post_data = {"account": self.account, "password": self.password}
        response = requests.post(url, headers=self.headers, data=post_data)
        print(response.json())


if __name__ == '__main__':
    zentao = zentao('','zhouliwei', 'abc.123')
    session_id = zentao.get_session_id()
    zentao.login_with_account_pwd(session_id)
