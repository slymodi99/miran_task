from rest_framework.routers import SimpleRouter

from products.api.views import ProductViewSet

router = SimpleRouter()
router.register("", ProductViewSet, basename="products")
urlpatterns = router.urls
