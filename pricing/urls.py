from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),

  path('product/list', 
       views.TemplateView.as_view(template_name="pricing/list_product.html", active="products_active"), 
       name='product_list'),

  path('product/edit/<int:pk>', 
        views.ProductEditView.as_view(title="Edytuj produkt"), 
        name='edit_product'),

  path('product/new', views.ProductEditView.as_view(), name='new_product'),

  path('component/list', 
       views.TemplateView.as_view(template_name="pricing/list_component.html", active="components_active"), 
       name='component_list'),

  path('component/<int:pk>/', 
       views.ComponentDetailsView.as_view(template_name="pricing/details_component.html"), 
       name='edit_component'),

  path('component/edit/<int:pk>/', 
       views.ComponentEditView.as_view(title="Edytuj komponent"), 
       name='edit_component'),

  path('component/new', views.ComponentEditView.as_view(), name='new_component'),

  path('project/list', 
       views.TemplateView.as_view(template_name="pricing/list_project.html", active="projects_active"), 
       name='project_list'),

  path('project/edit/<int:pk>/', 
       views.ProjectEditView.as_view(title="Edytuj projekt"), 
       name='edit_project'),

  path('project/new', views.ProjectEditView.as_view(), name='new_project'),

  #path('new_order', views.new_order, name='new_order'),
  #path('order_history', views.order_history, name='order_history'),
  # REST API
  path('products', views.ProductSearchView.as_view(), name='products'),
  path('components', views.ComponentSearchView.as_view(), name='components'),
  path('projects', views.ProjectSearchView.as_view(), name='projects'),
  #path('dependency', views.dependency, name='dependency'),
]
