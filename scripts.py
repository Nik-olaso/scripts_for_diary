from datacenter.models import (
    Chastisement,
    Commendation,
    Lesson,
    Mark,
    Schoolkid,
    Subject,
    Teacher,
)
import random


COMPLIMENT_EXAMPLES = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
]


def get_student(student):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=student)
    except Schoolkid.MultipleObjectsReturned:
        print("Найдено слишком много учеников, уточните фамилию!")
    except Schoolkid.DoesNotExist:
        print("Не найдено ученика с таким именем, проверьте имя")
    return schoolkid


def remove_chastisements(student):
    schoolkid = get_student(student)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def fix_marks(student):
    schoolkid = get_student(student)
    student_bad_marks = Mark.objects.filter(
        schoolkid=schoolkid, points__in=[2, 3]
    ).update(points="5")


def create_commendation(student, subject_name):
    schoolkid = get_student(student)
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_name,
    )
    teacher = Teacher.objects.filter(lesson=lessons[0])
    date = (
        Lesson.objects.filter(
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
            subject__title=subject_name,
            teacher=teacher[0],
        )
        .order_by("?")
        .first()
    )
    subject = Subject.objects.filter(
        title=subject_name, year_of_study=schoolkid.year_of_study
    )
    compliment = random.choice(COMPLIMENT_EXAMPLES)
    сommendation = Commendation.objects.create(
        text=compliment,
        created=date.date,
        schoolkid=schoolkid,
        subject=subject[0],
        teacher=teacher[0],
    )
