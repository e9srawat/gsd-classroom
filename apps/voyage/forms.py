"""
forms
"""

from django import forms
from .models import Course, Assignment


class CreateCourseForm(forms.ModelForm):
    """
    form to add new course
    """

    class Meta:
        model = Course
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class CreateAssignmentForm(forms.ModelForm):
    """
    Form to create a new assignment
    """

    class Meta:
        model = Assignment
        fields = ["program", "course", "content", "due", "instructions", "rubric"]
        widgets = {
            "program": forms.Select(attrs={"class": "form-control"}),
            "course": forms.Select(attrs={"class": "form-control"}),
            "content": forms.Select(attrs={"class": "form-control"}),
            "due": forms.TextInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "instructions": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "rubric": forms.Textarea(attrs={"rows": 1, "class": "form-control"}),
        }
