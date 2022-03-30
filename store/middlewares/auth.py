from django.shortcuts import redirect

def auth_middleware(get_response):


    def middleware(request):
        returnURL = request.META['PATH_INFO']
        if not request.session.get('customer'):

            return redirect(f'login?return_url={returnURL}')
        response = get_response(request)
        return response

    return middleware