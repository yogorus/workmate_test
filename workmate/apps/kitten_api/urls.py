from rest_framework import routers
from apps.kitten_api import views

router = routers.DefaultRouter()

router.register(r"kittens", views.KittenViewSet, "kittens")
router.register(r"breeds", views.BreedViewSet, "breeds")

urlpatterns = []

urlpatterns += router.urls
