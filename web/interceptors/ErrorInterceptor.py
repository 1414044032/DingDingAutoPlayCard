from application import app
from common.Helper import ops_render


@app.errorhandler(404)
def error_404(e):
    return ops_render("error/error.html", {'status': 404, 'msg': '很抱歉，您访问的页面不存在！'})
