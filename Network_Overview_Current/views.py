from django.utils.timezone import now
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import (ListView,DetailView,FormView,UpdateView,DeleteView)
from django.urls import reverse
from . import models
from .forms import (NOC_Processing_form,)
# Create your views here.

class Network_Overview_Current(ListView):
    context_object_name = 'Network_Overview_Current'
    model = models.NOC_Processing
    template_name = 'Network_Overview_Current/Network_Overview_Current_list.html'
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', now().year)
        new_context = models.NOC_Processing.objects.filter(
            Year=filter_val)
        return new_context

class Network_Overview_Current_DetailViews(DetailView):
    model = models.NOC_Processing
    context_object_name = 'Network_Overview_Current_details'
    template_name = 'Network_Overview_Current/Network_Overview_Current_detail.html'

class Network_Overview_Current_CreateView(FormView):
    form_class= NOC_Processing_form
    models = models.NOC_Processing
    template_name ='Network_Overview_Current/Upload_Network_Overview_Current.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('Network_Overview_Current:home'))
        else:
            return render(request, self.template_name, {'form': form})


class Network_Overview_Current_UpdateView(UpdateView):
    form_class = NOC_Processing_form
    model = models.NOC_Processing
    context_object_name = 'Network_Overview_Current_update'
    template_name ='Network_Overview_Current/Update_Network_Overview_Current.html'


class Network_Overview_Current_DeleteView(DeleteView):
    template_name = 'Network_Overview_Current/Delete_Network_Overview_Current.html'
    # specify the model you want to use
    model = models.NOC_Processing
    # can specify success url
    # url to redirect after successfully
    # deleting object
    def get_success_url(self):
        return reverse('Network_Overview_Current:home')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(Network_Overview_Current_DeleteView, self).post(request, *args, **kwargs)
    
# Create your views here.
