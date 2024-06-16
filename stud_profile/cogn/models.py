from django.db import models


class Students(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    fio = models.TextField()
    spec = models.TextField(blank=True, null=True)
    adress = models.TextField(blank=True, null=True)
    tel = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    spec_napravl = models.TextField(blank=True, null=True)
    forma = models.CharField(max_length=20, blank=True, null=True)
    sroki = models.TextField(blank=True, null=True)
    facultet = models.TextField(blank=True, null=True)
    kafedra = models.CharField(max_length=50, blank=True, null=True)
    rukov = models.CharField(max_length=50, blank=True, null=True)
    tema = models.CharField(max_length=100, blank=True, null=True)
    gruppa = models.IntegerField(blank=True, null=True)
    edecanat_id = models.IntegerField(unique=True, blank=True, null=True)
    fac_id = models.IntegerField(blank=True, null=True)
 #   course = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'students'


class Files(models.Model):
    fio = models.CharField(max_length=50, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    owner = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    id = models.IntegerField(db_column='stud_id', primary_key=True)

    class Meta:
        managed = False
        db_table = 'files'
""""
class Marks(models.Model):

    student_id = models.IntegerField(db_column='STUDENT_ID', blank=True, null=True)  # Field name made lowercase.
    student_fio = models.CharField(db_column='STUDENT_FIO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    gruppa = models.IntegerField(db_column='GRUPPA', blank=True, null=True)  # Field name made lowercase.
    discipline_name = models.TextField(db_column='DISCIPLINE_NAME', blank=True, null=True)  # Field name made lowercase.
    mark_name = models.CharField(max_length=20, blank=True, null=True)
    is_examen = models.IntegerField(db_column='IS_EXAMEN', blank=True, null=True)  # Field name made lowercase.
    number_of_semester = models.IntegerField(db_column='NUMBER_OF_SEMESTER', blank=True, null=True)  # Field name made lowercase.
    mark = models.IntegerField(blank=True, null=True)
    coddis = models.CharField(db_column='CODDIS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    id = models.IntegerField(db_column='stud_id', primary_key=True)

    class Meta:
        managed = False
        db_table = 'marks'
"""

class Comp(models.Model):
    id = models.IntegerField(primary_key=True)
    kod_plana = models.PositiveIntegerField()
    stud_plan = models.PositiveIntegerField()
    comp_name = models.PositiveIntegerField()
    shifr_name = models.PositiveIntegerField()
    order = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'comp'


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'cogn_faculty'

    def __str__(self):
        return self.name

class Group(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    cod1 = models.IntegerField()
    fakshfr1 = models.CharField(max_length=10)
    kurs1 = models.IntegerField()
    gruppa1 = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'cogn_group'

    def __str__(self):
        return f"{self.faculty} - {self.gruppa1}"

class Studen(models.Model):
    student_id = models.IntegerField(primary_key=True)
    fio = models.CharField(max_length=255, null=True)
    gruppa1 = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = False
        db_table = 'cogn_studen'

    def __str__(self):
        return f"{self.fio} - {self.gruppa1}"

class Mark(models.Model):

    student = models.ForeignKey(Studen, on_delete=models.CASCADE, null=True)
    student_fio = models.CharField(max_length=255)
    gruppa1 = models.CharField(max_length=255)  # Added field
    cod = models.IntegerField()  # Added field
    id_disc = models.IntegerField()  # Added field
    discipline_name = models.CharField(max_length=255)
    mark_name = models.CharField(max_length=255)
    is_examen = models.BooleanField()  # Added field
    number_of_semester = models.IntegerField()  # Added field
    coddis = models.CharField(max_length=255)  # Added field
    idplan = models.IntegerField()  # Added field
    value = models.CharField(max_length=255)  # Added field
    fio = models.CharField(max_length=255)
    course = models.IntegerField()  # Added field
    type_control = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'cogn_mark'

    def __str__(self):
        return f"{self.student_fio} - {self.gruppa1} - {self.discipline_name} - {self.mark_name}"

    @staticmethod
    def get_courses():
        return Mark.objects.values_list('course', flat=True).distinct()

    @staticmethod
    def get_marks_by_course(course):
        return Mark.objects.filter(course=course).order_by('number_of_semester')

class File(models.Model):
    student = models.ForeignKey(Studen, on_delete=models.CASCADE)
    student_fio = models.CharField(max_length=255)
    gruppa1 = models.CharField(max_length=255)  # Added field
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255)
    owner = models.IntegerField()  # Added field
    url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'cogn_file'

    def __str__(self):
        return f"{self.student_fio} - {self.gruppa1} - {self.name}"


class Student(models.Model):
    student_fio = models.CharField(max_length=100)
    sluh_pam = models.PositiveIntegerField(null=True)
    rawen = models.PositiveIntegerField(null=True)
    vnim_ob = models.PositiveIntegerField(null=True)
    vnim_ust = models.PositiveIntegerField(null=True)
    vospr_prost = models.PositiveIntegerField(null=True)
    obr_pam = models.PositiveIntegerField(null=True)
    prim_predm = models.PositiveIntegerField(null=True)
    predl = models.PositiveIntegerField(null=True)
    IQ = models.PositiveIntegerField(null=True)
    intro_extro = models.PositiveIntegerField(null=True)
    adapt = models.PositiveIntegerField(null=True)
    social = models.PositiveIntegerField(null=True)
    refl = models.PositiveIntegerField(null=True)
    motivation = models.PositiveIntegerField(null=True)
    student = models.ForeignKey(Studen, on_delete=models.CASCADE, null=True)
    gruppa1 = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.student_fio} - {self.gruppa1}"