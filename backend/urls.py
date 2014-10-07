from django.conf.urls import url, include
from rest_framework import routers
from nwk import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'retails', views.RetailViewSet)
router.register(r'promotions', views.PromotionViewSet)
router.register(r'p_reductions', views.PromotionPriceReductionViewSet)
router.register(r'p_discounts', views.PromotionDiscountViewSet)
router.register(r'p_generals', views.PromotionGeneralViewSet)
router.register(r'consumers', views.ConsumerGeneralViewSet)
router.register(r'applications', views.ApplicationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('mysite.urls')),
]