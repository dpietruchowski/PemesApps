from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
import json
import pdb
from . import models
from . import forms as myforms

def index(request):
    return render(request, 'pricing/index.html')

def post_product(request, DependencyFormSet, pk):
    form = myforms.ProductForm(request.POST)
    formset = DependencyFormSet(request.POST)
    valid = False
    dependency = {}
    if formset.is_valid() and form.is_valid():
        valid = True
        name = form.cleaned_data['name']
        price = form.cleaned_data['price']
        for f in formset:
            product_id = f.cleaned_data['product_id']
            amount = f.cleaned_data['amount']
            dependency.update({product_id: amount})
    else:
        for f in formset:
            if not f.is_valid():
                print(f.errors)

    if valid:
        if pk is None:
            product = models.Product.objects.create(
                name=name,
                price=price
            )
        else:
            product = models.Product.objects.get(pk=pk)
        product.update_children(dependency)
        return redirect(products)

    return HttpResponse("Nie udalo sie")

def edit_product(request, pk):
    DependencyFormSet = forms.formset_factory(myforms.DependencyForm, extra=0)
    if request.method == 'POST':
        return post_product(request, DependencyFormSet, pk)
    else:
        product = get_object_or_404(models.Product, pk=pk)
        #print(product.get_full_dependency())
        form = myforms.ProductForm(initial={
            'name': product.name,
            'price': product.price
        })
        children_form_set = []
        for child in product.children.all():
            children_form_set.append({
                'product_id': child.child.pk,
                'name': child.child.name,
                'amount': child.amount
            })
        formset = DependencyFormSet(initial=children_form_set)
    return render(request, 'pricing/edit_product.html', {
        'form' : form, 
        'formset': formset,
    })

def new_product(request):
    DependencyFormSet = forms.formset_factory(myforms.DependencyForm, extra=0)
    if request.method == 'POST':
        return post_product(request, DependencyFormSet, None)
    formset = DependencyFormSet()
    form = myforms.ProductForm()
    return render(request, 'pricing/edit_product.html', {
        'form' : form,
    })

def products(request):
    paginator = Paginator(models.Product.objects.all().order_by('-name'), 20)
    page = request.GET.get('page')
    product_list = paginator.get_page(page)
    return render(request, 'pricing/product_list.html', {'product_list' : product_list})

def search_products(request):
    results = []
    if request.method == "GET":
        if u'query' in request.GET:
            value = request.GET[u'query']
            model_results = models.Product.objects.filter(name__icontains=value)
            results = [{"id": str(x.id), "name": x.name, "price": str(x.price)} for x in model_results]
    return JsonResponse(json.dumps(results[:10]), safe=False)

def new_order(request):
    return render(request, 'pricing/edit_order.html', {
    })

def dependency(request):
    results = []
    if request.method == "GET":
        amount = 1
        if u'amount' in request.GET:
            amount = int(request.GET[u'amount'])
        if u'id' in request.GET:
            id = request.GET[u'id']
            try:
                product = models.Product.objects.get(pk=int(id))
            except models.Product.DoesNotExist:
                return JsonResponse(json.dumps([]), safe=False)
            for product_dep in product.get_full_dependency(amount):
                product_amount = product_dep["amount"]
                child_product = product_dep["object"]
                results.append({
                    "pk": child_product.pk,
                    "name": child_product.name,
                    "price": str(child_product.price),
                    "amount": str(product_amount)
                })
    return JsonResponse(json.dumps(results), safe=False)