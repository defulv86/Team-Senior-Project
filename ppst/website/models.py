from django.db import models
import random
import string

class User(models.Model):
    uname = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    passwd = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    permission_lvl = models.IntegerField(default=0)

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
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    age = models.IntegerField(default=0)
    
    def __str__(self):
        return self.link

class Result(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    ans1 = models.CharField(max_length=6,default='')
    latency1 = models.IntegerField(default=0)
    ans2 = models.CharField(max_length=6,default='')
    latency2 = models.IntegerField(default=0)
    ans3 = models.CharField(max_length=6,default='')
    latency3 = models.IntegerField(default=0)
    ans4 = models.CharField(max_length=6,default='')
    latency4 = models.IntegerField(default=0)
    ans5 = models.CharField(max_length=6,default='')
    latency5 = models.IntegerField(default=0)
    ans6 = models.CharField(max_length=6,default='')
    latency6 = models.IntegerField(default=0)
    amount_correct = models.IntegerField(default=0)

class Stimulus(models.Model):
    order = models.IntegerField(default=0)
    stimulus_content = models.CharField(max_length=6)
    stimulus_type = models.CharField(max_length=15,default='')

class Response(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    time_submitted = models.DateTimeField(null=True)
    response_posistion = models.IntegerField(default=0)
    stimulus = models.ForeignKey(Stimulus, on_delete=models.CASCADE, default=1)

class Aggreagate(models.Model):
    age_group = models.CharField(max_length=10)
    avg_latency1 = models.IntegerField(default=0)
    avg_latency2 = models.IntegerField(default=0)
    avg_latency3 = models.IntegerField(default=0)
    avg_latency4 = models.IntegerField(default=0)
    avg_latency5 = models.IntegerField(default=0)
    avg_latency6 = models.IntegerField(default=0)
