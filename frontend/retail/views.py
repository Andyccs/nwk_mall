from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
import shopgrab.settings as settings
import slumber


def get_promotion_details(pk):
    pass


def get_promotion_list(retail_id):
    api = slumber.API(settings.SLUMBER_DIRECTORY)
    promotion_list = api.retails(retail_id).all_promotions.get()
    return promotion_list


def home(request):
    # retail_id = request.session.get('retail_id')
    retail_id = 1
    if retail_id is None:
        # return to login if there is no session / session expired
        return HttpResponseRedirect(reverse('shopgrab:login'))
    promotion_list = get_promotion_list(retail_id)
    template = loader.get_template('retail/home.html')
    context = RequestContext(request, {'promotion_list': promotion_list})
    return HttpResponse(template.render(context))
