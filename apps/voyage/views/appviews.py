"""
views
"""

from typing import Any
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import redirect, render
from qux.seo.mixin import SEOMixin
from ..models import Faculty, Student, StudentAssignment
from ..forms import CreateCourseForm, CreateAssignmentForm


class VoyageDefaultView(SEOMixin, TemplateView):
    """
    bage page
    """

    template_name = "voyage/base.html"


class FacultiesView(SEOMixin, ListView):
    """
    Faculty list
    """

    model = Faculty
    context_object_name = "faculty"


class FacultyDetailView(DetailView):
    """
    Faculty detail
    """

    model = Faculty
    template_name = "voyage/faculty_detail.html"


class StudentsView(SEOMixin, ListView):
    """
    Students list
    """

    model = Student
    context_object_name = "student"


class StudentDetailView(DetailView):
    """
    Students detail
    """

    model = Student
    template_name = "voyage/student_detail.html"

    def get_context_data(self, **kwargs):
        """
        gets context
        """
        context = super().get_context_data(**kwargs)
        courses = self.object.courses()
        assignments = self.object.assignments()
        dicn = {}
        for i in courses:
            dicn[i] = assignments.filter(course=i)
        context["assignments"] = dicn
        return context


class AssignmentView(SEOMixin, DetailView):
    """
    Assignment detail
    """

    model = Student
    template_name = "voyage/assignment_list.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        """
        gets context
        """
        context = super().get_context_data(**kwargs)
        assignments = self.object.assignments()
        dicn = {}
        for i in assignments:
            submissions = i.submissions(graded=True)
            if submissions:
                grades = [int(i.grade) for i in submissions]
                avg = sum(grades) / len(grades)
                dicn[i] = [avg]
            else:
                dicn[i] = [0]
            dicn[i].append(StudentAssignment.objects.filter(assignment=i))
        context["assignments"] = dicn
        print(context)
        return context


class CreateNewCourse(TemplateView):
    """
    Creates new course
    """

    template_name = "voyage/add_course.html"

    def get_context_data(self, **kwargs: Any):
        """
        gets context
        """
        context = super().get_context_data(**kwargs)
        context["form"] = CreateCourseForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        post method
        """
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("faculty_list")
        return render(request, self.template_name, {"form": form})


class CreateNewAssignment(TemplateView):
    """
    Creates new assignment
    """

    template_name = "voyage/add_course.html"

    def get_context_data(self, **kwargs):
        """
        gets context
        """
        context = super().get_context_data(**kwargs)
        context["form"] = CreateAssignmentForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        post method
        """
        form = CreateAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("faculty_list")
        return render(request, self.template_name, {"form": form})
