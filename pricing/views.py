from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django import forms
from django.core.paginator import Paginator
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from common.views import (
    ObjectView,
    ObjectSetView,
    QueryView,
    NameSearchView,
    VueView
)

from .forms import (
    ProductForm, 
    ComponentForm, 
    ComponentRelationshipForm,
    ProjectForm,
    ProjectComponentForm
)
from .models import (
    Product,
    Group, 
    Component, 
    ElementRelationship,
    Project,
    ProjectComponent
)

def index(request):
    return render(request, 'pricing/index.html', {
        'pricing_active': 'active'
    })

class AppViewNav:
    app = 'pricing'

class ProductEditView(ObjectView, AppViewNav): 
    template_name = 'pricing_editpage.html'
    model = Product
    form_class = ProductForm
    success_url = '/pricing/products'
    page = 'product_edit'


class ComponentEditView(ObjectSetView, AppViewNav):
    template_name = 'pricing_editpage.html'
    model = Component
    form_class = ComponentForm
    success_url = '/pricing/components'
    form_set_class = ComponentRelationshipForm
    related_name = 'relationship'
    page = 'component_edit'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #print(kwargs)
        return kwargs

    def formset_valid(self, formset):
        relationship = {}
        for form in formset:
            element_id = form.cleaned_data['id']
            amount = form.cleaned_data['amount']
            relationship.update({element_id: amount})
        self.object.update_children(relationship)


class ProjectEditView(ObjectSetView, AppViewNav):
    template_name = 'pricing_editpage.html'
    model = Project
    form_class = ProjectForm
    success_url = '/pricing/projects'
    form_set_class = ProjectComponentForm
    related_name = 'components'
    page = 'project_edit'

    def formset_valid(self, formset):
        relationship = {}
        for form in formset:
            element_id = form.cleaned_data['id']
            amount = form.cleaned_data['amount']
            relationship.update({element_id: amount})
        self.object.update_children(relationship)


class PricingVueView(VueView):
    app_name = 'pricing' 

    
class EditPricingVueView(PricingVueView):
    app_name = 'pricing'      
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.template_name = self.app_name + '_editpage.html'
        return context


class ProductSearchView(NameSearchView):
    properties=['id', 'name', 'brand', 'price', 'group']
    model = Product


class ComponentSearchView(NameSearchView):
    properties=['id', 'name']
    model = Component

    def convert_object(self, obj):
        obj_dict = super().convert_object(obj)
        if obj.project is not None:
            obj_dict.update({'project': obj.project.name})
        return obj_dict

class ProjectComponentsSearchView(QueryView):
    queries = [u'name', u'project']
    properties=['id', 'name']
    def search(self, request):
        name = request.GET[u'name']
        project_id = int(request.GET[u'project'])
        project = Project.objects.get(pk=project_id)
        if project is None:
            return self.json_response([])
        components = project.related_components
        model_results = components.filter(name__icontains=name)
        return self.json_response(model_results)


class ProjectSearchView(NameSearchView):
    properties=['id', 'name', 'leader']
    model = Project


class ComponentDetailsView(SingleObjectMixin, TemplateView):
    model = Component
    object = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        component = self.get_object()
        if component is not None:
            context['pk'] = component.pk
            context['name'] = component.name
            context['products'] = component.get_all_products(1, component)
            print(context['products'])
        return context


class ProjectDetailsView(SingleObjectMixin, TemplateView):
    model = Project
    object = None
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        if project is not None:
            context['pk'] = project.pk
            context['name'] = project.name
            context['leader'] = project.leader
            context['description'] = project.description
            context['products'] = project.get_all_products()
            print(context['products'])
        return context