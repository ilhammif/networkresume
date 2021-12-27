import os
from django.db import models
from django.utils.timezone import now
from django.utils import dateformat
from django.urls import reverse
from django.dispatch import receiver
from Nodin import models as Nodin_models
# Create your models here.

class RNC(models.Model):
    Name = models.CharField(max_length=500,null=True,blank=True,unique=True)
    RNC = models.FileField(upload_to = 'RNC')
    Year = models.PositiveIntegerField(null=True, default= now().year)
    date_field = models.DateField(auto_now=True,null=False,blank=False)

    def save(self,*args,**kwargs):
        strdatenow = dateformat.format(now(), 'Y-m-d H:i:s')
        if not self.RNC:
            self.date_field = now()
        self.Name = "{} - {}".format(self.RNC.name[:-5], strdatenow)
        super().save(*args,**kwargs)


    def __str__(self):
        return str(self.Name)
    
    def get_absolute_url(self):
        return reverse("RNC:detail",kwargs={'pk':self.pk})

@receiver(models.signals.post_delete, sender=RNC)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.RNC:
        if os.path.isfile(instance.RNC.path):
            os.remove(instance.RNC.path)

@receiver(models.signals.pre_save, sender=RNC)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = RNC.objects.get(pk=instance.pk).RNC
    except RNC.DoesNotExist:
        return False

    new_file = instance.RNC
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)