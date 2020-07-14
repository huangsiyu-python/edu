from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher


class CourseCategorySerializer(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ["id", "name"]


class CourseTeacherSerializer(ModelSerializer):

    class Meta:
        model = Teacher
        fields = ("id", "name", "title", "signature","role","brief")


class CourseModelSerializer(ModelSerializer):
    teacher = CourseTeacherSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", "lesson_list","level"]



