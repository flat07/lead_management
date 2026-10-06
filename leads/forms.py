# leads/forms.py

from django import forms

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead

        fields = (
            "name",
            "phone",
            "email",
            "source",
            "status",
            "note",
        )

        widgets = {  # noqa: RUF012
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "John Smith",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "+998 90 123 45 67",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "john@example.com",
                }
            ),
            "source": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                }
            ),
            "note": forms.Textarea(
                attrs={
                    "class": ("textarea textarea-bordered w-full h-32"),
                    "placeholder": "Lead notes...",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")

        if not phone and not email:
            raise forms.ValidationError("Either phone or email is required.")

        return cleaned_data
