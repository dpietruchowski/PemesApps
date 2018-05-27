from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django import forms
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
import json
import pdb
from .forms import ProductForm
from .models import Product, Group

def index(request):
    return render(request, 'pricing/index.html', {
        'pricing_active': 'active'
    })

class ProductView(FormView):
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
        context['new_product_active'] = 'active'
        if 'pk' in self.kwargs:
            context['pk'] = int(self.kwargs['pk'])
        return context

    def form_valid(self, form):
        print("valid")
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        if 'pk' in self.kwargs:
            form_kwargs['instance'] = self.model.objects.get(pk=int(self.kwargs['pk']))
        return form_kwargs

@csrf_exempt 
def delete_product(request, pk):
    result = 'failed'
    if request.method == "DELETE":
        product = Product.objects.get(pk=pk)
        product.delete()
        result = 'success'
    return JsonResponse(json.dumps([{'result': result}]), safe=False)


def product_list(request):
    return render(request, 'pricing/product_list.html', {
        'pricing_active': 'active',
        'products_active': 'active',
    })


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
