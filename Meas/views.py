from django.utils.timezone import now
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import (ListView,DetailView,FormView,UpdateView,DeleteView)
from django.urls import reverse
from . import models
from .forms import (Meas_form,)

class Meas(ListView):
    context_object_name = 'Meas'
    model = models.Meas
    template_name = 'Meas/Meas_list.html'
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', now().year)
        new_context = models.Meas.objects.filter(
            Year=filter_val)
        return new_context

class Meas_DetailViews(DetailView):
    model = models.Meas
    context_object_name = 'Meas_details'
    template_name = 'Meas/Meas_detail.html'

class Meas_CreateView(FormView):
    form_class= Meas_form
    models = models.Meas
    template_name ='Meas/Upload_Meas.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('Meas:home'))
        else:
            return render(request, self.template_name, {'form': form})


class Meas_UpdateView(UpdateView):
    form_class = Meas_form
    model = models.Meas
    context_object_name = 'Meas_update'
    template_name ='Meas/Update_Meas.html'


class Meas_DeleteView(DeleteView):
    template_name = 'Meas/Delete_Meas.html'
    # specify the model you want to use
    model = models.Meas
    # can specify success url
    # url to redirect after successfully
    # deleting object
    def get_success_url(self):
        return reverse('Meas:home')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(Meas_DeleteView, self).post(request, *args, **kwargs)
   
# Create your views here.
