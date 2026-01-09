from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from livros.views import LivroViewSet, register_user, CategoriaViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'livros', LivroViewSet, basename='livro')  
router.register(r'categorias', CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    # JWT login e refresh
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # registrar novo ut
    path('register/', register_user, name='register'),
]






