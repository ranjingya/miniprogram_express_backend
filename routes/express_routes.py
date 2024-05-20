from routes import app, request, jsonify, requests
from utils.token_util import TokenUtil


# 快递接口
@app.route('/get-express')
def get_express():
    express_no = request.args.get('no')
    express_type = request.args.get('type')

    params = {'no': express_no}
    if express_type:
        params['type'] = express_type

    host = 'https://wuliu.market.alicloudapi.com'
    path = '/kdi'
    appcode = '40397b8a4b06429796874563354c3bfe'
    url = host + path
    header = {"Authorization": 'APPCODE ' + appcode}
    try:
        res = requests.get(url, headers=header, params=params)
    except:
        print("URL错误")
        exit()

    http_status_code = res.status_code

    if http_status_code == 200:
        return TokenUtil.response_refresh_token(jsonify({
            'code': 200,
            'msg': 'success',
            'data': res.json()
        }))
    else:
        http_reason = res.headers['X-Ca-Error-Message']
        if http_status_code == 400 and http_reason == 'Invalid Param Location':
            print("参数错误")
        elif http_status_code == 400 and http_reason == 'Invalid AppCode':
            print("AppCode错误")
        elif http_status_code == 400 and http_reason == 'Invalid Url':
            print("请求的 Method、Path 或者环境错误")
        elif http_status_code == 403 and http_reason == 'Unauthorized':
            print("服务未被授权（或URL和Path不正确）")
        elif http_status_code == 403 and http_reason == 'Quota Exhausted':
            print("套餐包次数用完")
        elif http_status_code == 403 and http_reason == 'Api Market Subscription quota exhausted':
            print("套餐包次数用完，请续购套餐")
        elif http_status_code == 500:
            print("API网关错误")
        else:
            print("参数名错误 或 其他错误")
            print(http_status_code)
            print(http_reason)

