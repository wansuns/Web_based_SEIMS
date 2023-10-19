#from django.middleware import

from django.utils.deprecation import MiddlewareMixin


class loginmidle(MiddlewareMixin):

    def process_request(self, request):
        print(request)
        if request.path_info in ['/userinfo/list/','userinfo/add']:
            print(request.path_info)

        info=request.session.get('id')
        if not info:
            print('未登录操作')

    def process_response(self, request, response):
        print('经过了loginmidle中间件')
        return response