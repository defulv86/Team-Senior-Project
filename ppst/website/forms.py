from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['category', 'description']
        
        widgets = {
            'category': forms.Select(attrs={'required': True}),
            'description': forms.Textarea(attrs={'required': True}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        description = cleaned_data.get("description")
        
        if not category or not description:
            raise forms.ValidationError("Both category and description are required!")
        return cleaned_data
