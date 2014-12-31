from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

import shopgrab.settings as settings

import slumber
from requests.exceptions import ConnectionError
from slumber.exceptions import HttpClientError


def get_promotion_details(pk):
    pass


def get_promotion_list(retail_id):
    api = slumber.API(settings.SLUMBER_DIRECTORY)
    promotion_list = api.retails(retail_id).all_promotions.get()
    return promotion_list


def home(request):
    template = loader.get_template('retail/home.html')
    # retail_id = request.session.get('retail_id')
    retail_id = 1
    if retail_id is None:
        # return to login if there is no session / session expired
        return HttpResponseRedirect(reverse('shopgrab:login'))
    try:
        promotion_list = get_promotion_list(retail_id)
        connection_status = True
    except (ConnectionError, HttpClientError):
        promotion_list = []
        connection_status = False
        pass
    context = RequestContext(request, {
        'connection': connection_status,
        'promotion_list': promotion_list})
    return HttpResponse(template.render(context))
