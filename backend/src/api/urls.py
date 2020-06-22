from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import authentication_views

router = DefaultRouter()
router.register('profile', authentication_views.UserProfileViewSet)

urlpatterns = [
    path('hello-view/',authentication_views.HelloApiView.as_view()),
    path('',include(router.urls)),
    path('activate/<str:token>/',authentication_views.ActivateAccountView.as_view()),
    path('signin/', authentication_views.Signin),
    path('google-login/', authentication_views.Google_Login),
    path('facebook-login/', authentication_views.Facebook_Login),

    path('forgot-password/',authentication_views.post_email_for_reset_password),
    path('reset-password/<str:token>/',authentication_views.reset_password),

]
