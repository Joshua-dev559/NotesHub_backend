from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from notes.views import RegisterView, MeView, LogoutView, EmailTokenObtainPairView

router = DefaultRouter()
router.register(r"notes", NoteViewSet, basename="note")

urlpatterns = [
    path("", include(router.urls)),
    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
]