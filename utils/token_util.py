from routes import jwt, ExpiredSignatureError, os, time, random, string, redis, g, make_response

# token_secret = os.getenv('SECRET_KEY')
token_secret = 'iamthesecretkey'

r = redis.Redis(host='localhost', port=6379)


class TokenUtil:
    # 编码token
    @staticmethod
    def gen_token(open_id):
        payload = {
            'open_id': open_id,
            'iat': time.time(),  # 发行时间
            'exp': time.time() + 60 * 60 * 24 * 7,  # 过期时间 7天
            'jti': ''.join(random.choices(string.ascii_letters + string.digits, k=20))  # 随机JWT ID
        }
        return jwt.encode(payload, token_secret, algorithm='HS256')

    # 解码token
    @staticmethod
    def verify_token(token):
        try:
            return jwt.decode(token, token_secret, algorithms=['HS256'])
        except ExpiredSignatureError:
            return 'token过期'
        except:
            return None

    # 删除token
    @staticmethod
    def del_token(open_id):
        try:
            return r.delete(open_id)
        except:
            return None

    @staticmethod
    def is_within_seven_days(exp):
        if exp - time.time() > 0:
            return True

    @staticmethod
    def response_refresh_token(body):
        response = make_response(body)
        if hasattr(g, 'new_token'):
            response.headers['Authorization'] = g.new_token
            print('refresh_token:', g.new_token)
        return response
