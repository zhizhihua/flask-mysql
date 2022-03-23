# redirect 重定向静态网页，user.py是视图函数
from flask import (Blueprint,
                   render_template,
                   request, redirect, url_for, session, jsonify,flash)
from exts import mail, db
from flask_mail import Message
from models import EmailcpatchaModel, UserModel
import string
import random
from datetime import datetime
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

# 对应的访问的url的前缀   http://127.0.0.1:5000/user
bp = Blueprint('user', __name__, url_prefix='/user')


# 设置在user蓝图下的login登录界面
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                # 获取表user 的id
                session['user_id'] = user.id
                return redirect('/')
            else:
                flash('邮箱和密码不匹配')
                return redirect(url_for('user.login'))
        else:
            flash('邮箱或者密码格式错误')
            return redirect(url_for('user.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 获取前端页面register.html文件中的form表单传入的内容
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            # 在form.py设置了对应的验证码的举措，这部分的captcha验证可以省略
            # captcha = form.captcha.data
            username = form.username.data
            password = form.password.data
            # 获取哈希密码转化后的密码
            hash_password = generate_password_hash(password)
            user = UserModel(email=email, username=username, password=hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.register'))


@bp.route('/mail')
def sender():
    message = Message(
        subject='邮箱测试',
        recipients=['zhizhihua9808@163.com', '919006684@qq.com', 'sj13652388474@outlook.com'],
        body='测试'
    )
    mail.send(message)
    return '发送成功'


@bp.route('/captcha', methods=['POST'])
# 还没设置好注册页面的时候使用下面的链接访问
# http://127.0.0.1:5000/user/captcha?email=919006684@qq.com
def getemaildaptcha():
    # get请求获取对应的邮箱
    # email = request.args.get('email')
    # post请求获取对应的邮箱
    email = request.form.get('email')
    # 获取数字和字母的库check
    check = string.digits + string.ascii_letters
    # 从check库获取随机四位的验证码
    captcha = ''.join(random.sample(check, 4))
    if email:
        message = Message(
            subject='稚至花',
            # recipients=['zhizhihua9808@163.com', '919006684@qq.com', 'sj13652388474@outlook.com'],
            recipients=[email],
            body=f'【稚至花科技有限公司】您在本公司注册的账号验证码是：【{captcha}】,请不要泄露给你身边的人哦☺！！'
        )
        # 发送message部分的内容
        mail.send(message)
        # 获取emailcaptcha表里面的email字段对应的邮箱的的第一条数据
        captchamodel = EmailcpatchaModel.query.filter_by(email=email).first()
        if captchamodel:
            # 如果数据库中存在验证码，则发送新的验证码captcha
            captchamodel.captcha = captcha
            # 发送新的内容之后要更新时间
            captchamodel.creat_time = datetime.now()
            # 上传到数据库中
            db.session.commit()
            # 不存在验证码则发送新的验证码
        else:
            captchamodel = EmailcpatchaModel(email=email, captcha=captcha)
            db.session.add(captchamodel)
            db.session.commit()
            # code 200在浏览器是访问请求正常的
        return jsonify({'code': 200})
    else:
        # 400 是客户端错误
        return jsonify({'code': 400, 'message': '请先传递邮箱！'})

#实现退出登录
@bp.route('/logout')
def logout():
    # 清除session所有的数据
    session.clear()
    return  redirect(url_for('user.login'))