from django.db import models

class auth_table(models.Model):
    username=models.CharField(max_length=90)
    password=models.CharField(max_length=250)
    role=models.CharField(max_length=80)


class department_table(models.Model):
    department=models.CharField(max_length=90)


class teacher_table(models.Model):
    LOGIN=models.ForeignKey(auth_table, on_delete=models.CASCADE)
    DEPT=models.ForeignKey(department_table, on_delete=models.CASCADE)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=90)
    age=models.IntegerField()
    phone=models.BigIntegerField()
    address=models.CharField(max_length=90)

class student_table(models.Model):
    LOGIN=models.ForeignKey(auth_table, on_delete=models.CASCADE)
    DEPT=models.ForeignKey(department_table, on_delete=models.CASCADE)
    name=models.CharField(max_length=90)
    age=models.IntegerField()
    email=models.CharField(max_length=90)
    phone=models.BigIntegerField()
    address=models.CharField(max_length=90)
    std_class=models.CharField(max_length=90)



