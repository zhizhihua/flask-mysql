# 主要用于装饰方向：
"""
装饰对应的需要登录之后才能访问的内容机制
"""
from flask import g, redirect, url_for
from functools import wraps


def login_required(func):
    # 这个装饰器一定不要忘记写了
    @wraps(func)
    # *args, **kwargs 表示全部参数类型
    def wrapper(*args, **kwargs):
        # 如果登录了跳转到问答页面
        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))

    return wrapper
