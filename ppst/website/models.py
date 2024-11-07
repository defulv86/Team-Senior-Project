from django.db import models
import random
import string
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


def generate_link():
    random_string = ''.join(random.choices(string.ascii_letters, k=6))
    return random_string  # Only return the random string

class Test(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('invalid', 'Invalid')
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    link = models.CharField(default=generate_link, max_length=100, null=True)
    created_at = models.DateTimeField(null=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    age = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    premature_exit = models.BooleanField(default=False)  # New field to mark premature exit

    def check_status(self):
        """Update the status based on test conditions."""
        if self.is_invalid:
            self.status = 'invalid'
        elif self.finished_at:
            self.status = 'completed'
        else:
            self.status = 'pending'
        self.save()

    @property
    def is_invalid(self):
        """Determine if a test should be invalid based on conditions."""
        expiration_date = self.created_at + timedelta(weeks=1)
        return timezone.now() >= expiration_date or self.premature_exit
    
    def  __str__(self):
        return f"Test Link: {self.link}, Administerd By: {self.user}, Status: {self.status}"


class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    
    # Store latencies and accuracies in JSON format
    character_latencies = models.JSONField(default=dict, blank=True)  # Format: {position: [latency1, latency2, ...]}
    character_accuracies = models.JSONField(default=dict, blank=True)  # Format: {position: [accuracy1, accuracy2, ...]}

    amount_correct = models.IntegerField(default=0)

    def __str__(self):
        return self.test.link

class Stimulus_Type(models.Model):
    stimulus_type = models.CharField(max_length=15, default='')

    def __str__(self):
        return self.stimulus_type

class Stimulus(models.Model):
    stimulus_content = models.CharField(max_length=6)
    stimulus_type = models.ForeignKey(Stimulus_Type, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.stimulus_content} ({self.stimulus_type})"

class Response(models.Model):
    response = models.CharField(max_length=5, default='')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    time_submitted = models.DateTimeField(null=True)
    response_position = models.IntegerField(default=0)
    stimulus = models.ForeignKey(Stimulus, on_delete=models.CASCADE, default=1)
    
    def  __str__(self):
        return self.test.link + " Response number: " + str(self.response_position)

class Aggregate(models.Model):
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    # Store average latencies and accuracies for different metrics in JSON format
    average_latencies = models.JSONField(default=dict, blank=True)  # e.g., {'fourdigit_1': 140, 'fivedigit_1': 190, ...}
    average_accuracies = models.JSONField(default=dict, blank=True)  # e.g., {'fourdigit_1': 0.79, 'fivedigit_1': 0.68, ...}

    def __str__(self):
        return f"Age Group: {self.min_age}-{self.max_age}"

    def get_metric_average(self, metric_name):
        """
        Retrieve the average accuracy and latency for a specified metric, if available.
        """
        accuracy = self.average_accuracies.get(metric_name)
        latency = self.average_latencies.get(metric_name)
        return {"accuracy": accuracy, "latency": latency}


# Ticket model.
class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Issue'),
        ('technical', 'Technical'),
        ('account', 'Account Management'),
        ('bug/error', 'Bug/Error Report'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.category} by {self.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, default=1)
    header = models.CharField(max_length=50)
    message = models.CharField(max_length=100)
    time_created = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def  __str__(self):
        return   str(self.id) + " Header: " + self.header + " | Test: " + self.test.link + " | " + str(self.time_created)
