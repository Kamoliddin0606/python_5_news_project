from django.urls import path, include
from .views import home, detailPost,category
urlpatterns = [
    path('', home, name='home'),
    path('detail/<int:pk>/', detailPost, name='detail'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('category/<int:pk>/', category, name='category'),
   
]


