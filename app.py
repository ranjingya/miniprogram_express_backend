from routes import app
from utils import ip_util

if __name__ == '__main__':
    app.run(host=ip_util.get_local_ip(), debug=True)
