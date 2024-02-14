"""
admin.py
"""

from django.utils.html import format_html
from django.contrib import admin

from .models import (
    Faculty,
    Content,
    Program,
    Course,
    Student,
    Assignment,
    StudentAssignment,
)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """
    FacultyAdmin
    """

    list_display = ("user", "num_courses", "num_assignments", "graded_assignments")

    def num_courses(self, obj):
        """
        Returns number of courses.
        """
        courses = obj.courses()
        ids = [i.id for i in courses]
        if courses:
            html = '<a href="/admin/voyage/course/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1] + f'">{len(courses)}</a>'
            return format_html(html)
        return 0

    def num_assignments(self, obj):
        """
        Returns number of assignments
        """
        content = obj.content()
        assignments = set(j for i in content for j in i.assignment_set.all())
        ids = [i.id for i in assignments]
        if assignments:
            html = '<a href="/admin/voyage/assignment/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1] + f'">{len(assignments)}</a>'
            return format_html(html)
        return 0

    def graded_assignments(self, obj):
        """
        Returns number of assignments that have been graded
        """
        assignments = obj.assignments_graded()
        ids = [i.id for i in assignments]
        if assignments:
            html = '<a href="/admin/voyage/studentassignment/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1] + f'">{len(assignments)}</a>'
            return format_html(html)
        return 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    StudentAdmin
    """

    list_display = (
        "user",
        "program",
        "num_courses",
        "assignments_assigned",
        "assignments_submitted",
        "avg_grade",
    )

    list_display_links = ("user", "program")

    def num_courses(self, obj):
        """
        number of courses each student is enrolled in
        """
        courses = obj.courses()
        ids = [i.id for i in courses]
        if courses:
            html = '<a href="/admin/voyage/course/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1] + f'">{len(courses)}</a>'
            return format_html(html)
        return 0

    def assignments_assigned(self, obj):
        """
        number of assignments assigned to the student
        """
        assignments = obj.assignments()
        ids = [i.id for i in assignments]
        if assignments:
            html = '<a href="/admin/voyage/assignment/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1] + f'">{len(assignments)}</a>'
            return format_html(html)
        return 0

    def assignments_submitted(self, obj):
        """
        number of assignments each student has submitted
        """
        assignments = obj.assignments_submitted()
        ids = [i.id for i in assignments]
        if assignments:
            html = '<a href="/admin/voyage/studentassignment/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1] + f'">{len(assignments)}</a>'
            return format_html(html)
        return 0

    def avg_grade(self, obj):
        """
        average grade of each student
        """
        graded_submissions = obj.assignments_graded()
        if graded_submissions:
            grades = [int(i.grade) for i in graded_submissions]

            return sum(grades) / len(grades)
        return 0


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    ContentAdmin
    """

    list_display = ("name", "num_courses", "num_assignments")

    def num_courses(self, obj):
        """
        number of courses that use each content
        """
        assignments = obj.assignment_set.all()
        courses = set(i.course for i in assignments)
        ids = [i.id for i in courses]
        if courses:
            html = '<a href="/admin/voyage/course/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1] + f'">{len(courses)}</a>'
            return format_html(html)
        return 0

    def num_assignments(self, obj):
        """
        number of assignments that use each content
        """
        assignments = obj.assignment_set.all()
        ids = [i.id for i in assignments]
        if assignments:
            html = '<a href="/admin/voyage/assignment/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1] + f'">{len(assignments)}</a>'
            return format_html(html)
        return 0


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """
    ProgramAdmin
    """

    list_display = ("name", "num_courses", "num_students")

    def num_courses(self, obj):
        """
        number of courses in each program
        """
        assignments = obj.assignment_set.all()
        courses = set(i.course for i in assignments)
        ids = [i.id for i in courses]
        if courses:
            html = '<a href="/admin/voyage/course/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1]
            html += f'">{len(courses)}</a>'
            return format_html(html)
        return 0

    def num_students(self, obj):
        """
        number of students in each program
        """
        students = obj.students()
        ids = [i.id for i in students]
        if students:
            html = '<a href="/admin/voyage/student/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1] + f'">{len(students)}</a>'
            return format_html(html)
        return 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    CourseAdmin
    """

    list_display = ("name", "num_assignments", "graded_100")

    def num_assignments(self, obj):
        """
        number of assignments in each course
        """
        assignments = obj.assignments()
        ids = [i.id for i in assignments]
        if assignments:
            html = '<a href="/admin/voyage/assignment/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1] + f'">{len(assignments)}</a>'
            return format_html(html)
        return 0

    def graded_100(self, obj):
        """
        number of assignments that are completed and graded 100%
        """
        assignments = obj.assignments()
        max_value = 999
        graded = set()
        for i in assignments:
            for j in i.studentassignment_set.filter(grade__isnull=False):
                if int(j.grade) == max_value:
                    graded.add(j)
        ids = [i.id for i in graded]
        if graded:
            html = '<a href="/admin/voyage/studentassignment/?id__in='
            for i in ids:
                html += f"{i},"
            html = html[:-1] + f'">{len(graded)}</a>'
            return format_html(html)
        return 0


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    AssignmentAdmin
    """

    list_display = ("rubric", "avg_grade")

    def avg_grade(self, obj):
        """
        average grade of each assignment
        """
        submissions = obj.submissions(graded=True)
        if submissions:
            grades = [int(i.grade) for i in submissions]
            return sum(grades) / len(grades)
        return 0


@admin.register(StudentAssignment)
class StudentAssignmentAdmin(admin.ModelAdmin):
    """
    StudentAssignmentAdmin
    """
