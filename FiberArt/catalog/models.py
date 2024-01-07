from django.db import models
from django.urls import reverse


class MyModelName(models.Model):
    my_field_name = models.CharField(max_length=20, help_text='Введите описание поля')

    def __str__(self):
        """Строка для представления объекта MyModelName (например, в административной панели и т.д.)."""
        return self.my_field_name
