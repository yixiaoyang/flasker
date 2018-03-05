#-*- coding:utf-8 -*-

import sys
sys.path.insert(0, "/usr/share/webapps/flask/crm")
from crm.app import create_app

reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app('default')

if __name__ == '__main__':
    app.run()
