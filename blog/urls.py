from django.urls import path
from .import views


urlpatterns = [
    path('signup', views.create_account, name="signup"),
    path('signin', views.user_login, name="login"),
    path('create_post', views.create_post, name="create-post"),
    path('logout', views.user_logout, name="logout"),
    path('all_post', views.all_post, name="all-post"),
    path('create_post', views.create_post, name="create-post"),
    path('detail_post/<int:post_id>', views.detail_post, name="detail-post"),
    path('create_comment/<int:post_id>', views.create_comment, name="create-comment"),
    path('delete/<int:post_id>', views.delete_post, name="delete-post"),
    path('all_users', views.all_users, name="all-users"),
    path('delete_user/<int:user_id>', views.delete_user, name="delete-user"),
]