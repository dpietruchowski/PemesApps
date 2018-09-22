from django.shortcuts import render

def index(request):
  return render(request, 'home/index.html', {'search_var': 'search_list'})
