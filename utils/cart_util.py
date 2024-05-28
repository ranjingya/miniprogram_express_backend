from datetime import datetime

from routes import MongoClient, redis
from utils.goods_util import GoodsUtil
from utils.token_util import TokenUtil

# 创建mongodb连接
client = MongoClient("mongodb://root:123456@localhost:27017/")
db_shops = client.shops
cart_collection = db_shops.cart


class CartUtil:

    # 通过open_id获取购物车列表
    @staticmethod
    def get_cart_list(open_id):
        cart_list = []
        for cart in cart_collection.find({'open_id': open_id}):
            cart['_id'] = str(cart['_id'])
            goods_id = cart.get('goods_id')
            if goods_id:
                goods_info = GoodsUtil.get_goods_by_id(goods_id)
                if goods_info:
                    del goods_info['create_time']
                    del goods_info['update_time']
                    del goods_info['id']
                    cart.update(goods_info)
            cart_list.append(cart)
        return cart_list

    # 添加商品到购物车
    @staticmethod
    def add_goods_to_cart(open_id, goods_id, count):
        cart = cart_collection.find_one({'open_id': open_id, 'goods_id': goods_id})
        # 如果购物车中已经有该商品，则数量增加count个
        if cart:
            print('已有该商品，数量加', count)
            count += cart.get('count', 0)  # 如果cart中没有count字段，默认0
            cart_collection.update_one({'_id': cart['_id']}, {'$set': {'count': count}})
        # 如果购物车中没有该商品，则直接添加新文档
        else:
            print('购物车没有该商品，添加新文档')
            cart_collection.insert_one({'open_id': open_id, 'goods_id': goods_id, 'count': count,
                                        'is_checked': 0, 'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        return True

    # 从购物车中删除多个商品
    @staticmethod
    def delete_goods_from_cart(open_id, goods_id):
        result = cart_collection.delete_one({'open_id': open_id, 'goods_id': goods_id})
        return result.deleted_count

    # 更新购物车中单个商品状态
    @staticmethod
    def update_goods_status(open_id, goods_id, is_checked):
        cart = cart_collection.find_one({'open_id': open_id, 'goods_id': goods_id})
        if cart:
            cart_collection.update_one({'_id': cart['_id']}, {'$set': {'is_checked': is_checked}})
            return True
        return False

    # 更新购物车中所有商品选中状态
    @staticmethod
    def update_all_goods_checked(open_id, is_checked):
        cart_collection.update_many({'open_id': open_id}, {'$set': {'is_checked': is_checked}})
        return True
