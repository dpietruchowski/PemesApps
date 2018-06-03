from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),

  path('product/list', 
       views.TemplateView.as_view(template_name="pricing/list_product.html", active="products_active"), 
       name='product_list'),

  path('product/<int:pk>', 
        views.ProductView.as_view(title="Edytuj produkt"), 
        name='edit_product'),

  path('product/new', views.ProductView.as_view(), name='new_product'),

  path('component/list', 
       views.TemplateView.as_view(template_name="pricing/list_component.html", active="components_active"), 
       name='component_list'),

  path('component/<int:pk>/', 
       views.ComponentView.as_view(title="Edytuj komponent"), 
       name='edit_component'),

  path('component/new', views.ComponentView.as_view(), name='new_component'),

  #path('new_order', views.new_order, name='new_order'),
  #path('order_history', views.order_history, name='order_history'),
  # REST API
  path('products', views.ProductSearchView.as_view(), name='products'),
  path('components', views.ComponentSearchView.as_view(), name='components'),
  #path('dependency', views.dependency, name='dependency'),
]
