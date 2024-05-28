from routes import request, jsonify, Blueprint
from utils.address_util import AddrUtil
from utils.token_util import TokenUtil

address = Blueprint('address', __name__)


@address.route('/get', methods=['GET'])
def get_address_list():
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    # 从数据库中获取open_id对应的地址数据
    address_list = AddrUtil.get_addr_list(open_id)

    # 返回数据
    response_data = jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'address_list': address_list
        }
    })

    return TokenUtil.response_refresh_token(response_data)


@address.route('/add', methods=['POST'])
def add_address():
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    params = {
        'name': None,
        'phone': None,
        'provinceName': None,
        'cityName': None,
        'districtName': None,
        'address': None,
        'fullAddress': None,
        'isDefault': None
    }

    for param in params.keys():
        value = request.json.get(param)
        params[param] = '' if value is None else value

    # 添加地址
    AddrUtil.add_addr(open_id, params)

    # 返回数据
    response_data = jsonify({
        'code': 200,
        'msg': 'success'
    })

    return TokenUtil.response_refresh_token(response_data)


@address.route('/get-by-id/<id>', methods=['GET'])
def get_address_by_id(id):
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    # 从数据库中获取open_id和地址id对应的地址数据
    address_info = AddrUtil.get_addr_by_id(open_id, id)

    # 返回数据
    response_data = jsonify({
        'code': 200,
        'msg': 'success',
        'data': {
            'address_info': address_info
        }
    })

    return TokenUtil.response_refresh_token(response_data)


@address.route('/delete/<id>', methods=['GET'])
def delete_address(id):
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    if AddrUtil.delete_addr_by_id(open_id, id) > 0:
        response_data = jsonify({
            'code': 200,
            'msg': 'success'
        })
    else:
        response_data = jsonify({
            'code': 201,
            'msg': 'failed'
        })
    return TokenUtil.response_refresh_token(response_data)


@address.route('/update', methods=['POST'])
def update_address():
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    params = {
        'id': None,
        'name': None,
        'phone': None,
        'provinceName': None,
        'cityName': None,
        'districtName': None,
        'address': None,
        'fullAddress': None,
        'isDefault': None
    }

    for param in params.keys():
        value = request.json.get(param)
        params[param] = '' if value is None else value

    AddrUtil.update_addr_by_id(open_id, params)

    # 返回数据
    response_data = jsonify({
        'code': 200,
        'msg': 'success'
    })

    return TokenUtil.response_refresh_token(response_data)
