from django.urls import path
from photo.views import home, register, user_login, user_logout, profile, photo_details, like_photo, dislike_photo, add_photo
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('add_photo/', add_photo, name='add_photo'),
    path('photo/<int:photo_id>/', photo_details, name='photo_details'),
    path('like/<int:photo_id>/', like_photo, name='like_photo'),
    path('dislike/<int:photo_id>/', dislike_photo, name='dislike_photo'),
]

urlpatterns += staticfiles_urlpatterns()

