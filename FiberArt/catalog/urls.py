from django.urls import path, include, re_path
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

# router = routers.DefaultRouter()
# router.register(r'color', views.ColorViewSet)

urlpatterns = [
    path('embroiders/', views.EmbroiderList.as_view()),
    path('embroiders/search/', views.search),
    #path('embroiders/<int:pk>/', views.EmbroideryDetail.as_view(), name='user-detail'),
    path('embroiders/<int:embroidery_id>/', views.EmbroideryDetail.as_view()),
    path('users/current', views.CurrentUserView.as_view()),
    path('my_embroiders', views.MyEmbroideryList.as_view()),
]

# urlpatterns = [
#     #path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls')),
# ]
#
# urlpatterns += [
#     path('', views.api_root),
#     path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
#     path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
#     path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),
#     path('users/', views.UserList.as_view(), name='user-list'),
#
# ]


