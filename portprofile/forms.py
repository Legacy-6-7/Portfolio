from django import forms
from .models import Portfolio, Skill, Project, Experience

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = '__all__'
        widgets = {
            'hero_tagline': forms.Textarea(attrs={'rows': 3}),
            'about_text_1': forms.Textarea(attrs={'rows': 3}),
            'about_text_2': forms.Textarea(attrs={'rows': 3}),
            'about_text_3': forms.Textarea(attrs={'rows': 3}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level', 'order']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'tags', 'live_url', 'source_url', 'glyph', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['date_range', 'role', 'organization', 'description', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }