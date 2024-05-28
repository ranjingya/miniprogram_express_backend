from datetime import datetime

from routes import MongoClient, redis
from utils.goods_util import GoodsUtil
from utils.token_util import TokenUtil

# 创建mongodb连接
client = MongoClient("mongodb://root:123456@localhost:27017/")
db_express = client.wx_express
address_collection = db_express.wx_address


class AddrUtil:

    # 地址列表
    @staticmethod
    def get_addr_list(open_id):
        addr_list = []
        for addr in address_collection.find({'open_id': open_id}):
            addr['_id'] = str(addr['_id'])
            addr_list.append(addr)
        return addr_list

    # 根据id获取地址详情
    @staticmethod
    def get_addr_by_id(open_id, addr_id):
        addr = address_collection.find_one({'open_id': open_id,
                                            'id': addr_id})
        if addr:
            addr['_id'] = str(addr['_id'])
            return addr
        return None

    # 根据地址id删除地址
    @staticmethod
    def delete_addr_by_id(open_id, addr_id):
        result = address_collection.delete_one({'open_id': open_id, 'id': int(addr_id)})
        return result.deleted_count

    # 根据地址id更新地址
    @staticmethod
    def update_addr_by_id(open_id, params):
        result = address_collection.update_one({'open_id': open_id, 'id': params['id']},
                                               {'$set': {
                                                   'name': params['name'],
                                                   'phone': params['phone'],
                                                   'provinceName': params['provinceName'],
                                                   'cityName': params['cityName'],
                                                   'districtName': params['districtName'],
                                                   'address': params['address'],
                                                   'fullAddress': params['fullAddress'],
                                                   'isDefault': params['isDefault'],
                                                   'updateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                               }})
        return result.modified_count

    # 获取最大id实现自增
    @staticmethod
    def get_max_id():
        max_id_entry = address_collection.find_one(sort=[('id', -1)])
        if max_id_entry is None:
            return 0
        else:
            return max_id_entry['id']

    @staticmethod
    def add_addr(open_id, params):
        new_id = AddrUtil.get_max_id() + 1  # 获取当前的最大id，并加1
        address_collection.insert_one({
            'id': new_id,
            'open_id': open_id,
            'name': params['name'],
            'phone': params['phone'],
            'provinceName': params['provinceName'],
            'cityName': params['cityName'],
            'districtName': params['districtName'],
            'address': params['address'],
            'fullAddress': params['fullAddress'],
            'isDefault': params['isDefault'],
            'createTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updateTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return True
