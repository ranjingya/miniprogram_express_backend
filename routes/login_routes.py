from routes import app, requests, request, jsonify
from utils.user_util import UserUtil


# 登录接口
@app.route('/login', methods=['POST'])
def login():
    # （已注册）用户登录，先校验redis中的token，有就放行，否则获取用户名密码与数据库校验，成功生成token存入redis
    # （未注册）用户登录，获取openId，注册信息存入数据库

    # user_info = {}
    #
    # if 'username' and 'password' in request.json:
    #     user_info = {
    #         'username': request.json.get('username'),
    #         'password': request.json.get('password'),
    #     }
    #     print(user_info)
    #
    # # 未登录，已注册，校验用户名密码，删除已存在的token，生成新token存入redis
    # is_exist_username = UserUtil.find_by_username(user_info)
    # if is_exist_username:
    #     print('用户登录：登录用户名密码正确，生成token：' + is_exist_username)
    #     return jsonify({
    #         'code': 200,
    #         'msg': '登录成功',
    #         'data': {
    #             'Authorization': is_exist_username
    #         }
    #     }), 200
    # elif is_exist_username == False:
    #     return jsonify({
    #         'code': 403,
    #         'msg': '登录失败，用户名密码错误'
    #     }), 403
    #
    # else:

    # 已登录
    if 'Authorization' in request.headers:
        is_exist_redis_openid = UserUtil.exist_redis_open_id(request.headers.get('Authorization'))
        if is_exist_redis_openid:
            return jsonify({
                'code': 200,
                'msg': '已登录'
            }), 200
        else:
            return jsonify({
                'code': 401,
                'msg': 'token不存在，请登录'
            }), 401

    app_id = 'wxc419699573b7e97f'
    secret = 'bfc17df99f502f1116baa5b7f614c3f5'
    js_code = request.json.get('code')
    print('js_code:' + js_code)
    query = f'?appid={app_id}&secret={secret}&js_code={js_code}&grant_type=authorization_code'
    res = requests.get('https://api.weixin.qq.com/sns/jscode2session' + query)

    open_id = res.json().get('openid')
    print('用户获取到的open_id：' + open_id)

    # 已注册，在redis中，返回token
    token = UserUtil.exist_redis_open_id(open_id)
    print(token)
    if token:
        return jsonify({
            'code': 200,
            'msg': '已登录',
            'data': {
                'Authorization': token
            }
        }), 200

    # 已注册，不在redis中，生成token存入redis，返回token
    token = UserUtil.find_by_open_id(open_id)
    if token:
        return jsonify({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'Authorization': token
            }
        }), 200
    else:
        # 未注册，插入数据库，生成token存入redis
        token = UserUtil.add_user_info(open_id)
        print('登陆生成token：' + token)
        return jsonify({
            'code': 200,
            'msg': '登陆成功',
            'data': {
                'Authorization': token
            }
        }), 200

# 从redis校验openId是否存在，不存在到数据库查询
# 还没有就插入到数据库
# 如果数据库有，生成token，存入redis，key为openId，value为token
# 返回token
# 如果给客户端的是openId，每一次请求都要带上openId，请求后先查redis
