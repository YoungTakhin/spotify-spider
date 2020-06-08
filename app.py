import json
from flask import request, Flask

from spider import spider

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/spotify', methods=['POST'])
def spotify_spider():
    """
    充值脚本控制器
    :return: {
        0: 浏览器驱动加载失败或网页无法打开
        1: 成功
        10: 密钥不正确或已经被使用
        11: Link已满
        100: 账号或密码错误
        101: 国家更改失败
        110: 已经是会员了
        111: 服务器无法访问网页
        1000: 链接用完了
    }
    """
    username = json.loads(request.data)['username']
    password = json.loads(request.data)['password']
    link = json.loads(request.data)['link']

    s = spider.Spider()

    code = s.get_website()
    if code == "1":
        code = s.login(username, password)
        if code == "1":
            code = s.check_country()
            if code == "1":
                code = s.open_other_link(link)
    s.close()
    return code


if __name__ == '__main__':
    app.run()
