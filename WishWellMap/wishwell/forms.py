from django import forms
from django.utils import timezone
from .models import Shelf, BucketItem, Memory
class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ['name', 'icon', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g. Travel, Career'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Paste or type an emoji (e.g. 📁, ✈️, 🎯)',
                'maxlength': '8',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Describe what goes on this shelf...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an existing shelf or creating new, ensure default fallback emoji
        if not self.initial.get('icon') and not getattr(self.instance, 'icon', None):
            self.fields['icon'].initial = '📁'

class BucketItemForm(forms.ModelForm):
    target_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control',
            'min': timezone.now().date().isoformat()  # Prevents selecting past dates in browser picker
        }),
        required=False
    )

    class Meta:
        model = BucketItem
        # Note: 'image' matches item.image in models and item.image.url in templates
        fields = ['title', 'shelf', 'image', 'description', 'why_statement', 'location', 'target_date', 'priority', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'shelf': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'why_statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_target_date(self):
        target_date = self.cleaned_data.get('target_date')
        if target_date and target_date < timezone.now().date():
            raise forms.ValidationError("Target date must be today or a future date!")
        return target_date

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['shelf'].queryset = Shelf.objects.filter(user=user)
            
class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['story', 'completion_date', 'mood', 'rating']
        widgets = {
            'story': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mood': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }


