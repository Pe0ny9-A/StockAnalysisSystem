"""
股票系统 - 应用入口文件
"""
import os
from app import create_app, socketio
from app.config import config

# 获取配置类型
config_name = os.environ.get('FLASK_CONFIG') or 'default'
app = create_app(config[config_name])

if __name__ == '__main__':
    # 使用socketio运行应用，而非普通的app.run()
    socketio.run(app, host='0.0.0.0', port=5000, debug=app.config['DEBUG']) 