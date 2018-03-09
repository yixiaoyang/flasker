### 数据迁移

1. 安装 'Flask-Migrate'

2. 将manager添加到主程序

``` python
import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
```

3. 运行 'python manager.py db init', 'python manager.py db migrate'


### 登录权限

1. 使用 'login_required'装饰器
2. 定义'login_manager.login_view'到自定义视图
3. 使用'Flask-Principal'实现角色管理

### 部署

#### wsgi
```
#-*- coding:utf-8 -*-

import sys
sys.path.insert(0, "/usr/share/webapps/flask/crm")
from crm.app import create_app

reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app('default')

if __name__ == '__main__':
    app.run()
```

#### systemd

```
yixiaoyang@[/usr/share/webapps/flask/systemd] % sudo cp ./gunicorn-flask.service /usr/lib/systemd/system/
```

#### nginx
```
server{
  listen 5002;
  #listen 5001;
  #server_name leon.org;
  location /{
         proxy_pass http://127.0.0.1:5001;
  }
}
```
