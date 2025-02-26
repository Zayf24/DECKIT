from django.db import models
from django.conf import settings

class Deck(models.Model):
    THEME_CHOICES = (
        ('default', 'Default'),
        ('sunrise', 'Sunrise'),
        ('tropical', 'Tropical'),
        ('ocean', 'Ocean'),
        ('lavender', 'Lavender')
        # Additional themes can be added here.
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='decks')
    name = models.CharField(max_length=255)
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='default')
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(null=True, blank=True)  # New field to record last access time
    views = models.PositiveIntegerField(default=0)  # New field to count accesses

    
    def __str__(self):
        return self.name

class Flashcard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='flashcards')
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)  # Used to keep track of flashcard order.

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
