from django.db import models


from django.contrib.auth.models import User

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)


class User(models.Model):
     username = models.EmailField(max_length=50)
     password= models.TextField (max_length=100)



class GeeksModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
 
    def __str__(self):
        return self.title


class Student(models.Model):
	name = models.CharField(max_length=100)
	age = models.IntegerField(default=18)
	fathers_name = models.CharField(max_length=100)
     
class Category(models.Model):
     category_name = models.CharField(max_length=99)


class Book(models.Model):
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     book_title = models.CharField(max_length= 99)