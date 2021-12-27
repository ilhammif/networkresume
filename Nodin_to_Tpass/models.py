import os
from django.db import models
from django.utils.timezone import now
from django.utils import dateformat
from django.urls import reverse
from django.dispatch import receiver
from django.core.files import File
from Nodin import models as Nodin_models
from RNC import models as RNC_models
from .processing import nodin_to_atoll
# Create your models here.

class Nodin_To_Tpass(models.Model):
    Name = models.CharField(max_length=500,null=True,blank=True)
    RNC_fields = models.ForeignKey(RNC_models.RNC,related_name='RNC1',on_delete = models.CASCADE)
    Nodin_fields = models.ForeignKey(Nodin_models.Nodin,related_name="Nodin1", on_delete = models.CASCADE)
    tpass_fields = models.FileField(upload_to='Tpass',blank=True)
    date = models.DateTimeField(auto_now=True,null=False,blank=False)
    Week = models.PositiveIntegerField(null=True,name='Week')
    Year = models.PositiveIntegerField(null=True,name='Year', default= now().year)


    def save(self,*args,**kwargs):
        strdatenow = dateformat.format(now(), 'Y-m-d H:i:s')
        self.date_field = now()
        RNC = self.RNC_fields
        Nodin =self.Nodin_fields
        file = nodin_to_atoll(Nodin,RNC)
        file_name = file[0]
        file_path = file[1]
        local_file = open(file_path, 'rb')
        with local_file as f:
            self.tpass_fields.save(file_name, File(f),save=False)
        os.remove(file_path)
        self.Name = "{} - {}".format(file_name[:-5], strdatenow)
        super().save(*args,**kwargs)


    def __str__(self):
        return str(self.pk)

@receiver(models.signals.post_delete, sender=Nodin_To_Tpass)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.tpass_fields:
        if os.path.isfile(instance.tpass_fields.path):
            os.remove(instance.tpass_fields.path)

@receiver(models.signals.pre_save, sender=Nodin_To_Tpass)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Nodin_To_Tpass.objects.get(pk=instance.pk).tpass_fields
    except Nodin_To_Tpass.DoesNotExist:
        return False

    new_file = instance.tpass_fields
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)