from django.conf.urls import patterns, url, include
from nwk import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'retails', views.RetailViewSet)
router.register(r'promotions', views.PromotionViewSet)
router.register(r'p_reductions', views.PromotionReductionViewSet)
router.register(r'p_discounts', views.PromotionDiscountViewSet)
router.register(r'p_generals', views.PromotionGeneralViewSet)
router.register(r'consumers', views.ConsumerGeneralViewSet)
router.register(r'applications', views.ApplicationViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include(
        'rest_framework.urls',
        namespace='rest_framework')),
    url(r'^register/$', views.register, name='detail'),
)
