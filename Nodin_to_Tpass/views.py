from django.utils.timezone import now
from django.http.response import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import (ListView,DetailView,FormView,UpdateView,DeleteView)
from django.urls import reverse
from . import models
from .forms import (Nodin_To_Tpass_form,)
# Create your views here.

class Nodin_To_Tpass(ListView):
    context_object_name = 'Nodin_To_Tpass'
    model = models.Nodin_To_Tpass
    template_name = 'Nodin_to_Tpass/Nodin_To_Tpass_list.html'
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', now().year)
        new_context = models.Nodin_To_Tpass.objects.filter(
            Year=filter_val)
        return new_context

class Nodin_To_Tpass_DetailViews(DetailView):
    model = models.Nodin_To_Tpass
    context_object_name = 'Nodin_To_Tpass_details'
    template_name = 'Nodin_to_Tpass/Nodin_To_Tpass_detail.html'

class Nodin_To_Tpass_CreateView(FormView):
    form_class= Nodin_To_Tpass_form
    models = models.Nodin_To_Tpass
    template_name ='Nodin_to_Tpass/Upload_Nodin_To_Tpass.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('Nodin_To_Tpass:home'))
        else:
            return render(request, self.template_name, {'form': form})


class Nodin_To_Tpass_UpdateView(UpdateView):
    form_class = Nodin_To_Tpass_form
    model = models.Nodin_To_Tpass
    context_object_name = 'Nodin_To_Tpass_update'
    template_name ='Nodin_to_Tpass/Update_Nodin_To_Tpass.html'


class Nodin_To_Tpass_DeleteView(DeleteView):
    template_name = 'Nodin_to_Tpass/Delete_Nodin_To_Tpass.html'
    # specify the model you want to use
    model = models.Nodin_To_Tpass
    # can specify success url
    # url to redirect after successfully
    # deleting object
    def get_success_url(self):
        return reverse('Nodin_To_Tpass:home')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(Nodin_To_Tpass_DeleteView, self).post(request, *args, **kwargs)
    
# Create your views here.
