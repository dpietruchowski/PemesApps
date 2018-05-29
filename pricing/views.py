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
from django.views.generic import TemplateView as GenericTemplateView
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
import json
import pdb
from .forms import (
    ProductForm, 
    ComponentForm, 
    ComponentRelationshipForm,
    get_all_fields
)
from .models import Product, Group, Component, ElementRelationship

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
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect()
        
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
    extra = 2
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
                pdb.set_trace()
                for field in get_all_fields(self.form_set_class):
                    form_relation.update({field: getattr(relation, field)})
                formset_list.append(form_relation)
            return FormSet(initial=formset_list)
        
    def get_formset_from_request(self):
        FormSet = self.formset_factory()
        return FormSet(self.request.POST)

    def get_context_data(self, **kwargs,):
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

    def form_invalid(self, form):
        formset = self.get_formset_from_request()
        if not formset.is_valid():
            self.formset_invalid(formset)


class ProductView(ObjectView): 
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


class ComponentView(ObjectSetView):
    template_name = 'pricing/edit_component.html'
    model = Component
    form_class = ComponentForm
    title = "Dodaj komponent"
    active = 'new_component_active'
    success_url = '/pricing/component/list'
    form_set_class = ComponentRelationshipForm
    related_name = 'relationship'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['pricing_active'] = 'active'
        context[self.active] = 'active'
        return context

    def formset_valid(self, formset):
        relationship = {}
        for form in formset:
            element_id = form.cleaned_data['element_id']
            amount = form.cleaned_data['amount']
            relationship.update({element_id: amount})

class TemplateView(GenericTemplateView):
    template_name = ''
    active = ''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pricing_active'] = 'active'
        context[self.active] = 'active'
        return context


def search_products(request):
    results = []
    if request.method == "GET":
        if u'query' in request.GET:
            value = request.GET[u'query']
            model_results = Product.objects.filter(name__icontains=value)
            results = [{"id": str(x.id), 
                        "name": x.name, 
                        "price": str(x.price),
                        "group": str(Group(x.group))} 
                        for x in model_results]
    return JsonResponse(json.dumps(results[:10]), safe=False)
