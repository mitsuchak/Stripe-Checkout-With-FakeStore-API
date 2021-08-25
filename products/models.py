from django.db import models

# Create your models here.
class  Stripe_Data(models.Model) :
    model_email  = models.EmailField(max_length=500)
    model_paymment_status = models.CharField(max_length=500)
    model_transaction_id = models.CharField(max_length=500)
    model_price = models.FloatField()
    model_image = models.ImageField()