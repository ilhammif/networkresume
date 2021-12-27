from django.shortcuts import render
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden,HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.views.generic import (ListView,DetailView,FormView,UpdateView,DeleteView,CreateView)
from django.urls import reverse
from . import models #excel_meas, meas_4g, meas_3G, meas_2G
from .forms import (Summary_All_Program_form,Summary_All_Program_Checker_form,SAP_Filter_form)
import pandas as pd
from .processing import SAP_Filter
from io import BytesIO
# Create your views here.

class Summary_All_Program(ListView):
    context_object_name = 'Summary_All_Program'
    model = models.Summary_All_Program
    template_name = 'Summary_All_Program/Summary_All_Program_list.html'
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '2021')
        new_context = models.Summary_All_Program.objects.filter(
            Year=filter_val)
        return new_context

class Summary_All_Program_DetailViews(DetailView):
    model = models.Summary_All_Program
    context_object_name = 'Summary_All_Program_details'
    template_name = 'Summary_All_Program/Summary_All_Program_detail.html'

class Summary_All_Program_CreateView(FormView):
    form_class= Summary_All_Program_form
    models = models.Summary_All_Program
    template_name ='Summary_All_Program/Upload_Summary_All_Program.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('Summary_All_Program:home'))
        else:
            return render(request, self.template_name, {'form': form})


class Summary_All_Program_UpdateView(UpdateView):
    form_class = Summary_All_Program_form
    model = models.Summary_All_Program
    context_object_name = 'Summary_All_Program_update'
    template_name ='Summary_All_Program/Update_Summary_All_Program.html'


class Summary_All_Program_DeleteView(DeleteView):
    template_name = 'Summary_All_Program/Delete_Summary_All_Program.html'
    # specify the model you want to use
    model = models.Summary_All_Program
    # can specify success url
    # url to redirect after successfully
    # deleting object
    def get_success_url(self):
        return reverse('Summary_All_Program:home')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(Summary_All_Program_DeleteView, self).post(request, *args, **kwargs)


class SAP_Filter_Processing(CreateView):
    form_class = Summary_All_Program_Checker_form
    model = models.Summary_All_Program_Checker
    template_name = 'Summary_All_Program/SAP_Filter_processing.html'
    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        form.fields['summary_all_program'].queryset = form.fields['summary_all_program'].queryset.order_by('-summary_all_program')
        form.fields['SAP_Filter'].queryset = form.fields['SAP_Filter'].queryset.order_by('-SAP_Filter')
        return form
    
    def form_valid(self,form):
        df = SAP_Filter(form)
        cptls0 = df[0]
        cptls = df[1]
        dfsow3 = df[2]
        week = form.cleaned_data['Week']
        if week > 9  :
            wk = "W"+str(week)
        elif week > 0:
            wk = "W0"+str(week)
        year = form.cleaned_data['Year']

        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            sheetname1 = 'Filter'
            cptls0.to_excel(writer, sheet_name = sheetname1, index=False)
            sheetname2 = 'Processed Filter'
            cptls.to_excel(writer, sheet_name = sheetname2, index=False)
            sheetname3 = 'SOW Check Result'
            dfsow3.to_excel(writer, sheet_name = sheetname3, index=False)
            writer.save()

            # Set up the Http response.
            filename = 'Filter Summary All Program {}-{} .xlsx'.format(year, wk)
            response = HttpResponse(
                b.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            response['Location'] = reverse('summary_all_program:home')
            return response


class SAP_Filter_List_View(ListView):
    context_object_name = 'SAP_Filter'
    model = models.SAP_Filter
    template_name = 'Summary_All_Program/SAP_Filter_list.html'
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '2021')
        new_context = models.SAP_Filter.objects.filter(
            Year=filter_val)
        return new_context

class SAP_Filter_DetailViews(DetailView):
    model = models.SAP_Filter
    context_object_name = 'SAP_Filter_details'
    template_name = 'Summary_All_Program/SAP_Filter_detail.html'

class SAP_Filter_CreateView(FormView):
    form_class= SAP_Filter_form
    models = models.SAP_Filter
    template_name ='Summary_All_Program/Upload_SAP_Filter.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('Summary_All_Program:homef'))
        else:
            return render(request, self.template_name, {'form': form})


class SAP_Filter_UpdateView(UpdateView):
    form_class = SAP_Filter_form
    model = models.SAP_Filter
    context_object_name = 'SAP_Filter_UpdateView'
    template_name ='Summary_All_Program/Update_SAP_Filter.html'


class SAP_Filter_DeleteView(DeleteView):
    template_name = 'Summary_All_Program/Delete_SAP_Filter.html'
    # specify the model you want to use
    model = models.SAP_Filter
    # can specify success url
    # url to redirect after successfully
    # deleting object
    def get_success_url(self):
        return reverse('Summary_All_Program:homef')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(SAP_Filter_DeleteView, self).post(request, *args, **kwargs)
