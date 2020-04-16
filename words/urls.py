from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getWords', views.getWords, name='getWords'),
    path('query', views.queryWord, name='query'),
    path('getUnit', views.getUnit, name='getUnit'),
    path('makeAnkiCards', views.makeForAnki, name='makeAnkiCards'),
    path('makeLatexs', views.makeLatex, name='makeLatexs'),
]