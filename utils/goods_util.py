from datetime import datetime

from routes import MongoClient, redis

# 创建mongodb连接
client = MongoClient("mongodb://root:123456@localhost:27017/")
db_shops = client.shops
goods_collection = db_shops.goods
types_collection = db_shops.types

# 创建redis连接
r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


class GoodsUtil:

    @staticmethod
    def get_type_name_by_id(type_id):
        type_info = types_collection.find_one({'id': type_id})
        if type_info:
            return type_info['name']
        return None

    @staticmethod
    def get_goods_list_by_type_id(type_id):
        goods_list = []
        for goods in goods_collection.find({'type_id': type_id}):
            goods['_id'] = str(goods['_id'])
            goods['type_name'] = GoodsUtil.get_type_name_by_id(type_id)
            goods_list.append(goods)
        return goods_list

    @staticmethod
    def get_goods_by_id(goods_id):
        goods = goods_collection.find_one({'id': goods_id})
        if goods:
            goods['_id'] = str(goods['_id'])
            return goods
        return None

    @staticmethod
    def get_all_goods_types():
        types_list = []
        for types in types_collection.find():
            types['_id'] = str(types['_id'])
            types_list.append(types)
        return types_list

#     @staticmethod
#     def rename_addtime_to_createtime_in_goods():
#         client = MongoClient("mongodb://root:123456@localhost:27017/")
#         db_shops = client.shops
#         types_collection = db_shops.goods
#         types_collection.update_many({}, {'$rename': {'type_alias': 'type_id'}})
#
# GoodsUtil.rename_addtime_to_createtime_in_goods()
