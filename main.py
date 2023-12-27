from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

VERSION = "0.0.1"
UPDATE_INFO = "支持转发聊天记录接口"

PANDORA_BACKEND_URL = os.environ.get('PANDORA_BACKEND_URL', 'http://172.17.0.1:8181')
FILTER_KEYWORD = os.environ.get('FILTER_KEYWORD', '*')

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # 转发请求到后端服务，包括 URL 参数
    full_url = f'{PANDORA_BACKEND_URL}/{path}'
    if request.query_string:
        full_url += '?' + request.query_string.decode("utf-8")
    
    print(full_url)

    resp = requests.request(
        method=request.method,
        url=full_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        allow_redirects=False
    )

    # 解析 JSON 数据
    data = resp.json()


    # 过滤掉特定的 JSON 对象
    data['items'] = [item for item in data['items'] if item['title'] != FILTER_KEYWORD]

    # 返回修改后的响应
    return jsonify(data), resp.status_code

with app.app_context():
    print("========================================")
    print("Pandora Isolate Middleware")
    print("Version: ", VERSION)
    print("Update Info: ", UPDATE_INFO)
    print("========================================")

if __name__ == '__main__':
    app.run(port=24523)
