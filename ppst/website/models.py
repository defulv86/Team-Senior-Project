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
    # four didget stats
    fourdigit_accuracy_1 = models.FloatField(default=0,null=True)
    fourdigit_latency_1 = models.IntegerField(default=0)
    fourdigit_accuracy_2 = models.FloatField(default=0,null=True)
    fourdigit_latency_2 = models.IntegerField(default=0)
    fourdigit_accuracy_3 = models.FloatField(default=0,null=True)
    fourdigit_latency_3 = models.IntegerField(default=0)
    # five didgit stats
    fivedigit_accuracy_1 = models.FloatField(default=0,null=True)
    fivedigit_latency_1 = models.IntegerField(default=0)
    fivedigit_accuracy_2 = models.FloatField(default=0,null=True)
    fivedigit_latency_2 = models.IntegerField(default=0)
    fivedigit_accuracy_3 = models.FloatField(default=0,null=True)
    fivedigit_latency_3 = models.IntegerField(default=0)
    # four mixed stats
    fourmixed_accuracy_1 = models.FloatField(default=0,null=True)
    fourmixed_latency_1 = models.IntegerField(default=0)
    fourmixed_accuracy_2 = models.FloatField(default=0,null=True)
    fourmixed_latency_2 = models.IntegerField(default=0)
    fourmixed_accuracy_3 = models.FloatField(default=0,null=True)
    fourmixed_latency_3 = models.IntegerField(default=0)
    # five mixed stats
    fivemixed_accuracy_1 = models.FloatField(default=0,null=True)
    fivemixed_latency_1 = models.IntegerField(default=0)
    fivemixed_accuracy_2 = models.FloatField(default=0,null=True)
    fivemixed_latency_2 = models.IntegerField(default=0)
    fivemixed_accuracy_3 = models.FloatField(default=0,null=True)
    fivemixed_latency_3 = models.IntegerField(default=0)
    amount_correct = models.IntegerField(default=0)

    def  __str__(self):
        return self.test.link

class Stimulus_Type(models.Model):
    stimulus_type = models.CharField(max_length=15, default='')
    
    def  __str__(self):
        return self.stimulus_type

class Stimulus(models.Model):
    stimulus_content = models.CharField(max_length=6)
    stimulus_type = models.ForeignKey(Stimulus_Type, on_delete=models.CASCADE, default=1)

    def  __str__(self):
        return self.stimulus_content + " " + self.stimulus_type.stimulus_type


class Response(models.Model):
    response = models.CharField(max_length=5, default='')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    time_submitted = models.DateTimeField(null=True)
    response_posistion = models.IntegerField(default=0)
    stimulus = models.ForeignKey(Stimulus, on_delete=models.CASCADE, default=1)

class Aggreagate(models.Model):
    age_group = models.CharField(max_length=10)

    # avg four didget stats
    avg_fourdigit_accuracy_1 = models.FloatField(default=0,null=True)
    avg_fourdigit_latency_1 = models.IntegerField(default=0)
    avg_fourdigit_accuracy_2 = models.FloatField(default=0,null=True)
    avg_fourdigit_latency_2 = models.IntegerField(default=0)
    avg_fourdigit_accuracy_3 = models.FloatField(default=0,null=True)
    avg_fourdigit_latency_3 = models.IntegerField(default=0)
    # avg five didgit stats
    avg_fivedigit_accuracy_1 = models.FloatField(default=0,null=True)
    avg_fivedigit_latency_1 = models.IntegerField(default=0)
    avg_fivedigit_accuracy_2 = models.FloatField(default=0,null=True)
    avg_fivedigit_latency_2 = models.IntegerField(default=0)
    avg_fivedigit_accuracy_3 = models.FloatField(default=0,null=True)
    avg_fivedigit_latency_3 = models.IntegerField(default=0)
    # avg four mixed stats
    avg_fourmixed_accuracy_1 = models.FloatField(default=0,null=True)
    avg_fourmixed_latency_1 = models.IntegerField(default=0)
    avg_fourmixed_accuracy_2 = models.FloatField(default=0,null=True)
    avg_fourmixed_latency_2 = models.IntegerField(default=0)
    avg_fourmixed_accuracy_3 = models.FloatField(default=0,null=True)
    avg_fourmixed_latency_3 = models.IntegerField(default=0)
    # avg five mixed stats
    avg_fivemixed_accuracy_1 = models.FloatField(default=0,null=True)
    avg_fivemixed_latency_1 = models.IntegerField(default=0)
    avg_fivemixed_accuracy_2 = models.FloatField(default=0,null=True)
    avg_fivemixed_latency_2 = models.IntegerField(default=0)
    avg_fivemixed_accuracy_3 = models.FloatField(default=0,null=True)
    avg_fivemixed_latency_3 = models.IntegerField(default=0)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    header = models.CharField(max_length=50)
    message = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now=True)
    is_dismissed = models.BooleanField(default=False)