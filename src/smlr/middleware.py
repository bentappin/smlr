

class SetRemoteAddrMiddleware(object):
    def process_request(self, request):
        if not request.META.has_key('REMOTE_ADDR'):
            try:
                request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
            except:
                request.META['REMOTE_ADDR'] = '1.1.1.1'
