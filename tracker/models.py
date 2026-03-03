from django.db import models

# Create your models here.
class Worker(models.Model):
	title = models.CharField(max_length=200)
	
	def __str__(self):
		return self.title

class Stage(models.Model):
  title = models.CharField(max_length=50)
  color = models.CharField(max_length=9, default='ffffff')
  
  def __str__(self):
    return self.title

class Task(models.Model):
	receiver = models.ForeignKey(Worker, on_delete=models.CASCADE)
	pub_date = models.DateTimeField("Дата создания")
	due_date = models.DateTimeField("Дата дедлайна")
	status = models.ForeignKey(Stage, on_delete=models.DO_NOTHING)
	title = models.CharField(max_length=200,default='')
	desc = models.CharField(max_length=1000,default='')
	file = models.FileField(null=True, upload_to='media/')

	def __str__(self):
		return self.title