from django.db import models

# Create your models here.

class User(models.Model):
    ip = models.CharField(max_length=200, verbose_name='عنوان الشبكة')
    limit = models.IntegerField(default=1, verbose_name='الحد الأقصى للطلبات')


class Subscription(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'معلق'),
        ('completed', 'مكتمل')
        ]
    id=models.CharField(max_length=200, verbose_name='معرف المستخدم',primary_key=True)
    token = models.CharField(max_length=120,verbose_name="Token")
    isUsed = models.BooleanField(default=True,verbose_name="مستخدم")
    payment_status = models.CharField(default='pending',max_length=20, choices=PAYMENT_STATUS_CHOICES, verbose_name="حالة الدفع")



class Blog(models.Model):
    blog_title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blog_title