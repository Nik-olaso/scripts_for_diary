from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid, Subject, Teacher)
import random


def remove_chastisements(student):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=student)
    except Schoolkid.MultipleObjectsReturned:  
        print('Найдено слишком много учеников, уточните фамилию!')
    except Schoolkid.DoesNotExist:
        print('Не найдено ученика с таким именем, проверьте имя')
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def fix_marks(student):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=student)
        print(schoolkid)
    except Schoolkid.MultipleObjectsReturned:  
        print('Найдено слишком много учеников, уточните фамилию!')
    except Schoolkid.DoesNotExist:
        print('Не найдено ученика с таким именем, проверьте имя')
    student_bad_marks = Mark.objects.filter(schoolkid = schoolkid, points__in = [2,3])
    for student_bad_mark in student_bad_marks:
        student_bad_mark.points = '5'
        student_bad_mark.save()


def create_commendation(student, subject_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=student)
    except Schoolkid.MultipleObjectsReturned:  
        print('Найдено слишком много учеников, уточните фамилию!')
    except Schoolkid.DoesNotExist:
        print('Не найдено ученика с таким именем, проверьте имя')
    lessons = Lesson.objects.filter(year_of_study='6', group_letter='А', subject__title=subject_name) 
    teacher = Teacher.objects.filter(lesson=lessons[0])
    date = Lesson.objects.filter(year_of_study='6', group_letter='А', subject__title=subject_name, teacher=teacher[0])[0]
    subject = Subject.objects.filter(title=subject_name, year_of_study='6')
    compliment_examples = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!', 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!', 'Очень хороший ответ!', 'Талантливо!', 'Ты сегодня прыгнул выше головы!', 'Я поражен!']
    compliment = random.choice(compliment_examples)
    сommendation = Commendation.objects.create(text=compliment, created=date.date, schoolkid=schoolkid, subject=subject[0], teacher=teacher[0])