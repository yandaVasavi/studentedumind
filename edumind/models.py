from django.db import models
from django.contrib.auth.models import User


class UserStudyProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='study_profile'
    )

    study_sessions = models.PositiveIntegerField(default=0)
    completed_quizzes = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username