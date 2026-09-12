from django.db import models

from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('Dream', '💭 Dream'),
    ('Goal', '🥅 Goal'),
    ('Planned', '📋 Planned'),
    ('Preparing', '🛠️ Preparing'),
    ('InProgress', '🚶 In Progress'),
    ('GonnaComplete', '🔥 Gonna Complete'),
    ('Completed', '🎉 Completed'),
]

PRIORITY_CHOICES = [
    ('Low', '🟢 Low'),
    ('Medium', '🟡 Medium'),
    ('High', '🔴 High'),
]

MOOD_CHOICES = [
    ('Happy', '😊 Happy'),
    ('Excited', '🥰 Excited'),
    ('Amazing', '🤩 Amazing'),
    ('Peaceful', '😌 Peaceful'),
    ('Emotional', '🥹 Emotional'),
    ('Proud', '😎 Proud'),
    ('Satisfied', '🌱 Satisfied'),
]

class Shelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shelves')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default="📁")
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)  # <-- Add this field

    class Meta:
        verbose_name_plural = "Shelves"

    def __str__(self):
        return f"{self.icon} {self.name}"

class BucketItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bucket_items')
    shelf = models.ForeignKey(Shelf, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    title = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='bucket_covers/', null=True, blank=True)
    description = models.TextField(blank=True)
    why_statement = models.TextField(blank=True, help_text="Why do you want to accomplish this?")
    location = models.CharField(max_length=200, blank=True)
    target_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Dream')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='bucket_items/', blank=True, null=True)
    def __str__(self):
        return self.title

class Memory(models.Model):
    bucket_item = models.OneToOneField(BucketItem, on_delete=models.CASCADE, related_name='memory')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memories')
    story = models.TextField()
    completion_date = models.DateField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='Happy')
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Memories"

    def __str__(self):
        return f"Memory: {self.bucket_item.title}"

class MemoryPhoto(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='memory_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class FlowProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='flow_progress')
    points = models.IntegerField(default=0)
    class Meta:
        verbose_name = "Goal Progress"          # Singular name in Admin
        verbose_name_plural = "Goal Progresses"  # Plural name in Admin

    @property
    def level_info(self):
        pts = self.points
        if pts < 50:
            return {'level': 'First Drop', 'icon': '💧', 'next': 50, 'prev': 0}
        elif pts < 150:
            return {'level': 'Ripple', 'icon': '💦', 'next': 150, 'prev': 50}
        elif pts < 300:
            return {'level': 'Stream', 'icon': '🌊', 'next': 300, 'prev': 150}
        elif pts < 500:
            return {'level': 'River', 'icon': '🏞️', 'next': 500, 'prev': 300}
        elif pts < 1000:
            return {'level': 'Deep Flow', 'icon': '🌊', 'next': 1000, 'prev': 500}
        else:
            return {'level': 'Endless Flow', 'icon': '🌌', 'next': 1000, 'prev': 1000}

    def __str__(self):
        return f"{self.user.username} - {self.points} Points"



