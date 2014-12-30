from django.conf.urls import url, include
from rest_framework import routers
from nwk import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'retails', views.RetailViewSet)

# promotion
router.register(r'promotions', views.PromotionViewSet)
# promotion type
# router.register(r'promotion_type', views.PromotionTypeViewSet)
# promotion tags
router.register(r'p_reductions', views.PromotionReductionViewSet)
router.register(r'p_discounts', views.PromotionDiscountViewSet)
router.register(r'p_generals', views.PromotionGeneralViewSet)

router.register(r'mall', views.MallViewSet)
router.register(r'consumers', views.ConsumerGeneralViewSet)
router.register(r'grab_promotions', views.GrabPromotionsGeneralViewSet)
router.register(r'applications', views.ApplicationViewSet)

# TODO: add filter to allow browsing promotions by retail
# TODO: add filter to allow browsing grab promotions by retail
# TODO: add filter to allow browsing grab promotions by user

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('mysite.urls')),
]
