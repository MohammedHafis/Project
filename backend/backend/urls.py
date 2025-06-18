from adminapp import views
from django.urls import path
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('', views.Login,name='login'),
    path('movielist/',views.movielist,name='movielist'),
    path('addmovie/',views.addmovie),
    path('editmovie/<int:pk>/',views.editmovie,name='edit_movie'),
    path('deletemovie/<int:pk>/',views.movie_delete,name='delete_movie'),
    path('viewmovie/<int:pk>',views.viewmovie,name='view_movie'),
    path('userlist/',views.userlist,name='userlist'),
    path('block/<int:pk>',views.blockuser,name='blockuser'),
    path('unblockuser/<int:pk>/', views.unblockuser, name='unblockuser'),
    path('userhistory/<int:pk>/',views.userhistory,name='user_history'),
    path('reports/',views.reports),
    path('changepass/',views.changepassword,name='change_password'),
    path('logout/',views.logout),
    path('signup/',views.signup,name='signup_api'),
    path('loginup/',views.loginup,name='login_api'),
    path('movie_list/',views.movie_list,name='movielist_api'),
    path('watchlater/',views.add_watchlater,name='add_watchlater_api'),
    path('watchlater_list/',views.watchlater_list,name='watchlater_list_api'),
    path('watchlater_remove/<int:movie_id>/', views.remove_watchlater, name='remove_watchlater_api'),
    path('watch_history/',views.watch_history,name='watch_history_api'),
    path('history_list/',views.watch_history_list,name='history_list_api'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('changepassword/', views.change_password, name='changepassword_api'),    
    ]
    
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

