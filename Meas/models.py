import os
from django.db import models
from django.utils.timezone import now
from django.utils import dateformat
from django.urls import reverse
from django.dispatch import receiver
# Create your models here.

class Meas(models.Model):
    Meas2G = models.FileField(upload_to = 'Meas2G')
    Meas3G = models.FileField(upload_to = 'Meas3G')
    Meas4G = models.FileField(upload_to = 'Meas4G')

    Week = models.PositiveIntegerField(null=True)
    Year = models.PositiveIntegerField(null=True, default= now().year)
    Year_Week= models.CharField(max_length=20,null=True, unique= True, blank=True)
    date_field = models.DateField(auto_now=True,null=False,blank=False)

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
        return reverse("Meas:detail",kwargs={'pk':self.pk})

@receiver(models.signals.post_delete, sender=Meas)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.Meas2G:
        if os.path.isfile(instance.Meas2G.path):
            os.remove(instance.Meas2G.path)
    if instance.Meas3G:
        if os.path.isfile(instance.Meas3G.path):
            os.remove(instance.Meas3G.path)
    if instance.Meas4G:
        if os.path.isfile(instance.Meas4G.path):
            os.remove(instance.Meas4G.path)

@receiver(models.signals.pre_save, sender=Meas)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old2G_file = Meas.objects.get(pk=instance.pk).Meas2G
        old3G_file = Meas.objects.get(pk=instance.pk).Meas3G
        old4G_file = Meas.objects.get(pk=instance.pk).Meas4G
    except Meas.DoesNotExist:
        return False

    new2G_file = instance.Meas2G
    if not old2G_file == new2G_file:
        if os.path.isfile(old2G_file.path):
            os.remove(old2G_file.path)
    new3G_file = instance.Meas3G
    if not old3G_file == new3G_file:
        if os.path.isfile(old3G_file.path):
            os.remove(old3G_file.path)
    new4G_file = instance.Meas4G
    if not old4G_file == new4G_file:
        if os.path.isfile(old4G_file.path):
            os.remove(old4G_file.path)