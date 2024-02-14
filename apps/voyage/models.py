"""
models.py
"""

import random
import datetime
from django.contrib.auth import get_user_model
from django.db import models
from qux.models import QuxModel


class Faculty(QuxModel):
    """
    Faculty model
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username

    def programs(self):
        """
        returns list of programs which has the current faculty
        """
        return set(Program.objects.filter(assignment__content__faculty=self))

    def courses(self):
        """
        returns list of courses which has the current faculty
        """
        return set(Course.objects.filter(assignment__content__faculty=self))

    def content(self, program=None, course=None):
        """
        returns list of content associated with the current faculty
        """
        content_list = Content.objects.filter(faculty=self)
        if program and course:
            return [
                i
                for i in content_list
                if i.assignment_set.filter(program=program, course=course)
            ]
        if program:
            return [i for i in content_list if i.assignment_set.filter(program=program)]
        if course:
            return [i for i in content_list if i.assignment_set.filter(course=course)]
        return content_list

    def assignments_graded(self, assignment=None):
        """
        returns list of studentassignments that have been graded
        """
        if assignment:
            return self.studentassignment_set.filter(assignment=assignment).exclude(
                grade__isnull=True
            )
        return self.studentassignment_set.exclude(grade__isnull=True)

    def random_data(self):
        """
        Generates Random Data
        """
        user_model = get_user_model()
        lst = []
        names = ["Bruce", "Diana", "Barry", "Hal", "Clark", "Arthur"]
        for i in range(5):
            username = random.choice(names)
            names.remove(username)
            password = "password" + str(i)
            email = username + "@email.com"
            user = user_model.objects.create(
                username=username, password=password, email=email
            )
            github = "github/" + username
            lst.append(Faculty(user=user, github=github))
        Faculty.objects.bulk_create(lst)


class Program(QuxModel):
    """
    Example: Cohort-2
    """

    name = models.CharField(max_length=128)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name

    def students(self):
        """
        List of students in the program
        """
        return Student.objects.filter(program=self)

    def random_data(self):
        """
        Generates Random Data
        """
        years = list(range(2020, 2024))
        days = list(range(1, 28))
        months = list(range(1, 13))
        lst = []
        for i in range(3):
            year = random.choice(years)
            day = random.choice(days)
            month = random.choice(months)
            name = "Cohort-" + str(i)
            start = datetime.date(year=year, day=day, month=month)
            end = datetime.date(year=year + 5, day=day, month=month)
            lst.append(Program(name=name, start=start, end=end))
        Program.objects.bulk_create(lst)


class Course(QuxModel):
    """
    Example: Python, or Django, or Logic
    """

    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def programs(self):
        """
        list of all programs with current course
        """
        return set(Program.objects.filter(assignment__course=self))

    def students(self):
        """
        list of all sudents doing the current course
        """
        return set(Student.objects.filter(program__assignment__course=self))

    def content(self):
        """
        list of all content in the current course
        """
        return set(Content.objects.filter(assignment__course=self))

    def assignments(self):
        """
        list of all assignments in the current course
        """
        return Assignment.objects.filter(course=self)

    def random_data(self):
        """
        Generates Random Data
        """
        courses_list = ["Python", "Django", "Html/Css"]
        lst = []
        for _ in range(3):
            name = random.choice(courses_list)
            courses_list.remove(name)
            lst.append(Course(name=name))
        Course.objects.bulk_create(lst)


class Content(QuxModel):
    """
    Meta information related to a GitHub repo
    """

    name = models.CharField(max_length=128)
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    repo = models.URLField(max_length=240, unique=True)

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Content"

    def __str__(self):
        return self.name
    
    def random_data(self):
        """
        Generates Random Data
        """
        faculties = Faculty.objects.all()
        lst = []
        for i in range(28):
            name = "content" + str(i)
            faculty = random.choice(faculties)
            repo = f"https://github.com/{faculty.user.username}/{name}"
            lst.append(Content(name=name, faculty=faculty, repo=repo))
        Content.objects.bulk_create(lst)


class Student(QuxModel):
    """
    Student model
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    github = models.CharField(max_length=39, unique=True)
    is_active = models.BooleanField(default=True)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.user.username
    
    def courses(self):
        """
        List of courses the student is doing
        """
        return set(Course.objects.filter(assignment__program__student=self))

    def assignments(self):
        """
        List of assignments for the student
        """
        return Assignment.objects.filter(program__student=self)

    def assignments_submitted(self, assignment=None):
        """
        List of assignments submitted by the student
        """
        if assignment:
            return self.studentassignment_set.filter(
                assignment=assignment, submitted__isnull=False
            )
        return self.studentassignment_set.filter(submitted__isnull=False)

    def assignments_not_submited(self, assignment=None):
        """
        List of assignments not submitted by the student
        """
        if assignment:
            return self.studentassignment_set.filter(
                assignment=assignment, submitted__isnull=True
            )
        return self.studentassignment_set.filter(submitted__isnull=True)

    def assignments_graded(self, assignment=None):
        """
        List of assignments submitted by the student that have been graded
        """
        if assignment:
            return self.studentassignment_set.filter(
                assignment=assignment, grade__isnull=False
            )
        return self.studentassignment_set.filter(grade__isnull=False)

    def random_data(self):
        """
        Generates Random Data
        """
        user_model = get_user_model()
        programs = Program.objects.all()
        student_names = [
            "Tim",
            "Jason",
            "Damien",
            "Grayson",
            "Wally",
            "Roy",
            "Donna",
            "Barbara",
            "Bart",
            "jonathan",
        ]
        lst = []
        for i in range(10):
            username = random.choice(student_names)
            student_names.remove(username)
            password = "password" + str(i)
            email = username + "@dceu.com"
            user = user_model.objects.create(
                username=username, password=password, email=email
            )
            github = "github/" + username
            program = random.choice(programs)
            lst.append(Student(user=user, github=github, program=program))
        Student.objects.bulk_create(lst)


