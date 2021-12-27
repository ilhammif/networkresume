import os
from django.db import models
from django.utils.timezone import now
from django.dispatch import receiver
from django.urls import reverse
# Create your models here.


class Summary_All_Program(models.Model):
    Week = models.PositiveIntegerField(null=True,name='Week')
    Year = models.PositiveIntegerField(null=True,name='Year', default= now().year)
    summary_all_program = models.FileField(upload_to = 'Summary_All_Program')
    sheetname = models.CharField(max_length=254,default='LIST',null=True,blank=True)
    Year_Week= models.CharField(max_length=20, null=True, unique= True,blank=True)
    
    def save(self,*args,**kwargs):
        
            if self.Week < 10:
                wk = "W0" + str(self.Week)
            else:
                wk = "W" + str(self.Week)
            self.Year_Week = "{} - {}".format(self.Year, wk)
            super().save(*args,**kwargs)


    def __str__(self):
        return str(self.Year_Week)
    
    def get_absolute_url(self):
        return reverse("summary_all_program:detail",kwargs={'pk':self.pk})
@receiver(models.signals.post_delete, sender=Summary_All_Program)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.summary_all_program:
        if os.path.isfile(instance.summary_all_program.path):
            os.remove(instance.summary_all_program.path)

@receiver(models.signals.pre_save, sender=Summary_All_Program)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Summary_All_Program.objects.get(pk=instance.pk).summary_all_program
    except Summary_All_Program.DoesNotExist:
        return False

    new_file = instance.summary_all_program
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class SAP_Filter(models.Model):
    # not done yet
    Week = models.PositiveIntegerField(null=True)
    Year = models.PositiveIntegerField(null=True, default= now().year)
    date = models.DateTimeField(auto_now=True)
    SAP_Filter = models.FileField(upload_to = 'SAP_Filter1')
    Year_Week= models.CharField(max_length=7, null=True, unique= True,blank=True)

    def save(self,*args,**kwargs):
    
        if self.Week < 10:
            wk = "W0" + str(self.Week)
        else:
            wk = "W" + str(self.Week)
        self.Year_Week = "{} - {}".format(self.Year, wk)
        super().save(*args,**kwargs)

    def __str__(self):
        return str(self.Year_Week)

    
    def get_absolute_url(self):
        return reverse("summary_all_program:SAPC_detail",kwargs={'pk':self.pk})
@receiver(models.signals.post_delete, sender=SAP_Filter)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.SAP_Filter:
        if os.path.isfile(instance.SAP_Filter.path):
            os.remove(instance.SAP_Filter.path)

@receiver(models.signals.pre_save, sender=SAP_Filter)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = SAP_Filter.objects.get(pk=instance.pk).SAP_Filter
    except SAP_Filter.DoesNotExist:
        return False

    new_file = instance.SAP_Filter
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class Summary_All_Program_Checker(models.Model):
    # not done yet
    summary_all_program = models.ForeignKey(Summary_All_Program, related_name='Summary_All_Program1',on_delete = models.CASCADE)
    SAP_Filter = models.ForeignKey(SAP_Filter, related_name='SAP_Filter1',on_delete = models.CASCADE)
    Week = models.PositiveIntegerField(null=True)
    Year = models.PositiveIntegerField(null=True, default= now().year)
    date = models.DateTimeField(auto_now=True)
    Year_Week= models.CharField(max_length=7, null=True,blank=True)

    
    def __str__(self):
        return str(self.Year_Week)
    
    def save(self,*args,**kwargs):
    
        if self.Week < 10:
            wk = "W0" + str(self.Week)
        else:
            wk = "W" + str(self.Week)
        self.Year_Week = "{} - {}".format(self.Year, wk)
        super().save(*args,**kwargs)

    def __str__(self):
        return str(self.Year_Week)
