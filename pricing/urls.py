from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('product_list', views.products, name='product_list'),
  path('product/<int:pk>/edit', views.edit_product, name='edit_product'),
  path('new_product', views.new_product, name='new_product'),
  path('new_order', views.new_order, name='new_order'),
  # REST API
  path('products', views.search_products, name='products'),
  path('dependency', views.dependency, name='dependency'),
]
