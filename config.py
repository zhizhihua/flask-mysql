# 数据库的配置变量
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'flaskfirst'
USERNAME = 'root'
PASSWORD = '123'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI

SECRET_KEY = 'SPSP'

# http://www.pythondoc.com/flask-mail/   参考文档
MAIL_SERVER = 'smtp.163.com'
# 必须是数字，不能是字符串的
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = 'zhizhihua9808@163.com'
MAIL_PASSWORD = 'XQTMGAMJGKFLTXDN'
MAIL_DEFAULT_SENDER = 'zhizhihua9808@163.com'

