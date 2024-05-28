from routes import request, jsonify, Blueprint
from utils.cart_util import CartUtil
from utils.token_util import TokenUtil

cart = Blueprint('cart', __name__)


@cart.route('/get', methods=['GET'])
def get_cart_list():
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    # 从数据库中获取open_id对应的购物车数据
    cart_list = CartUtil.get_cart_list(open_id)
    # 返回数据
    response_data = jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'cart_list': cart_list
        }
    })

    return TokenUtil.response_refresh_token(response_data)


@cart.route('/add/<goods_id>/<count>', methods=['GET'])
def add_goods_to_cart(goods_id, count):
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    # 获取参数
    goods_id = int(goods_id)
    count = int(count)

    # 添加商品到购物车
    CartUtil.add_goods_to_cart(open_id, goods_id, count)

    # 返回数据
    response_data = jsonify({
        'code': 200,
        'msg': 'success'
    })

    return TokenUtil.response_refresh_token(response_data)


@cart.route('/delete/<goods_id>', methods=['GET'])
def delete_goods_from_cart(goods_id):
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    # 获取参数
    goods_id = int(goods_id)

    # 从购物车中删除商品
    delete_result = CartUtil.delete_goods_from_cart(open_id, goods_id)
    if delete_result == 0:
        response_data = jsonify({
            'code': 400,
            'msg': '删除失败'
        })
    else:
        response_data = jsonify({
            'code': 200,
            'msg': 'success'
        })

    return TokenUtil.response_refresh_token(response_data)


@cart.route('/update/<goods_id>/<is_checked>', methods=['GET'])
def update_goods_status(goods_id, is_checked):
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    # 获取参数
    goods_id = int(goods_id)
    is_checked = int(is_checked)

    # 更新购物车中商品状态
    CartUtil.update_goods_status(open_id, goods_id, is_checked)

    # 返回数据
    response_data = jsonify({
        'code': 200,
        'msg': 'success'
    })

    return TokenUtil.response_refresh_token(response_data)


@cart.route('/update-all/<is_checked>', methods=['GET'])
def update_all_goods_checked(is_checked):
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    # 获取参数，0取消全选，1全选
    is_checked = int(is_checked)

    # 更新购物车中商品状态
    CartUtil.update_all_goods_checked(open_id, is_checked)

    # 返回数据
    response_data = jsonify({
        'code': 200,
        'msg': 'success'
    })

    return TokenUtil.response_refresh_token(response_data)
