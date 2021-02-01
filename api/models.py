from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000, blank=True)
    type = models.CharField(max_length=128)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='author_project')
    contributor = models.ManyToManyField(User)


class Issue(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1000, blank=True)
    priority = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='auteur_issue')
    user_assigner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='assigner')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='issues')


class Comments(models.Model):
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='auteur_comments')
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)

