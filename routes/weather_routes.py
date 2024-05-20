from datetime import datetime

from routes import app, jsonify, requests
from utils.token_util import TokenUtil


# 天气接口
@app.route('/get-weather')
def get_weather():
    location = "119.36286268564223,32.11114462781771"
    token = "miHSQu7jCIFpp1VV"
    url = "https://api.caiyunapp.com/v2.6/" + token + "/" + location + "/realtime"
    skycon_dict = {
        'CLEAR_DAY': '晴（白天）',
        'CLEAR_NIGHT': '晴（夜间）',
        'PARTLY_CLOUDY_DAY': '多云（白天）',
        'PARTLY_CLOUDY_NIGHT': '多云（夜间）',
        'CLOUDY': '阴',
        'LIGHT_HAZE': '轻度雾霾',
        'MODERATE_HAZE': '中度雾霾',
        'HEAVY_HAZE': '重度雾霾',
        'LIGHT_RAIN': '小雨',
        'MODERATE_RAIN': '中雨',
        'HEAVY_RAIN': '大雨',
        'STORM_RAIN': '暴雨',
        'FOG': '雾',
        'LIGHT_SNOW': '小雪',
        'MODERATE_SNOW': '中雪',
        'HEAVY_SNOW': '大雪',
        'STORM_SNOW': '暴雪',
        'DUST': '浮尘',
        'SAND': '沙尘',
        'WIND': '大风',
    }

    response = requests.get(url).json()
    weather_result = {
        'code': 200,
        'msg': 'success',
        'data': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'temperature': str(response['result']['realtime']['temperature']) + '°C',
            'skycon': skycon_dict[response['result']['realtime']['skycon']],
        }
    }
    return TokenUtil.response_refresh_token(jsonify(weather_result))
