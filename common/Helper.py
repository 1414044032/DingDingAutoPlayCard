import datetime

from flask import g, render_template


#  统一渲染
def ops_render(template, context={}):
    return render_template(template, **context)


# 获取当前时间
def getCurrentDate(fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime((fmt))
