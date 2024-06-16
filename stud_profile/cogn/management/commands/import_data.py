import requests
from django.core.management.base import BaseCommand
from cogn.models import Studen, Mark, File, Group, Student  # Замените 'myapp' на название вашего приложения в Django

class Command(BaseCommand):
    help = 'Импорт данных из API в базу данных'

    def handle(self, *args, **kwargs):
        # Получение данных из API
        api_url = "https://portfolio.tspu.edu.ru/public/api/jobcenter?group=403&api_token=koIitJwlFt5H?ytIeNNub/UKqRbWNBMU95-VBHUjX3At?PBXpejLX2UXYs?8sw1x7DIzwKlqGDSrtx=w!8CY7Ny"
        response = requests.get(api_url)
        data = response.json()

        # Распарсивание данных и создание объектов моделей
        for student_name, student_data in data.items():
            group_info = student_data[0]['marks'][0]['GRUPPA']  # Assuming this is how the group information is accessed

            # Retrieve the Group instance based on the group_info
            group_instance = Group.objects.get(gruppa1=group_info)

            # Create a Student instance and assign it to the student_obj variable
            student_obj = Student.objects.create(
                student_id=student_data[0]['student_id'],
                student_fio=student_data[0]['fio'],
                gruppa1=group_instance,
            )
            """
            for mark_data in student_data[0]['marks']:
                mark_obj = Mark.objects.create(
                    student=student_obj,
                    student_fio=mark_data['STUDENT_FIO'],
                    gruppa1=group_instance,
                    cod=mark_data['COD'],
                    id_disc=mark_data['id_disc'],
                    discipline_name=mark_data['DISCIPLINE_NAME'],
                    mark_name=mark_data['mark_name'],
                    is_examen=mark_data['IS_EXAMEN'],
                    number_of_semester=mark_data['NUMBER_OF_SEMESTER'],
                    coddis=mark_data['CODDIS'],
                    idplan=mark_data['IDPLAN'],
                    value=mark_data['value'],
                    fio=mark_data['fio'],
                    course=mark_data['course'],
                    type_control=mark_data['type_control'],
                )

            for file_data in student_data[0]['files']:
                file_obj = File.objects.create(
                    student=student_obj,
                    name=file_data['name'],
                    description=file_data['description'],
                    category=file_data['category'],
                    owner=file_data['owner'],
                    url=file_data['url'],
                )
            """