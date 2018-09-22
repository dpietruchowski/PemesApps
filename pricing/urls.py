from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),

  path('products', views.PricingVueView.as_view(page='products')),
  path('components', views.PricingVueView.as_view(page='components')),
  path('projects', views.PricingVueView.as_view(page='projects')),

  path('product/new', views.ProductEditView.as_view(), name='new_product'),
  path('component/new', views.ComponentEditView.as_view(), name='new_component'),
  path('project/new', views.ProjectEditView.as_view(), name='new_project'),

  path('product/edit/<int:pk>', 
        views.ProductEditView.as_view(), 
        name='edit_product'),
  path('component/edit/<int:pk>/', 
       views.ComponentEditView.as_view(), 
       name='details_component'),
  path('project/edit/<int:pk>/', 
       views.ProjectEditView.as_view(), 
       name='edit_project'),

  path('component/<int:pk>/', 
       views.ComponentDetailsView.as_view(template_name="pricing/details_component.html"), 
       name='edit_component'),
  path('project/<int:pk>/', 
       views.ProjectDetailsView.as_view(template_name="pricing/details_project.html"), 
       name='details_project'),


  #path('new_order', views.new_order, name='new_order'),
  #path('order_history', views.order_history, name='order_history'),
  # REST API
  path('product/list', views.ProductSearchView.as_view(), name='products'),
  path('component/list', views.ComponentSearchView.as_view(), name='components'),
  path('component/list', views.ProjectComponentsSearchView.as_view(), name='project_components'),
  path('project/list', views.ProjectSearchView.as_view(), name='projects'),
  #path('dependency', views.dependency, name='dependency'),
]
