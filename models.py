from exts import db
from datetime import datetime


# 定义邮箱验证码存储模块
class EmailcpatchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    # 获取存储到数据库的时间
    creat_time = db.Column(db.DateTime, default=datetime.now)


# 设置注册端口用户信息存储表
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    # password 的长度最少设置为200，为后期加密延长密码做准备
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    jointime = db.Column(db.DateTime, default=datetime.now)


class QuestionModel(db.Model):
    # 创建完毕记得flask orm 上传数据库
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    # password 的长度最少设置为200，为后期加密延长密码做准备
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    # 反向引用我们的usermodel里面的user的id
    # 获取到同一user发布的所有问答，可以通关questions写
    author = db.relationship('UserModel',backref = 'questions')
