from django import forms
from .models import PromptSubmission

class PromptSubmissionForm(forms.ModelForm):
    class Meta:
        model = PromptSubmission
        fields = ["name", "prompt"]   # score is not user-input

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "input-text",
                "placeholder": "e.g. Alex from HR",
            }),
            "prompt": forms.Textarea(attrs={
                "class": "input-textarea",
                "placeholder": (
                    "Write a prompt that tells the AI to draft the required content.\n"
                    "Include context, goals, audience, tone, and constraints."
                ),
                "rows": 10,
            }),
        }