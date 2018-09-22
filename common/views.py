from django import forms
from django.views.generic.edit import (
    ModelFormMixin, 
    ProcessFormView, 
    SingleObjectTemplateResponseMixin, 
)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import TemplateView as GenericTemplateView
from django.views.generic import View

from django.http import HttpResponse, JsonResponse

from decimal import *

import json
import pdb

from .utils import *

from pricing.models import Project

class BaseObjectView(ModelFormMixin, ProcessFormView):
    def set_object(self):
        if self.kwargs.get(self.pk_url_kwarg, None) is not None:
            self.object = self.get_object()
            if self.object is not None:
                self.form_array = []
                for field in get_all_fields(self.form_class):
                    attr = getattr(self.object, field)
                    if isinstance(attr, str):
                        pass
                    elif isinstance(attr, Decimal):
                        attr = float(attr)
                    elif isinstance(attr, Project):
                        continue
                    elif attr is None:
                        continue
                    else:
                        pdb.set_trace()
                        raise Exception('Unknown {} field type'.format(field))
                    self.form_array.append({field: attr})
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
        page_active = self.page
        if pk is not None:
            context['pk'] = pk
            context['form_array'] = self.form_array
        context[self.app + '_active'] = 'active'
        context['page'] = self.page
        context[page_active] = 'active'
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
        self.formset_list = []
        if self.object is not None:
            related_query = getattr(self.object, self.related_name)
            for relation in related_query.all():
                form_relation = {}
                for field in get_all_fields(self.form_set_class):
                    form_relation.update({field: getattr(relation, 'get_' + field)()})
                self.formset_list.append(form_relation)
        
    def get_formset_from_request(self):
        FormSet = self.formset_factory()
        return FormSet(self.request.POST)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.get_formset()
        context['formset_list'] = self.formset_list
        return context

    def formset_valid(self, formset):
        pass

    def formset_invalid(self, formset):
        for form in formset:
            if not form.is_valid():
                print("Errory")
                print(form)
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
        print("Errory")
        print(form)
        print(form.errors)
        return super().form_invalid(form)


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


class VueView(GenericTemplateView):
    app_name = ''
    page = ''
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.app_name] = 'active'
        context[self.page] = 'active'
        context['page'] = self.page
        self.template_name = self.app_name + '_page.html'
        return context