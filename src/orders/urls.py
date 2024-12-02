from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('cancel/<int:order_id>', views.order_cancel, name='order_cancel'),
    path('admin/order/<int:order_id>',
         views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/',
         views.admin_order_pdf,
         name='admin_order_pdf'
         ),
    path('', views.order_list, name='order_list'),
]
