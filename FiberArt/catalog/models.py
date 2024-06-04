from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


class TypeEmbroidery(models.Model):
    Name = models.CharField(max_length=20, help_text='Название типа вышивки')

    def __str__(self):
        return self.Name


class Embroidery(models.Model):
    #User_id = models.ForeignKey(User, on_delete=models.CASCADE, help_text='Создатель')
    User_id = models.ForeignKey(User, related_name='Embroiders', on_delete=models.CASCADE, default='')
    Name = models.CharField(max_length=40, help_text='Название схемы')
    Type_id = models.ForeignKey(TypeEmbroidery, on_delete=models.CASCADE, help_text='Тип вышивки')
    Date = models.DateField(auto_now_add=True)
    Description = models.TextField(default='')
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return f"User: {self.User_id} Name: {self.Name} Date: {self.Date}"

    def get_absolute_url(self):
        return f'embroiders/{self.id}'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000/'+self.image.url
        return ''

    def get_user_name(self):
        return self.User_id.username

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def get_description(self):
        return self.Description.replace('\r\n', '<br>')


class Color(models.Model):
    Name = models.CharField(max_length=40, help_text='Название цвета')
    HEX = models.CharField(max_length=7, help_text='HEX данного цвета')

    def __str__(self):
        return self.Name


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE, default='')
    highlighted = models.TextField(default='')

    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created']
