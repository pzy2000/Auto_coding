from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
# Create your views here.

class PostIndex(ListView):
    pass

class PostBusca(PostIndex):
    pass

class PostCategorias(PostIndex):
    pass

class PostDetalhes(UpdateView):
    pass
