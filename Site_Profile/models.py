import os
from django.db import models
from django.utils.timezone import now
from django.dispatch import receiver
from django.urls import reverse
# Create your models here.
class Site_Profile(models.Model):
    Week = models.PositiveIntegerField(null=True,name='Week')
    Year = models.PositiveIntegerField(null=True,name='Year', default= now().year)
    site_id_profile = models.FileField(upload_to = 'Site_ID_Profile')
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
        return reverse("site_profile:detail",kwargs={'pk':self.pk})

@receiver(models.signals.post_delete, sender=Site_Profile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.site_id_profile:
        if os.path.isfile(instance.site_id_profile.path):
            os.remove(instance.site_id_profile.path)

@receiver(models.signals.pre_save, sender=Site_Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Site_Profile.objects.get(pk=instance.pk).site_id_profile
    except Site_Profile.DoesNotExist:
        return False

    new_file = instance.site_id_profile
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

"""
class SiteID(models.Model):
    site_id = models.CharField(max_length=10) # max length was 6
    site_name = models.CharField(max_length=60,null=True,blank=True) # max length was 40
    branch = models.CharField(max_length=20) # max length was 8
    cluster_sales = models.CharField(max_length=30,null=True,blank=True) # max length was 17
    city = models.CharField(max_length=30,null=True,blank=True) # max length was 21
    long = models.FloatField() # min: 126.292, max: 141.00686000000002, mean: 134.60452992646776
    lat = models.FloatField() # min: -8.569422, max: -0.412199, mean: -3.3654660085415817
    inner__outer = models.CharField(max_length=10,null=True,blank=True) # max length was 5
    date = models.DateTimeField(auto_now=True)
    Year_Week= models.CharField(max_length=7, null=True, unique= True, blank=True)

    def save(self,*args,**kwargs):
        
            if self.Week < 10:
                wk = "W0" + str(self.Week)
            else:
                wk = "W" + str(self.Week)
            self.Year_Week = "{} - {}".format(self.Year, wk)
            super().save(*args,**kwargs)


    def __str__(self):
        return str(self.Year_Week)
""" 
