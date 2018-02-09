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
