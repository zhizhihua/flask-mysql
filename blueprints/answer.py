from flask import flash, Blueprint, render_template, g, request, redirect, url_for
from decorators import login_required
from .forms import Question
from models import QuestionModel
from exts import db

# 对应的访问的url的前缀   http://127.0.0.1:5000/
bp = Blueprint('answer', __name__, url_prefix='/')


# 设置在answer蓝图下的answer界面 就是问答的页面  访问http://127.0.0.1:5000/即可到达
@bp.route('/')
def answer():
    # if hasattr(g,'user'):
    #     # 获取当前登录的用户的名字
    #     print(g.user.username)
    # context = {'user':g.user}
    # return render_template('index.html',**context)
    # 上面的代码主要是让我们理解具体的操作结果和代码逻辑
    return render_template('index.html')


@bp.route('/question/public', methods=['GET', 'POST'])
# 装饰器
@login_required
def public_question():
    # 判断是否登录，如果没登录，跳转到登录界面
    # if hasattr(g,'user'):
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        # 设置表单验证
        form = Question(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect('/')
        else:
            # 提示报错信息
            flash('标题或者内容格式错误！！！')
            # 跳转到当前页面
            return redirect(url_for('answer.public_question'))

    # return render_template('public_question.html')
