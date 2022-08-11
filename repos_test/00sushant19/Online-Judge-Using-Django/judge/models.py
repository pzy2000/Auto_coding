
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class problem(models.Model):
    name=models.TextField()
    statement = models.TextField()
    difficulty=models.TextField()
    time_limit=models.FloatField(null=True)


class solution(models.Model):
    #submitter = models.ForeignKey(coder, on_delete=models.CASCADE,null=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    submitter = models.TextField(null=True)
    curr_problem=models.ForeignKey(problem, on_delete=models.CASCADE, null=True)
    verdict=models.TextField(null=True)
    time_of_submit = models.DateTimeField(auto_now=True)
    code=models.TextField(null=True, blank=True)
    def __str__(self):
        return str(self.id)
    

class testcase(models.Model):
    curr_problem=models.ForeignKey(problem, on_delete=models.CASCADE,null=True)
    input=models.TextField()
    output=models.TextField()
