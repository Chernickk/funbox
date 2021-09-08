from rest_framework.routers import SimpleRouter
from .views import VisitedLinks, VisitedDomains
from django.urls import path, include


router = SimpleRouter()

router.register('visited_links', VisitedLinks, basename='visited_links')

urlpatterns = [
    path('visited_links/', VisitedLinks.as_view()),
    path('visited_domains/', VisitedDomains.as_view()),
]
