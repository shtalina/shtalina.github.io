from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import tensorflow.keras as keras
from tensorflow.keras.models import load_model, Sequential
from .models import Student, Faculty, Group, Comp, Studen, Mark, File
import numpy as np
from io import BytesIO
from django.core.paginator import Paginator
from itertools import groupby
import plotly.graph_objects as go
import requests
from django.shortcuts import render
import pandas as pd

# Create your views here.

def faculty(request):
    faculties = Faculty.objects.all()
    grouped_groups = []
    for faculty in faculties:
        groups = Group.objects.filter(faculty=faculty).order_by('kurs1')
        grouped_data = []
        for key, group in groupby(groups, key=lambda x: x.kurs1):
            grouped_data.append((key, list(group)))
        grouped_groups.append((faculty, grouped_data))

    return render(request, 'cogn/groups.html', {'faculties': faculties, 'grouped_groups': grouped_groups})

def stud(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    students = Studen.objects.filter(gruppa1=group)
    return render(request, 'cogn/stud.html', {'group': group, 'students': students})

def profile(request, student_id):
    data = Student.objects.get(student_id=student_id)
    student = Studen.objects.get(student_id=student_id)
    group = student.gruppa1

    if group:
        faculty = group.faculty
    else:
        faculty = None

    def marks():
        mark = Mark.objects.filter(student_id=student_id).order_by('number_of_semester')

        # Формируем словарь, где ключи - названия курсов, значения - список оценок для каждого курса
        marks_by_course = {}
        for marks in mark:
            if marks.course not in marks_by_course:
                marks_by_course[marks.course] = []
            marks_by_course[marks.course].append(marks)

        # Получите все записи экзаменов для данного студента

        # Создайте списки для хранения данных о семестрах и средних баллах
        semesters = []
        average_scores = []

        # Итерируйтесь по записям экзаменов и вычисляйте средний балл для каждой сессии
        current_semester = 0
        current_scores = []
        for record in mark:
            if record.is_examen == 1:
                if record.number_of_semester != current_semester:
                    if current_scores:

                        numeric_scores = [int(score) for score in current_scores if
                                          str(score).isdigit()]  # Convert to string before checking
                        if numeric_scores:
                            average_score = sum(numeric_scores) / len(numeric_scores)
                            semesters.append(current_semester)
                            average_scores.append(average_score)

                    # Reset current data for a new session
                    current_semester = record.number_of_semester
                    current_scores = [int(record.value)]  # Convert to integer during initialization
                else:
                    current_scores.append(int(record.value))  # Convert to integer when adding current score

        # Добавьте последнюю сессию, если есть данные
        if current_scores:
            average_score = sum(current_scores) / len(current_scores)
            semesters.append(current_semester)
            average_scores.append(average_score)

        # Создайте график для траектории изменения среднего балла
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=semesters, y=average_scores, mode='lines+markers'))
        fig.update_layout(xaxis_title='Семестр', yaxis_title='Средний балл')

        # Преобразуйте график в HTML и передайте его в шаблон
        graph_htm = fig.to_html(full_html=False)
        return(mark, graph_htm, marks_by_course)

    marke = marks()
    mark, graph_htm, marks_by_course = marke

    def normalize_data(values):

        normalized_values = np.log(values)

        return normalized_values.flatten()

    def pentagon():
        cognitive_data = {
            "Мышление": data.rawen,
            "Восприятие": data.vospr_prost,
            "Внимание": data.vnim_ob,
            "Слуховая Память": data.sluh_pam,
            "Креативное мышление": data.prim_predm,
            "Вербально-коммуникативные способности": data.predl,
            "Устойчивость внимания": data.vnim_ust,
            "Образная память": data.obr_pam,
        }

        values = np.array(list(cognitive_data.values()))

        # Нормализация данных
        normalized_values = normalize_data(values)

        categories = list(cognitive_data.keys())

          #Создаем фигуру для пентагонального графика
        fig = go.Figure()

        # Добавляем границы пентагона
        fig.add_trace(go.Scatterpolar(
            r=np.append(normalized_values, normalized_values[0]),
            theta=['Мышление', 'Восприятие', 'Внимание', 'Слуховая Память', 'Креативное мышление', 'Вербально-коммуникативные способности', 'Устойчивость внимания', 'Образная память'],
            fill='toself',
            name='Cognitive Metrics',
            line=dict(color='rgb(118, 138, 204)')
        ))

        # Добавляем значения на точки

        for i, (category, value) in enumerate(zip(categories, normalized_values)):
            fig.add_trace(go.Scatterpolar(
                r=[value, value, value, value, value, value, value, value],  # Позиционируем значение на соответствующей категории
                theta=[category, category, category, category, category, category, category, category],  # 6 точек вокруг категории
                mode='markers+text',  # Включаем маркеры и текст
                text=[f'{value:.2f}'],  # Устанавливаем текст метки
                textposition='top right' if i % 2 == 0 else 'top left',  # Располагаем текст в нижней части точки
                # Устанавливаем размер маркера
                name=category,  # Устанавливаем имя категории
                marker=dict(color='rgb(64, 83, 145)')
            ))

            # Обновляем макет
        fig.update_layout(
            width=800,  # Устанавливаем ширину графика
            height=600,
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5],  # Диапазон для нормализованных значений будет от 0 до 1
                    showline=False,  # Устанавливаем showline в False
                    showticklabels=False
                ),
            ),
            showlegend=False,
            # title='Когнитивная модель студента:',

            font=dict(size=12)
        )

    # Преобразуем фигуру в HTML
        graph_html = fig.to_html()
        return graph_html


    graph_html = pentagon()
    graph_html = graph_html


    def compt(request):
        all_competencies = Comp.objects.all()

        # Фильтруем компетенции по категориям
        opk_competencies = all_competencies.filter(order__startswith='2')
        uk_competencies = all_competencies.filter(order__startswith='1')
        pk_competencies = all_competencies.filter(order__startswith='3')

        # Разбиваем компетенции на страницы для каждой категории
        opk_paginator = Paginator(opk_competencies, 4)
        uk_paginator = Paginator(uk_competencies, 5)
        pk_paginator = Paginator(pk_competencies, 5)

        # Получаем номера страниц из GET-параметров
        opk_page_number = request.GET.get('opk_page')
        uk_page_number = request.GET.get('uk_page')
        pk_page_number = request.GET.get('pk_page')

        # Получаем объекты страниц для каждой категории
        opk_page_obj = opk_paginator.get_page(opk_page_number)
        uk_page_obj = uk_paginator.get_page(uk_page_number)
        pk_page_obj = pk_paginator.get_page(pk_page_number)
        return (opk_page_obj, uk_page_obj, pk_page_obj)

    opk_page_obj, uk_page_obj, pk_page_obj = compt(request)
    opk_page_obj = opk_page_obj
    uk_page_obj = uk_page_obj
    pk_page_obj = pk_page_obj

    model = keras.models.load_model("./cogn/models/rec.h5")
    def get_recommendations_from_model():
        # входные данные
        params = {
            "vnim_ob": data.vnim_ob,
            "vnim_ust": data.vnim_ust,
            "obr_pam": data.obr_pam,
            "prim_predm": data.prim_predm,
            "vospr_prost": data.vospr_prost,
            "rawen": data.rawen,
            "sluh_pam": data.sluh_pam,
            "predl": data.predl,
        }
        values = np.array(list(params.values()))

        # Изменяем форму входных данных
        values_reshaped = values.reshape(1, -1)  # изменяем форму на (1, 8)

         # Предсказание с использованием модели
        predictions = model.predict(values_reshaped)

        # Получение топ-3 рекомендаций
        top_recommendations_indices = np.argsort(predictions[0])[-3:][::-1]
        df = pd.read_excel('./cogn/static/aaa.xlsx')

        # Преобразование DataFrame в словарь
        recommendation_labels = df.set_index('Index')['W'].to_dict()

        # Получение текстовых меток для рекомендаций
        top_recommendations = [recommendation_labels[idx] for idx in top_recommendations_indices]

        # Получение текстовых меток для рекомендаций
        # Здесь нужно добавить ваш механизм для получения меток рекомендаций, так как вы используете свою модель


        return top_recommendations

    top_recommendations = get_recommendations_from_model()
    top_recommendations = top_recommendations

    for i, recommendation in enumerate(top_recommendations, start=1):
        print(f"Рекомендация {i}: {recommendation}")



    return render(request, 'cogn/profile.html', {
        'graph_html': graph_html,
        'data': data,
        'student': student,
        'mark': mark,
        'graph_htm': graph_htm,
        'compt': compt,
        'group': group,
        'faculty': faculty,
        'opk_page_obj': opk_page_obj,
        'uk_page_obj': uk_page_obj,
        'pk_page_obj': pk_page_obj,
        'marks_by_course': marks_by_course,
        'top_recommendations': top_recommendations,

    })

def contacts(request):
    return render(request, 'cogn/contacts.html')

