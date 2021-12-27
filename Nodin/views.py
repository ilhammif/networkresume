from django.utils.timezone import now
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import (ListView,DetailView,FormView,UpdateView,DeleteView)
from django.urls import reverse
from . import models
from .forms import (Nodin_form,)
# Create your views here.

class Nodin(ListView):
    context_object_name = 'nodin'
    model = models.Nodin
    template_name = 'Nodin/nodin_list.html'
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', now().year)
        new_context = models.Nodin.objects.filter(
            Year=filter_val)
        return new_context

class Nodin_DetailViews(DetailView):
    model = models.Nodin
    context_object_name = 'nodin_details'
    template_name = 'Nodin/nodin_detail.html'

class Nodin_CreateView(FormView):
    form_class= Nodin_form
    models = models.Nodin
    template_name ='Nodin/Upload_nodin.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('Nodin:home'))
        else:
            return render(request, self.template_name, {'form': form})


class Nodin_UpdateView(UpdateView):
    form_class = Nodin_form
    model = models.Nodin
    context_object_name = 'nodin_update'
    template_name ='Nodin/Update_nodin.html'


class Nodin_DeleteView(DeleteView):
    template_name = 'Nodin/Delete_nodin.html'
    # specify the model you want to use
    model = models.Nodin
    # can specify success url
    # url to redirect after successfully
    # deleting object
    def get_success_url(self):
        return reverse('Nodin:home')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(Nodin_DeleteView, self).post(request, *args, **kwargs)
    
# Create your views here.
