from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import MessagesView, ChatRoomView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),  
    path('signup/', views.signup, name='signup'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('friend_requests/', views.friend_requests, name='friend_requests'),
    path('create_post/', views.create_post, name='create_post'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/update/<str:username>/', views.update_profile, name='update_profile'),
    path('logout/', views.user_logout, name='logout'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('update/username/<str:username>/', views.update_username, name='update_username'),
    path('update/pronouns/<str:username>/', views.update_pronouns, name='update_pronouns'),
    path('update/bio/<str:username>/', views.update_bio, name='update_bio'),
    path('unfriend/<int:user_id>/', views.unfriend_view, name='unfriend'),
    path('friends/', views.friends_view, name='friends'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    
    path('shorts/', views.shorts_view, name='shorts_view'),
    path('upload/', views.upload_view, name='upload'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    # path('create-card/', views.create_card, name='create_card'),
    path('cards/', views.cards_view, name='cards'),  # For logged-in user
    path('cards/<str:username>/', views.other_user_cards_view, name='user_cards'),
    # MESSAGING

    path('messages/', MessagesView.as_view(), name='messages'),
    path('chat/<str:username>/', ChatRoomView.as_view(), name='chat_room'),
    path('bookmarks/', views.bookmarks_view, name='bookmarks'),
    path('toggle-bookmark/', views.toggle_bookmark, name='toggle_bookmark'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
