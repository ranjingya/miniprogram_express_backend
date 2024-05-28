from routes import app, request, jsonify, requests
from utils.express_util import QueryHistoryUtil
from utils.token_util import TokenUtil


# 快递接口
@app.route('/get-express')
def get_express():
    express_no = request.args.get('no')
    express_type = request.args.get('type')
    token= request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

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
    data = res.json()
    query_result = data['result']
    print('data:', data)
    print('query_result:', query_result)
    if int(data['status']) == 0:
        QueryHistoryUtil.add_query_history(open_id, query_result)
        return TokenUtil.response_refresh_token(jsonify({
            'code': 200,
            'msg': 'success',
            'data': data
        }))
    if int(data['status']) == 201:
        return TokenUtil.response_refresh_token(jsonify({
            'code': 201,
            'msg': '快递单号错误',
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


@app.route('/get-query-history', methods=['GET'])
def get_query_history():
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    # 获取参数
    page = int(request.args.get('page'))
    count = int(request.args.get('count'))
    express_id = None
    if request.args.get('express_id') is not None:
        express_id = request.args.get('express_id')
    express_com_type = None
    if request.args.get('express_com_type') is not None:
        express_com_type = request.args.get('express_com_type')
    offset = (page - 1) * count

    # 从数据库中获取分页数据、符合条件的总数
    total, query_history_list = (
        QueryHistoryUtil.get_query_history_pagination(open_id, express_id, express_com_type, offset, count))

    # 返回数据
    return jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'total': total,
            'query_history_list': query_history_list
        }
    })
