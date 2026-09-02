from django.db import models
from django.conf import settings

class Portfolio(models.Model):
    # Hero
    name = models.CharField(max_length=100, default="Samarth")
    role = models.CharField(max_length=200, default="Full-Stack Web Developer")
    hero_tagline = models.TextField(default="I build fast, reliable, and thoughtfully designed web applications — from database to pixel.")

    # About
    about_text_1 = models.TextField(blank=True)
    about_text_2 = models.TextField(blank=True)
    about_text_3 = models.TextField(blank=True)
    years_experience = models.CharField(max_length=20, default="3+")
    projects_shipped = models.CharField(max_length=20, default="25+")

    # Contact
    email = models.EmailField(default="samarth.dev@example.com")
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portfolio — {self.name}"


class Skill(models.Model):
    name = models.CharField(max_length=50)
    level = models.PositiveIntegerField(default=80)  
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('fullstack', 'Full-Stack'),
        ('frontend', 'Frontend'),
        ('api', 'API'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='fullstack')
    tags = models.CharField(max_length=200, help_text="Comma separated, e.g. React, Node.js")
    live_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)
    glyph = models.CharField(max_length=10, default="{ }", help_text="Symbol shown on card")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def __str__(self):
        return self.title


class Experience(models.Model):
    date_range = models.CharField(max_length=50)       
    role = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.role} @ {self.organization}"

