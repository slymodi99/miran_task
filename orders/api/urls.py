from rest_framework.routers import SimpleRouter

from orders.api.views import OrderViewSet

router = SimpleRouter()
router.register("", OrderViewSet, basename="orders")
urlpatterns = router.urls
