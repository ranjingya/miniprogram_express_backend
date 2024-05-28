from routes import request, jsonify, Blueprint
from utils.send_util import SendUtil
from utils.token_util import TokenUtil

send = Blueprint('send', __name__)


@send.route('/add', methods=['POST'])
def add_send():
    # 获取open_id
    token = request.headers.get('Authorization')
    open_id = TokenUtil.verify_token(token)['open_id']

    send_address_info = request.json.get('send_address_info')
    receive_address_info = request.json.get('receive_address_info')

    params = {
        'send_name': send_address_info.get('name'),
        'send_phone': send_address_info.get('phone'),
        'send_provinceName': send_address_info.get('provinceName'),
        'send_cityName': send_address_info.get('cityName'),
        'send_districtName': send_address_info.get('districtName'),
        'send_address': send_address_info.get('address'),
        'send_fullAddress': send_address_info.get('fullAddress'),
        'receive_name': receive_address_info.get('name'),
        'receive_phone': receive_address_info.get('phone'),
        'receive_provinceName': receive_address_info.get('provinceName'),
        'receive_cityName': receive_address_info.get('cityName'),
        'receive_districtName': receive_address_info.get('districtName'),
        'receive_address': receive_address_info.get('address'),
        'receive_fullAddress': receive_address_info.get('fullAddress'),
    }

    # 添加地址
    SendUtil.add_send(open_id, params)

    # 返回数据
    response_data = jsonify({
        'code': 200,
        'msg': 'success'
    })

    return TokenUtil.response_refresh_token(response_data)