from django.urls import path
from . import views

app_name = 'graduation'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('gourmet/', views.GourmetView.as_view(), name="gourmet"),
    path('gourmet_search/', views.Gourmet_searchView.as_view(), name="gourmet_search"),
    path('gourmet_detail/<str:pk>', views.Gourmet_detailView.as_view(), name="gourmet_detail"),
    path('shop/', views.ShopView.as_view(), name="shop"),
    path('shop_list/', views.ShopListView.as_view(), name="shop_list"),
    path('shop_shosai/<slug:pk>', views.Shop_detailView.as_view(), name="shop_shosai"),
    # path('shop_gourmet/', views.ShopGourmetView.as_view(), name="shop_gourmet"),
    path('account/', views.AccountView.as_view(), name="account"),
    #サインアップ用ページ
    path('accounts/user-signup', views.UserSignupView.as_view(), name="user_signup"),
    #ガイドコース
    path('guide1/', views.Guide_rearchView.as_view(), name="guide_rearch"),
    path('guide2/', views.Guide_rearch_resultView.as_view(), name="guide_rearch_result"),
    path('guide3/', views.Guide_addView.as_view(), name="guide_add"),
    path('guide4/<slug:pk>', views.Guide_detailView.as_view(), name="guide_detail"),
    path('guide5/', views.Guide_listView.as_view(), name="guide_list"),
    path('guide5_2/<slug:pk>', views.Guide_deleteView.as_view(), name="guide_delete"),
    path('guide6/', views.Guide_favorite_listView.as_view(), name="guide_favorite_list"),
    path('guide7/<slug:pk>', views.Guide_place_detailView.as_view(), name="guide_place_detail"),
    path('guide8/', views.Guide_MylistView.as_view(), name="guide_mylist"),
    
    path('favorite/<slug:pk>', views.Guide_favoriteView, name="guide_favorite"),
    path('favorite2/<slug:pk>', views.Guide_favorite2View, name="guide_favorite2"),
    path('place/<slug:pk>', views.Guide_place_favoriteView, name="guide_place_favorite"),

]