from django.urls import path,include
from . import views

urlpatterns=[
    path('productcard/',views.ProductView.as_view({'get':'list','post':'create'})),
    path('productcard/<int:pk>',views.ProductView.as_view({'put':'update','delete':'destroy'})),

    path('productstate/',views.ProductStateView.as_view({'get':'list','post':'create'})),
    path('productstate/<int:pk>',views.ProductStateView.as_view({'put':'update','delete':'destroy'})),

    path('getstate/',views.GetProductState.as_view()),
    path('print/',views.PrintView.as_view())
]