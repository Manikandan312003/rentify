from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import ProfileViewSet, MyView, Register, Login

profileRouter = DefaultRouter()

profileRouter.register('user', ProfileViewSet)

urlpatterns = [
    path('user/me', MyView.as_view()),
    path('user/register', Register.as_view(), name='register'),
    path('user/login', Login.as_view(), name='login'),
]

urlpatterns += profileRouter.urls