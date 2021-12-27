from django.utils.timezone import now
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import (ListView,DetailView,FormView,UpdateView,DeleteView)
from django.urls import reverse
from . import models
from .forms import (RNC_form,)
# Create your views here.

class RNC(ListView):
    context_object_name = 'RNC'
    model = models.RNC
    template_name = 'RNC/RNC_list.html'
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', now().year)
        new_context = models.RNC.objects.filter(
            Year=filter_val)
        return new_context

class RNC_DetailViews(DetailView):
    model = models.RNC
    context_object_name = 'RNC_details'
    template_name = 'RNC/RNC_detail.html'

class RNC_CreateView(FormView):
    form_class= RNC_form
    models = models.RNC
    template_name ='RNC/Upload_RNC.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('RNC:home'))
        else:
            return render(request, self.template_name, {'form': form})


class RNC_UpdateView(UpdateView):
    form_class = RNC_form
    model = models.RNC
    context_object_name = 'RNC_update'
    template_name ='RNC/Update_RNC.html'


class RNC_DeleteView(DeleteView):
    template_name = 'RNC/Delete_RNC.html'
    # specify the model you want to use
    model = models.RNC
    # can specify success url
    # url to redirect after successfully
    # deleting object
    def get_success_url(self):
        return reverse('RNC:home')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(RNC_DeleteView, self).post(request, *args, **kwargs)
    
# Create your views here.
