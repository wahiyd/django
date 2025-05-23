from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminThemeViewSet, theme_editor

router = DefaultRouter()
router.register(r'themes', AdminThemeViewSet, basename='admintheme')

urlpatterns = [
    path('', include(router.urls)),
    path('editor/', theme_editor, name='theme_editor'),
]
