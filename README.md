### Introduction
-----
gold-digger-server是一个基于Flask框架的后台服务，提供前端API服务


### Preparation
-----
依赖安装<a href="https://www.python.org/downloads/release/python-390/">python3.9</a>
libffi-devel（python3存在内置模块ctypes，提供兼容c语言的数据类型，需要linux系统安装外部函数库libffi）
bzip2-devel（python3支持bzip2压缩算法）

### Start
----
+ python运行环境
```shell
# 启动python虚拟环境
pip3 install --user pipenv

# 设置pipenv虚拟环境默认位置为根目录
export PIPENV_VENV_IN_PROJECT=1

# 设置python的环境
pipenv --python 3.9

# 使用pipenv根据安装依赖
pipenv install

# 激活虚拟环境
pipenv shell
```

+ 运行start.sh脚本启动 或者 直接启动uwsgi
```shell
uwsgi --ini uwsgi.ini
```

+ nginx conf配置

```
server {
    listen       80;

    location / {
        root /data/workspace/vue-gold-digger/dist;
        index index.html;
        add_header Cache-Control no-store;
    }

    location /static {
        alias /data/workspace/vue-gold-digger/dist/static;
    }

    location ^~/api/ {
        proxy_pass http://127.0.0.1:4506/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   html;
    }
}

```

