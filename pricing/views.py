from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django import forms
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.views.generic.edit import (
    ModelFormMixin, 
    ProcessFormView, 
    SingleObjectTemplateResponseMixin, 
)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import TemplateView as GenericTemplateView
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
import json
import pdb
from .forms import (
    ProductForm, 
    ComponentForm, 
    ComponentRelationshipForm,
    ProjectForm,
    ProjectComponentForm,
    get_all_fields
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

class BaseObjectView(ModelFormMixin, ProcessFormView):
    def set_object(self):
        if self.kwargs.get(self.pk_url_kwarg, None) is not None:
            self.object = self.get_object()
        else:
            self.object = None

    def get(self, request, *args, **kwargs):
        self.set_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.set_object()
        return super().post(request, *args, **kwargs)
        
    def delete(self, request, *args, **kwargs):
        response = {'message': 'Usunieto', 'result':True}
        try:
            self.object = self.get_object()
            self.object.delete()
        except:
            response = {'message': 'Nie usunieto', 'result':False}
        return JsonResponse(json.dumps([response]), safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        if pk is not None:
            context['pk'] = pk
        return context

class ObjectView(SingleObjectTemplateResponseMixin, BaseObjectView):
    template_name_suffix = '_form'

class ObjectSetView(ObjectView):
    form_set_class = None
    extra = 0
    related_name = None

    def formset_factory(self):
        return forms.formset_factory(self.form_set_class, extra=self.extra)

    def get_formset(self):
        FormSet = self.formset_factory()
        if self.object is None:
            return FormSet()
        else:
            formset_list = []
            related_query = getattr(self.object, self.related_name)
            for relation in related_query.all():
                form_relation = {}
                for field in get_all_fields(self.form_set_class):
                    form_relation.update({field: getattr(relation, 'get_' + field)()})
                formset_list.append(form_relation)
            return FormSet(initial=formset_list)
        
    def get_formset_from_request(self):
        FormSet = self.formset_factory()
        return FormSet(self.request.POST)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def formset_valid(self, formset):
        pass

    def formset_invalid(self, formset):
        for form in formset:
            if not form.is_valid():
                print(form.errors)

    def form_valid(self, form):
        formset = self.get_formset_from_request()
        if formset.is_valid():
            Response = super().form_valid(form)
            self.formset_valid(formset)
            return Response
        else:
            self.formset_invalid(formset)
            return super().form_invalid(form)

    def form_invalid(self, form):
        formset = self.get_formset_from_request()
        if not formset.is_valid():
            self.formset_invalid(formset)
        print(form.errors)
        return super().form_invalid(form)


class ProductEditView(ObjectView): 
    template_name = 'pricing/edit_product.html'
    model = Product
    form_class = ProductForm
    title = "Dodaj produkt"
    active = 'new_product_active'
    success_url = '/pricing/product/list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['pricing_active'] = 'active'
        context[self.active] = 'active'
        return context


class ComponentEditView(ObjectSetView):
    template_name = 'pricing/edit_component.html'
    model = Component
    form_class = ComponentForm
    title = "Dodaj komponent"
    active = 'new_component_active'
    success_url = '/pricing/component/list'
    form_set_class = ComponentRelationshipForm
    related_name = 'relationship'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #print(kwargs)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['pricing_active'] = 'active'
        context[self.active] = 'active'
        return context

    def formset_valid(self, formset):
        relationship = {}
        for form in formset:
            element_id = form.cleaned_data['id']
            amount = form.cleaned_data['amount']
            relationship.update({element_id: amount})
        self.object.update_children(relationship)


class ProjectEditView(ObjectSetView):
    template_name = 'pricing/edit_project.html'
    model = Project
    form_class = ProjectForm
    title = "Dodaj projekt"
    active = 'new_project_active'
    success_url = '/pricing/project/list'
    form_set_class = ProjectComponentForm
    related_name = 'components'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['pricing_active'] = 'active'
        context[self.active] = 'active'
        return context

    def formset_valid(self, formset):
        relationship = {}
        for form in formset:
            element_id = form.cleaned_data['id']
            amount = form.cleaned_data['amount']
            relationship.update({element_id: amount})
        self.object.update_children(relationship)


class TemplateView(GenericTemplateView):
    template_name = ''
    active = ''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pricing_active'] = 'active'
        context[self.active] = 'active'
        return context


class QueryView(View):
    queries = []
    properties = []
    def get(self, request, *args, **kwargs):
        avaiable = True
        #pdb.set_trace()
        for query in self.queries:
            if not query in request.GET:
                avaiable = False
                break
        if avaiable:
            return self.search(request)
        return JsonResponse(json.dumps([]), safe=False)

    def json_response(self, model_results):
        results = []
        for obj in model_results:
            results.append(self.convert_object(obj))
        return JsonResponse(json.dumps(results[:10]), safe=False)

    def convert_object(self, obj):
        obj_dict = {}
        for prop in self.properties:
            obj_dict.update({prop: str(getattr(obj, prop))})
        return obj_dict



class NameSearchView(QueryView):
    queries = [u'query']
    model = None
    def search(self, request):
        value = request.GET[u'query']
        model_results = self.model.objects.filter(name__icontains=value)
        return self.json_response(model_results)


class ProductSearchView(NameSearchView):
    properties=['id', 'name', 'brand', 'price', 'group']
    model = Product


class ComponentSearchView(NameSearchView):
    properties=['id', 'name']
    model = Component

    def convert_object(self, obj):
        obj_dict = super().convert_object(obj)
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