import os
from django.db import models
from django.utils.timezone import now
from django.utils import dateformat
from django.urls import reverse
from django.dispatch import receiver
from django.core.files import File
from Meas import models as Meas_models
from Site_Profile import models as SP_models
from .processing1 import NOC_Func
# Create your models here.

class NOC_Processing(models.Model):
    Name = models.CharField(max_length=500,null=True,blank=True)
    Year_Week = models.CharField(max_length=50,null=True,blank=True)
    lw_fields = models.ForeignKey(Meas_models.Meas,related_name='Meas1',on_delete = models.CASCADE)
    cw_fields = models.ForeignKey(Meas_models.Meas,related_name="Meas2",on_delete = models.CASCADE)
    site_profile_fields = models.ForeignKey(SP_models.Site_Profile,related_name="Meas2",on_delete = models.CASCADE)

    NOC_fields = models.FileField(upload_to='NOC',blank=True)
    date_field = models.DateTimeField(auto_now=True,null=False,blank=False)
    Week = models.PositiveIntegerField(null=True,name='Week')
    Year = models.PositiveIntegerField(null=True,name='Year', default= now().year)


    def save(self,*args,**kwargs):
        strdatenow = dateformat.format(now(), 'Y-m-d H:i:s')
        self.date_field = strdatenow
        LastWeek = self.lw_fields
        CurrentWeek =self.cw_fields
        SiteProfile = self.site_profile_fields
        file = NOC_Func(LastWeek,CurrentWeek,SiteProfile)
        if self.Week < 10:
            wk = "W0" + str(self.Week)
        else:
            wk = "W" + str(self.Week)

        file_name = 'Network Overview {}-{} Current.xlsx'.format(wk,str(self.Year))
        file_path = file[1]
        local_file = open(file_path, 'rb')
        with local_file as f:
            self.NOC_fields.save(file_name, File(f),save=False)
        os.remove(file_path)
        
        self.Name = file_name
        self.Year_Week = "{} - {}".format(self.Year, wk)
        super().save(*args,**kwargs)


    def __str__(self):
        return "{} - {}".format(self.Name[:-5], self.date_field)

@receiver(models.signals.post_delete, sender=NOC_Processing)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.NOC_fields:
        if os.path.isfile(instance.NOC_fields.path):
            os.remove(instance.NOC_fields.path)

@receiver(models.signals.pre_save, sender=NOC_Processing)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = NOC_Processing.objects.get(pk=instance.pk).NOC_fields
    except NOC_Processing.DoesNotExist:
        return False

    new_file = instance.NOC_fields
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)