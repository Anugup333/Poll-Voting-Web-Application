from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import make_naive
import datetime

# Create your models here.


class Poll(models.Model):
    question = models.CharField(max_length=255)
    close_time = models.DateTimeField()
    is_closed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def is_open(self):
        return not self.is_closed and  datetime.datetime.now() < make_naive(self.close_time) 

    def __str__(self):
        return self.question

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.poll.question} ({self.text})"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.poll.question} ({self.user.username})'
    
    class Meta:
        unique_together = ('user', 'poll')
    
    