class Assignment(QuxModel):
    """
    Assignment model
    """

    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    due = models.DateTimeField()
    instructions = models.TextField()
    rubric = models.TextField()

    class Meta:
        unique_together = ["program", "course", "content"]

    def __str__(self):
        return self.content.name

    def students(self):
        """
        List of students with current assignment
        """
        return Student.objects.filter(program__assignment=self)

    def submissions(self, graded=None):
        """
        Return a queryset of submissions that are either all, graded, or not graded.
        """
        if graded:
            return self.studentassignment_set.filter(grade__isnull=False)
        return self.studentassignment_set.filter(grade__isnull=True)

    def random_data(self):
        """
        Generates Random Data
        """
        programs = list(Program.objects.all())
        courses = list(Course.objects.all())
        contents = Content.objects.all()
        unq = []
        lst = []
        counter = 0
        while len(lst) != 5:
            program = random.choice(programs)
            course = courses[programs.index(program)]
            content = random.choice(contents)
            uniq = (program, course, content)
            if uniq in unq:
                continue
            unq.append(uniq)
            due = datetime.date(
                year=program.start.year,
                month=program.start.month,
                day=program.start.day + 1,
            )
            instructions = "Instructions for Assignment " + str(counter)
            rubric = "Assignment" + str(counter)
            lst.append(
                Assignment(
                    program=program,
                    course=course,
                    content=content,
                    due=due,
                    instructions=instructions,
                    rubric=rubric,
                )
            )
            counter += 1
        Assignment.objects.bulk_create(lst)


class StudentAssignment(QuxModel):
    """
    StudentAssignment model
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=None,
        null=True,
        blank=True,
    )
    submitted = models.DateTimeField(default=None, null=True, blank=True)
    reviewed = models.DateTimeField(default=None, null=True, blank=True)
    reviewer = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, default=None, null=True, blank=True
    )
    feedback = models.TextField(default=None, null=True, blank=True)

    def random_data(self):
        """
        Generates Random Data
        """
        students = Student.objects.all()
        assignments = list(Assignment.objects.all())
        faculty = list(Faculty.objects.all())
        lst = []
        for i in students:
            student = i
            assignment = random.choice(assignments)
            reviewer = faculty[assignments.index(assignment)]
            submitted = None
            reviewed = None
            grade = None
            if random.choice((True, False)):
                submitted = assignment.due
                if random.choice((True, False)):
                    reviewed = datetime.date(
                        year=submitted.year,
                        month=submitted.month,
                        day=submitted.day + 1,
                    )
                    grade = random.choice(range(1000))
            lst.append(
                StudentAssignment(
                    student=student,
                    assignment=assignment,
                    grade=grade,
                    submitted=submitted,
                    reviewed=reviewed,
                    reviewer=reviewer,
                )
            )
        StudentAssignment.objects.bulk_create(lst)


def create_random_data():
    """
    Generates Random Data
    """
    faculty = Faculty()
    program = Program()
    course = Course()
    content = Content()
    student = Student()
    assignment = Assignment()
    student_assignment = StudentAssignment()
    faculty.random_data()
    program.random_data()
    course.random_data()
    content.random_data()
    student.random_data()
    assignment.random_data()
    student_assignment.random_data()
    student_assignment.random_data()
