from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    c_name=models.CharField(max_length=50)
   
    def __str__(self):
        return self. c_name



class Asset(models.Model):
    SIZES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
    ]
    
    title=models.CharField(max_length=50)
    date=models.DateField(null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    qty=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    amount=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    description=models.CharField(max_length=50)  
    size = models.CharField(max_length=1, choices=SIZES)

  
    def save(self, *args, **kwargs):
        # when sale is made updaye qty and amt
        
       
       self.amount=self.qty*self.price
       
       super().save(*args,**kwargs) 
       
       

class Sale(models.Model):
    title=models.CharField(max_length=50)
    asset=models.ForeignKey(Asset,on_delete=models.CASCADE)    
    qty_sold=models.IntegerField()
    sale_qty=models.IntegerField(blank=True,null=True)
    sale_amount=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    sale_date=models.DateField()

    def __str__(self):
      
      return(f"{self.asset}")

   
    

    def update_asset_qty_amt(self):
        # when sale is made updaye qty and amt
        asset=self.asset
        
        asset.qty-=self.sale_qty
        asset.save()


class Customer(models.Model):
       GENDER = [
        ("M", "MALE"),
        ("F", "FEMALE"),
    
    ]
       first_name=models.CharField(max_length=50)
       last_name=models.CharField(max_length=50)
       user=models.ForeignKey(User,on_delete=models.CASCADE)    
       phone=models.IntegerField()
       address=models.CharField(max_length=50)
       gender = models.CharField(max_length=1, choices=GENDER)
def __str__(self):
      
      return(f"{self.user}")

class Order(models.Model):
      
       customer=models.ForeignKey(User,on_delete=models.CASCADE)  
       sale=models.ManyToManyField(Sale)   
       order_date=models.DateField()
      
def __str__(self):
      
      return(f"{self.customer}{self.sale}")




       
    

   
      
