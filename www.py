from application import app

# 统一拦截器
from web.interceptors.ErrorInterceptor import *

# 蓝图功能，对所有的url进行蓝图功能配置
from web.controllers.index import route_index
from web.controllers.static import route_static

app.register_blueprint(route_index, url_prefix='/')
app.register_blueprint(route_static, url_prefix='/static')
