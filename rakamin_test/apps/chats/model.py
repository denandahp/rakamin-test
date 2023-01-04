from django.db import models

from rakamin_test.apps.users.model import users


class messages(models.Model):
    sender = models.ForeignKey(users, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(users, on_delete=models.CASCADE, related_name='receiver')
    reply_from = models.IntegerField(blank=True, null=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.sender} to {self.receiver}"


class room(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    user1 = models.ForeignKey(users, related_name='user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(users, related_name='user2', on_delete=models.CASCADE)
    is_deleted_user1 = models.BooleanField(default=False)
    is_deleted_user2 = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"Room {self.user1} - {self.user2}"
