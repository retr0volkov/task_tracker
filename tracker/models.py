from django.db import models

# Create your models here.
class Worker(models.Model):
	title = models.CharField(max_length=200)
	
	def __str__(self):
		return self.title
    
class Task(models.Model):
	receiver = models.ForeignKey(Worker, on_delete=models.CASCADE)
	pub_date = models.DateTimeField("Дата создания")
	due_date = models.DateTimeField("Дата дедлайна")
	status = models.CharField(max_length=10) # created, received, done, deleted
	title = models.CharField(max_length=200,default='')
	desc = models.CharField(max_length=1000,default='')

	def __str__(self):
		return self.title