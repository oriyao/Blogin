"""
# coding:utf-8
@Time    : 2020/9/21
@Author  : jiangwei
@mail    : jiangwei1@kylinos.cn
@File    : decorators
@Software: PyCharm
"""
import datetime
from functools import wraps

from flask import Markup, flash, url_for, redirect, abort,current_app,request
from flask_login import current_user


# 某些操作需要确认后才能进行
def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirm:
            message = Markup(
                'Please confirm your account first.'
                'Not receive the email?'
                '<a class="alert-link" href="%s">Resend Confirm Email</a>' %
                url_for('auth.resend_confirm_email'))
            flash(message, 'warning.txt')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)

    return decorated_function


# 后台管理页面不允许普通用户登入
def permission_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.role_id == 1:
            abort(403)
        return func(*args, **kwargs)

    return decorated_function


def db_exception_handle(db):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                import traceback
                traceback.print_exc()
                db.session.rollback()
                abort(500)
        return decorated_function
    return decorator


def statistic_traffic(db, obj):
    """
    网站今日访问量、评论量、点赞量统计装饰器
    :param db: 数据库操作对象
    :param obj: 统计模型类别(VisitStatistics,CommentStatistics,LikeStatistics)
    :return:
    """
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            # 类型不能为str类型，后续可以考虑将数据库中格式修改为text
            td= datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d'), "%Y-%m-%d")
            vst = obj.query.filter_by(date=td.strftime('%Y-%m-%d')).first()
            if vst is None:
                current_app.logger.info('新的一天开始了: ' + request.remote_addr + '第一个访问了openstack.top')
                new_vst = obj(date=td, times=1)
                db.session.add(new_vst)
            else:
                current_app.logger.info('老日期，访问次数加1 : ' + str(td))
                vst.times += 1
            db.session.commit()
            pass
            return func(*args, **kwargs)
        return decorated_function
    return decorator
