from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'graduation'
urlpatterns = [
    path('guide1/', views.Guide_rearchView.as_view(), name="guide_rearch"),
    path('guide2/', views.Guide_rearch_resultView.as_view(), name="guide_rearch_result"),
    path('guide3/', views.Guide_addView.as_view(), name="guide_add"),
    path('guide4/<slug:pk>', views.Guide_detailView.as_view(), name="guide_detail"),
    path('guide5/', views.Guide_listView.as_view(), name="guide_list"),
    path('guide5_2/<slug:pk>', views.Guide_deleteView.as_view(), name="guide_delete"),
    path('guide6/', views.Guide_favorite_listView.as_view(), name="guide_favorite_list"),
    path('guide7/<slug:pk>', views.Guide_place_detailView.as_view(), name="guide_place_detail"),
    
    path('favorite/<slug:pk>', views.Guide_favoriteView, name="guide_favorite"),
    path('favorite2/<slug:pk>', views.Guide_favorite2View, name="guide_favorite2"),
    path('place/<slug:pk>', views.Guide_place_favoriteView, name="guide_place_favorite"),
]