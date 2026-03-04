from django.db import models
from django.conf import settings

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
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	pub_date = models.DateTimeField("Дата создания")
	due_date = models.DateField("Дата дедлайна")
	status = models.ForeignKey(Stage, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, default='')
	desc = models.TextField(max_length=1000, default='')
	file = models.FileField(blank=True, null=True, upload_to='media/')

	def __str__(self):
		return self.title

class Comment(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  task = models.ForeignKey(Task, on_delete=models.CASCADE)
  content = models.TextField(max_length=1000)
    
  def __str__(self):
    return str(self.author.username[:2])