from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('product_list', views.products, name='product_list'),
  path('product/<int:pk>/edit', views.edit_product, name='edit_product'),
  path('new_product', views.new_product, name='new_product'),
  #path('machine_list', views.machines, name='machine_list'),
  #path('machine/<int:pk>/edit', views.machine_product, name='machine_product'),
  #path('new_machine', views.new_machine, name='new_machine'),
  #path('new_order', views.new_order, name='new_order'),
  #path('order_history', views.order_history, name='order_history'),
  # REST API
  path('products', views.search_products, name='products'),
  path('dependency', views.dependency, name='dependency'),
]
