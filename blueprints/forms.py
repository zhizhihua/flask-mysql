import wtforms
from wtforms.validators import length, email, EqualTo
from models import EmailcpatchaModel, UserModel


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    # password 的长度最少设置为200，为后期加密延长密码做准备
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[EqualTo('password')])

    # 验证验证码是否争取
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailcpatchaModel.query.filter_by(email=email).first()
        # 前提是将验证码都换成小写状态，如果输入的验证码和数据库的验证码一致则不提示下面的报错
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError('邮箱验证码错误！😜')

    # 验证邮箱是否重复注册
    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError('邮箱已经注册')


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class Question(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=3, max=200)])
    content = wtforms.StringField(validators=[length(min=5)])


