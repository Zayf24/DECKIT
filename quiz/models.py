from django.db import models
from django.contrib.auth.models import User
from flashcard.models import Deck
from django.conf import settings

class Quiz(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quizzes")
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="quizzes")
    score = models.IntegerField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.deck.name} - {self.score}/{self.total_questions}"
    

