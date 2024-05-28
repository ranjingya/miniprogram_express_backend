from datetime import datetime

from routes import MongoClient
from utils.token_util import TokenUtil

# 创建mongodb连接
client = MongoClient("mongodb://root:123456@localhost:27017/")
db_wx_express = client.wx_express
send_collection = db_wx_express.wx_send


class SendUtil:

    # 获取最大id实现自增
    @staticmethod
    def get_max_id():
        max_id_entry = send_collection.find_one(sort=[('id', -1)])
        if max_id_entry is None:
            return 0
        else:
            return max_id_entry['id']

    @staticmethod
    def add_send(open_id, params):
        print('add_send')
        send_list = {
            "open_id": open_id,
            "id": SendUtil.get_max_id() + 1,
            "send_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        send_list.update(params)
        send_collection.insert_one(send_list)
