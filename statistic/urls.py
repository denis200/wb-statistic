from django.urls import path
from . import views

urlpatterns=[
    path('productcard/',views.ProductView.as_view({'get':'list','post':'create'})),
    path('productcard/<int:pk>',views.ProductView.as_view({'put':'update','delete':'destroy'})),

    path('productstate/',views.ProductStateView.as_view({'get':'list','post':'create'})),
    path('productstate/<int:pk>',views.ProductStateView.as_view({'put':'update','delete':'destroy'})),

    path('cardtracking/',views.TrackingView.as_view({'get':'list','post':'create'})),
    path('cardtracking/<int:pk>',views.TrackingView.as_view({'put':'update','delete':'destroy'})),
]