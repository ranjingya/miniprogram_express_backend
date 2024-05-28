from routes import request, jsonify, app, g, datetime, time
from utils.user_util import UserUtil, TokenUtil


@app.before_request
def before_all_request():
    url = request.path
    print('before_all_request\n请求路径为：', url)
    # if url == '/login':
    #     return None
    token = request.headers.get('Authorization')
    if token:
        token_data = TokenUtil.verify_token(token)
        print('用户open_id: ', token_data['open_id'])
        print('token过期日期: ', datetime.fromtimestamp(token_data['exp']) )
        # 如果token在一天内过期，更新token
        if token_data['exp'] - time.time() < 60 * 60 * 24:
            TokenUtil.del_token(token_data['open_id'])
            new_token = TokenUtil.gen_token(token_data['open_id'])
            UserUtil.save_token(token_data['open_id'], new_token)
            print('token在一天内过期，更新token：', new_token)
            # 将新token存入全局g对象中
            g.new_token = new_token


@app.before_request
def before_request():
    url = request.path
    if url == '/login' or url == '/get-weather' or url.startswith('/goods'):
        return None
    token = request.headers.get('Authorization')
    if not token:
        print('token不存在于headers中')
        return jsonify({
            'code': 401,
            'msg': 'token不存在，请登录'
        }), 401

    # 检查token是否存在于Redis中
    open_id = TokenUtil.verify_token(token)['open_id']
    is_exist_redis_openid = UserUtil.exist_redis_open_id(open_id)
    if not is_exist_redis_openid:
        print('token不存在于Redis中')
        return jsonify({
            'code': 401,
            'msg': 'token不存在，请登录'
        }), 401

    # 检查token是否过期
    token_data = TokenUtil.verify_token(token)
    if token_data == 'token过期':
        print('token过期')
        return jsonify({
            'code': 401,
            'msg': 'token过期，请重新登录'
        }), 401

    # token有效，放行
    return None
