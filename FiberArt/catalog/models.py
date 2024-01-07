from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class TypeEmbroidery(models.Model):
    Name = models.CharField(max_length=20, help_text='Название типа вышивки')

    def __str__(self):
        return self.Name


class Embroidery(models.Model):
    User_id = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Создатель')
    Name = models.CharField(max_length=40, help_text='Название схемы')
    Type_id = models.ForeignKey(TypeEmbroidery, on_delete=models.CASCADE, help_text='Тип вышивки')
    SizeX = models.IntegerField(help_text='Количество клеток по горизонтали')
    SizeY = models.IntegerField(help_text='Количество клеток по вертикали')
    Scheme = models.TextField(help_text='Массив цветов')
    Date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.User_id} Name: {self.Name} Date: {self.Date}"


class Color(models.Model):
    Name = models.CharField(max_length=40, help_text='Название цвета')
    HEX = models.CharField(max_length=7, help_text='HEX данного цвета')

    def __str__(self):
        return self.Name
