from django.shortcuts import render
from django.views.generic import TemplateView, ListView,DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Translation

def ViewForMain(request):
    return render(request, template_name = 'WordBase/main_page.html')
def mainbase(request):
    return render(request, template_name='WordBase/Base.html')

class ListBaseView(ListView):
    template_name = 'WordBase/base_word_list.html'
    model = Translation
    context_object_name = 'translate'
class CreateBaseView(CreateView):
    template_name = 'WordBase/create_word.html'
    model = Translation
    fields = ('russian_word',)
    success_url = reverse_lazy('list_base')
class DetailBaseView(DetailView):
    template_name = 'WordBase/detail_word.html'
    model = Translation
    context_object_name = 'translate'
class DeleteBaseView(DeleteView):
    template_name = 'WordBase/delete_word.html'
    model = Translation
    success_url = reverse_lazy('list_base')
class UpdateBaseView(UpdateView):
    template_name = 'WordBase/create_word.html'
    model = Translation
    fields = 'russian_word', 'spanish_word'
    success_url = reverse_lazy('list_base')