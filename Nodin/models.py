import os
from django.db import models
from django.utils.timezone import now
from django.utils import dateformat
from django.urls import reverse
from django.dispatch import receiver
# Create your models here.

class Nodin(models.Model):
    Name = models.CharField(max_length=500,null=True,blank=True,unique=True)
    Nodin = models.FileField(upload_to = 'Nodin')
    Year = models.PositiveIntegerField(null=True, default= now().year)
    date_field = models.DateField(auto_now=True,null=False,blank=False)

    def save(self,*args,**kwargs):
            strdatenow = dateformat.format(now(), 'Y-m-d H:i:s')
            if not self.Nodin:
                 self.date_field = now()
            self.Name = "{} - {}".format(self.Nodin.name[:-5], strdatenow)
            super().save(*args,**kwargs)


    def __str__(self):
        return str(self.Name)
    
    def get_absolute_url(self):
        return reverse("Nodin:detail",kwargs={'pk':self.pk})

@receiver(models.signals.post_delete, sender=Nodin)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.Nodin:
        if os.path.isfile(instance.Nodin.path):
            os.remove(instance.Nodin.path)

@receiver(models.signals.pre_save, sender=Nodin)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Nodin.objects.get(pk=instance.pk).Nodin
    except Nodin.DoesNotExist:
        return False

    new_file = instance.Nodin
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)