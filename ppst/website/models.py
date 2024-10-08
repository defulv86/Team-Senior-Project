from django.db import models
import random
import string

class User(models.Model):
    uname = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    passwd = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    permission_lvl = models.IntegerField()

    def __str__(self):
        return self.uname

def generate_link():
    random_string = ''.join(random.choices(string.ascii_letters, k=6))
    link = f"ppst.com/{random_string}"
    return link

class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(default=generate_link(),max_length=100, null=True)
    created_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True)
