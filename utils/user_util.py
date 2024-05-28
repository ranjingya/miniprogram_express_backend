from routes import MongoClient, redis
from utils.token_util import TokenUtil

# 创建mongodb连接
client = MongoClient("mongodb://root:123456@localhost:27017/")
db_express = client.wx_express
user_collection = db_express.wx_user

# 创建redis连接
r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


class UserUtil:

    # 判断open_id是否存在redis中
    @staticmethod
    def exist_redis_open_id(open_id):
        token = r.get(open_id)
        if token:
            return token
        else:
            print('此open_id不存在于Redis中')
            return None

    # 根据open_id查询用户信息
    @staticmethod
    def find_by_open_id(open_id):
        user_info_mongodb = user_collection.find_one({'open_id': open_id})
        if user_info_mongodb is None:
            print('用户未注册')
            return None
        token = TokenUtil.gen_token(user_info_mongodb['open_id'])
        UserUtil.save_token(user_info_mongodb['open_id'], token)
        return token

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
    def add_user_info(open_id):
        max_id = UserUtil.get_max_id(user_collection)
        new_id = max_id + 1
        user_collection.insert_one({
            '_id': new_id,
            'open_id': open_id,
            'username': '',
            'password': '',
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
