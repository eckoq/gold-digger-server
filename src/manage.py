#  -*-coding:utf-8 -*-

import os
from app import create_app

# 启动模式
app = create_app(os.getenv('FLASK_CONFIG') or 'development')

if __name__ == '__main__':
    app.run()
