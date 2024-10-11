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

    @property
    def is_authenticated(self):
        # Always return True for authenticated users
        return True

def generate_link():
    random_string = ''.join(random.choices(string.ascii_letters, k=6))
    link = f"ppst.com/{random_string}"
    return link

class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(default=generate_link ,max_length=100, null=True)
    created_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.link

class Result(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    age = models.IntegerField()
    avg_latency1 = models.IntegerField()
    avg_latency2 = models.IntegerField()
    avg_latency3 = models.IntegerField()
    avg_latency4 = models.IntegerField()
    avg_latency5 = models.IntegerField()
    avg_latency6 = models.IntegerField()
    amount_correct = models.IntegerField()

class Stimulus(models.Model):
    order = models.IntegerField()
    stimulus_content = models.CharField(max_length=6)

class Response(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    response = models.CharField(max_length=10)
    latency = models.IntegerField()
    is_correct = models.BooleanField()
    stimulus = models.ForeignKey(Stimulus, on_delete=models.CASCADE, default=1)
