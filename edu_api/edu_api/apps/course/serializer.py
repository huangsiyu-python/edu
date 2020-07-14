from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


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
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", "lesson_list","level_name","brief_html"]

class CourseLessonModelSerializer(ModelSerializer):
    class Meta:
        model=CourseLesson
        fields=("id","name","free_trail")

class CourseChapterModelSerializer(ModelSerializer):
    coursesections=CourseLessonModelSerializer(many=True)
    class Meta:
        model=CourseChapter
        fields=["id","chapter","name","coursesections"]

