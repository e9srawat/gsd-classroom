from django.urls import path

from ..views.appviews import *

urlpatterns = [
    path("", VoyageDefaultView.as_view(), name="home"),
    path("faculties/", FacultiesView.as_view(), name="faculties"),
    path("faculty_detail/<int:pk>", FacultyDetailView.as_view(), name="faculty_detail"),
    path("students/", StudentsView.as_view(), name="students"),
    path("student_detail/<int:pk>", StudentDetailView.as_view(), name="student_detail"),
    path("all_assignments/<int:pk>", AssignmentView.as_view(), name="student_assignments"),
    path("course/new/", CreateNewCourse.as_view(), name="new_course"),
    path("assignment/new/", CreateNewAssignment.as_view(), name="new_assignment"),

]
