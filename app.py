from flask import Flask, request, Response, session,g
from exts import db, mail
import config
# from blueprints.answer import  bp as answer_bp
from blueprints import answer_bp
from blueprints import user_bp
from flask_migrate import Migrate
# 导入数据库模型
from models import EmailcpatchaModel,UserModel

app = Flask(__name__)
app.config.from_object(config)
# 绑定exts的 db内容到app文件
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(answer_bp)
app.register_blueprint(user_bp)

# 钩子函数
@app.before_request
# 请求之前执行这个函数
def before_request():
    # 获取到位数据库里面对应的user表的id
    user_id = session.get('user_id')
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定一个叫做user的变量，他的值是user这个变量
            setattr(g,'user',user)
            # user变量绑定成为全局变量
            # g.user = user
        except:

            g.user =None


# 上下文处理器
# 请求来了，先执行请求（before——request），在执行视图函数，在返回视图函数中的模板
# 最后执行context_processor
@app.context_processor
def context_processor():
    # 判断是否绑定了这个user全局变量
    if hasattr(g,'user'):
        return {'user':g.user}
    else:
        return {}



if __name__ == '__main__':
    app.run()
