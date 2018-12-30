'''
相关配置
'''

from datetime import timedelta
# session加密密钥
SECRET_KEY = 'ABCDEFG'
# 设置过期时间
PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

# 数据库配置
# 格式  dialect + driver: //username: password@host: port/database
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'rootzx'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'db_myself'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'\
    .format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False