from routes import MongoClient, redis
from utils.token_util import TokenUtil

# 创建mongodb连接
client = MongoClient("mongodb://root:123456@localhost:27017/")
db_express = client.wx_express
user_collection = db_express.wx_user

# 创建redis连接
r = redis.Redis(host='localhost', port=6379)


class UserUtil:

    # 判断open_id是否存在redis中
    @staticmethod
    def exist_redis_open_id(token):
        token_data = TokenUtil.verify_token(token)
        if token_data is None:
            return None
        open_id = token_data.get('open_id')
        token = r.get(open_id)
        if token:
            return token
        else:
            print('此open_id不存在于Redis中')
            return None

    # 根据用户名查询用户信息
    @staticmethod
    def find_by_username(user_info):
        user_info_mongodb = user_collection.find_one({'username': user_info['username']})
        if user_info_mongodb is None:
            print('用户未注册')
            return None
        if user_info_mongodb['password'] == user_info['password']:
            old_token = r.get(user_info_mongodb['open_id'])
            TokenUtil.del_token(user_info_mongodb['open_id'])
            print('重新登录，删除token：', old_token)
            token = TokenUtil.gen_token(user_info_mongodb['open_id'])
            UserUtil.save_token(user_info_mongodb['open_id'], token)
            return token
        else:
            return False

    # 获取最大_id实现自增
    @staticmethod
    def get_max_id(collection):
        max_id_entry = collection.find_one(sort=[('_id', -1)])
        if max_id_entry is None:
            return 0
        else:
            return max_id_entry['_id']

    # 新增用户信息
    @staticmethod
    def add_user_info(user_info, open_id):
        max_id = UserUtil.get_max_id(user_collection)
        new_id = max_id + 1
        if user_info['username'] is None:
            user_info['username'] = ''
            user_info['password'] = ''
        user_collection.insert_one({
            '_id': new_id,
            'open_id': open_id,
            'username': user_info['username'],
            'password': user_info['password'],
            'phone': '',
            'avatar': ''
        })
        # 生成token存入redis
        token = TokenUtil.gen_token(open_id)
        UserUtil.save_token(open_id, token)
        return token

    @staticmethod
    def save_token(open_id, token):
        r.set(open_id, token, ex=60 * 60 * 24 * 7)
