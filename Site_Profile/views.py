import os
from django.db.models.fields import Field
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden,HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import (ListView,DetailView,FormView,UpdateView,DeleteView)
from django.urls import reverse
from . import models #excel_meas, meas_4g, meas_3G, meas_2G
from .forms import (Site_Profile_form,)
# Create your views here.

class Site_Profile(ListView):
    context_object_name = 'Site_Profile'
    model = models.Site_Profile
    template_name = 'Site_Profile/Site_Profile_list.html'
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '2021')
        new_context = models.Site_Profile.objects.filter(
            Year=filter_val)
        return new_context

class Site_Profile_DetailViews(DetailView):
    model = models.Site_Profile
    context_object_name = 'Site_Profile_details'
    template_name = 'Site_Profile/Site_Profile_detail.html'

class Site_Profile_CreateView(FormView):
    form_class= Site_Profile_form
    models = models.Site_Profile
    template_name ='Site_Profile/Upload_Site_Profile.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('Site_Profile:home'))
        else:
            return render(request, self.template_name, {'form': form})


class Site_Profile_UpdateView(UpdateView):
    form_class = Site_Profile_form
    model = models.Site_Profile
    context_object_name = 'Site_Profile_update'
    template_name ='Site_Profile/Update_Site_Profile.html'


class Site_Profile_DeleteView(DeleteView):
    template_name = 'Site_Profile/Delete_Site_Profile.html'
    # specify the model you want to use
    model = models.Site_Profile
    # can specify success url
    # url to redirect after successfully
    # deleting object
    def get_success_url(self):
        return reverse('Site_Profile:home')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(Site_Profile_DeleteView, self).post(request, *args, **kwargs)
    