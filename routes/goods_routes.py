from routes import request, jsonify, Blueprint
from utils.goods_util import GoodsUtil
from utils.token_util import TokenUtil

goods = Blueprint('goods', __name__)


@goods.route('/get-by-type-id', methods=['GET'])
def get_goods_list_by_type_id():
    type_id = int(request.args.get('type_id'))
    goods_list = GoodsUtil.get_goods_list_by_type_id(type_id)
    response_data = jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'goods_list': goods_list
        }
    })
    return response_data


@goods.route('/get-by-id', methods=['GET'])
def get_goods_by_id():
    goods_id = int(request.args.get('goods_id'))
    goods_info = GoodsUtil.get_goods_by_id(goods_id)
    response_data = jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'goods_info': goods_info
        }
    })
    return response_data


@goods.route('/get-all-types', methods=['GET'])
def get_all_goods_types():
    goods_types = GoodsUtil.get_all_goods_types()
    response_data = jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'goods_types': goods_types
        }
    })
    return response_data