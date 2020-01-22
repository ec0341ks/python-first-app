from django.contrib.auth.models import User
from django.db import models


class List(models.Model):
    title = models.CharField(max_length=200)
    # on_deleteは、ユーザー削除時にリストも同時に削除する動作
    user = models.ForeignKey(User, on_delete=models.CASCADE)
