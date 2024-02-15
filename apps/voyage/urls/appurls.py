"""
Urls
"""

from django.urls import path
from ..views.appviews import (
    VoyageDefaultView,
    FacultyDetailView,
    FacultiesView,
    NumberStudentsView,
    FacultyAssignments,
    CreateNewAssignment,
    AssignmentView,
    StudentsView,
    StudentDetailView,
    StudentsAssignments,
    SubmissionsView,
    CreateNewCourse
)

urlpatterns = [
    path("", VoyageDefaultView.as_view(), name="home"),
    path("faculties/", FacultiesView.as_view(), name="faculties"),
    path("faculty_detail/<int:pk>", FacultyDetailView.as_view(), name="faculty_detail"),
    path("num_students/<int:pk>", NumberStudentsView.as_view(), name="num_students"),
    path(
        "num_assignments/<int:pk>", FacultyAssignments.as_view(), name="num_assignments"
    ),
    path("students/", StudentsView.as_view(), name="students"),
    path("student_detail/<int:pk>", StudentDetailView.as_view(), name="student_detail"),
    path(
        "student_assignments/<int:student_id>/<int:course_id>",
        StudentsAssignments.as_view(),
        name="student_assignments",
    ),
    path("all_assignments/", AssignmentView.as_view(), name="all_assignments"),
    path("submissions/", SubmissionsView.as_view(), name="submissions"),
    path("course/new/", CreateNewCourse.as_view(), name="new_course"),
    path("assignment/new/", CreateNewAssignment.as_view(), name="new_assignment"),
]
