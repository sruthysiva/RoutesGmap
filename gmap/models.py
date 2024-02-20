from django.db import models
from django.contrib.auth.models import User



# Create your models here.
mapbox_access_token='pk.eyJ1Ijoic3J1dGh5c2l2YWRhcyIsImEiOiJjbHJ5dDRvbGYxb2ljMmtteHhpcDY3MmxxIn0.YN98-omLBLCwOKEyM4e5qA'

class UploadedFile(models.Model):
    
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file.name
    
class profile(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class uploadedData(models.Model):
    
    column1_name = models.CharField(max_length=255, blank=True, null=True)
    column2_address = models.CharField(max_length=255, blank=True, null=True)
    column3_latitude=models.DecimalField(max_digits=9, decimal_places=6,null=True)
    column4_longitude= models.DecimalField(max_digits=9, decimal_places=6,null=True)
    column5_city = models.CharField(max_length=255, blank=True, null=True)
    column6_district = models.CharField(max_length=255, blank=True, null=True)
    column7_state = models.CharField(max_length=255, blank=True, null=True)
    column8_country = models.CharField(max_length=255, blank=True, null=True)
    column9_zipcode = models.CharField(max_length=20)
    column10_email=  models.EmailField()
    column11_phone = models.CharField(max_length=10)
    column12_category = models.CharField(max_length=255, blank=True, null=True)
    visited  = models.BooleanField(default=False)
    place_id = models.CharField(max_length=255, blank=True, null=True)

    

    
    
    



    
