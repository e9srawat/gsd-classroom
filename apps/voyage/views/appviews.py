"""
views
"""

from typing import Any
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import redirect, render
from qux.seo.mixin import SEOMixin
from ..models import Faculty, Student, StudentAssignment, Course, Assignment
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


class NumberStudentsView(ListView):
    """
    NumberStudents View
    """

    model = Course
    template_name = "voyage/common_list.html"

    def get_context_data(self, **kwargs):
        """
        returns context data
        """
        course = Course.objects.get(id=self.kwargs["pk"])
        context = super().get_context_data(**kwargs)
        context["context"] = course.students()
        print(context)
        return context


class FacultyAssignments(ListView):
    """
    FacultyAssignments view
    """

    model = Course
    template_name = "voyage/common_list.html"
    context_object_name = "context"

    def get_queryset(self, *args, **kwargs):
        """
        gets queryset
        """
        course = Course.objects.get(id=self.kwargs["pk"])
        queryset = course.assignments()
        return queryset


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
        print(context)
        return context


class StudentsAssignments(ListView):
    """
    StudentsAssignments view
    """

    model = Course
    template_name = "voyage/common_list.html"
    context_object_name = "context"

    def get_queryset(self, *args, **kwargs):
        """
        gets queryset
        """
        course = Course.objects.get(id=self.kwargs["course_id"])
        student = Student.objects.get(id=self.kwargs["student_id"])
        assignments = student.assignments().filter(course=course)
        return assignments


class AssignmentView(SEOMixin, ListView):
    """
    Assignment detail
    """

    model = Assignment
    template_name = "voyage/assignment_list.html"

    def get_context_data(self, **kwargs):
        """
        gets context
        """
        context = super().get_context_data(**kwargs)
        assignments = Assignment.objects.all()
        dicn = {}
        for i in assignments:
            submissions = i.submissions(graded=True)
            if submissions:
                grades = [int(i.grade) for i in submissions]
                avg = sum(grades) / len(grades)
                dicn[i] = [avg]
            else:
                dicn[i] = [0]
            dicn[i].append(
                StudentAssignment.objects.filter(assignment=i, submitted__isnull=False)
            )
        context["assignments"] = dicn
        print(context)
        return context


class SubmissionsView(ListView):
    """
    Submissions view
    """

    model = StudentAssignment
    template_name = "voyage/submissions.html"
    context_object_name = "studentassignments"
    queryset = StudentAssignment.objects.filter(submitted__isnull=False)


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
            return redirect("home")
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
            return redirect("home")
        return render(request, self.template_name, {"form": form})
