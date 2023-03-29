from django.db import models

# Create your models here.
class user(models.Model):
    user_id = models.BigIntegerField(primary_key=True,default=None)

    user_name = models.CharField(max_length=20,default="")
    password = models.CharField(max_length = 20,default="")
    permission= models.BigIntegerField(default=2)

class department(models.Model):
    department_id = models.BigIntegerField(primary_key=True,default=1)
    department_name=models.CharField(max_length=20,default="")
    manager  =models.CharField(max_length=20,default="")
    introduction = models.CharField(max_length=20,default="")
class case(models.Model):
    case_id = models.IntegerField(primary_key=True,default=1)
    case_name =models.CharField(max_length=20,default="")
    disease = models.ForeignKey(to='disease',on_delete=models.CASCADE)
    patient_specie = models.CharField(max_length=20,default="")
    patient_age = models.IntegerField(default=1)
    patient_weight = models.DecimalField(max_digits=5,decimal_places=2)
    admission = models.CharField(max_length=20,default="")
    admission_pic = models.CharField(max_length=20,default="")
    admission_video = models.CharField(max_length=20,default="")
    checking = models.CharField(max_length=20,default="")
    checking_pic = models.CharField(max_length=20,default="")
    checking_video = models.CharField(max_length=20,default="")
    diagnostic_result = models.CharField(max_length=20,default="")
    treatment = models.CharField(max_length=20,default="")
    treatment_pic = models.CharField(max_length=20,default="")
    treatment_video = models.CharField(max_length=20,default="")

class department(models.Model):
    department_id = models.IntegerField(primary_key=True)
    department_name = models.CharField(max_length=20)
    manager = models.CharField(max_length=20)
    introduction = models.CharField(max_length=100)
class disposition(models.Model):
    disposition_id = models.CharField(max_length=8, primary_key=True)
    disposition_name = models.CharField(max_length=20)
    disposition_price = models.IntegerField(default=0)
    introduction = models.TextField()

class disease(models.Model):
    disease_id = models.IntegerField(primary_key=True)
    disease_name = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    introduction = models.CharField(max_length=20)
class question(models.Model):
    question_id = models.IntegerField(primary_key=True)
    question_type = models.ForeignKey(to='question_type',on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    disease_id = models.ForeignKey(to='disease',on_delete=models.CASCADE)
    difficulty = models.IntegerField()
class question_type(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type_name = models.CharField(max_length=20)
    score = models.IntegerField()
class test_paper(models.Model):
    paper_id = models.IntegerField(primary_key=True)
    paper_name = models.CharField(max_length=20)
    question_id = models.ForeignKey(to=question,on_delete=models.CASCADE)
    creator_id = models.ForeignKey(to='user',on_delete=models.CASCADE)
    creation_time = models.DateTimeField()

class result(models.Model):
    result_id = models.IntegerField(primary_key=20)
    user_id = models.IntegerField()
    question_id = models.ForeignKey(to='question',on_delete=models.CASCADE)
    result_answer = models.CharField(max_length=20)
    score = models.IntegerField()

class exam_result(models.Model):
    result_id = models.ForeignKey(to='result',on_delete=models.CASCADE)
    exam_id = models.IntegerField()

class exam(models.Model):
    exam_id = models.IntegerField()
    exam_name = models.CharField(max_length=20)
    paper_id = models.ForeignKey(to='test_paper',on_delete=models.CASCADE)
    creator_id = models.ForeignKey(to='user',on_delete=models.CASCADE)
    creation_time = models.DateTimeField()
    starting_time = models.DateTimeField()
    duration = models.IntegerField()
    excellent_score = models.IntegerField()
    passing_score = models.IntegerField()
    candidate = models.CharField(max_length=20)







