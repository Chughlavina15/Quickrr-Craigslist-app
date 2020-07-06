from django.urls import path
from. import views
from .views import index
urlpatterns=[
    path('',views.index,name='signup'),
    path('login/', views.login, name='login'),
    path('main/',views.home,name='home'),
    path('new_search/',views.new_search,name='new_search')
#    path('new-search/','views.new_search',name='new_search')

]