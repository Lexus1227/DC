from django.db import models
from django.contrib.auth.models import User

class TextDescription(models.Model):  # Таблица "Текст описания"
    text = models.TextField('Текст')  # Текст
    count_views = models.PositiveIntegerField('Кол-во просмотров', default=0)  # Кол-во просмотров текста

    def __str__(self):  # Для краткого отображения текста используем его первые 30 символов
        return self.text[:30]

    class Meta:  # То, как название таблицы будет отображаться на панели администратора
        verbose_name = 'Текст описания'
        verbose_name_plural = 'Тексты описаний'


class News(models.Model):  # Таблица "Новость"
    title = models.CharField('Название', max_length=50)  # Заголовок до 50 символов
    cover = models.ImageField('Картинка анонса', upload_to='static/news/img/', blank=True) # Обложка новости
    anons = models.CharField('Анонс', max_length=250)  # Анонс до 250 символов
    description = models.ForeignKey(TextDescription, on_delete=models.CASCADE)  # Описание новости
    datetime = models.DateTimeField('Дата и время публикации', auto_now_add=True)  # Дата и время публикации новости

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Comment(models.Model):  # Таблица "Комментарий"
    comment = models.TextField('Комментарий')  # Текст комментария
    description = models.ForeignKey(TextDescription, on_delete=models.CASCADE)  # Текст, к которому написан комментарий
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор комментария
    datetime = models.DateTimeField('Дата и время публикации', auto_now_add=True)  # Дата и время публикации комментария

    def __str__(self):  # Для краткого отображения комментария используем его первые 30 символов
        return self.comment[:30]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class Actor(models.Model):  # Таблица "Актер"
    first_name = models.CharField('Имя', max_length=50)  # Имя актера
    last_name = models.CharField('Фамилия', max_length=50)  # Фамилия актера
    father_name = models.CharField('Отчество', max_length=50, blank=True)  # Отчество актера
    portrait = models.ImageField('Портрет', upload_to='static/news/img/', blank=True)  # Фото актера
    description = models.ForeignKey(TextDescription, on_delete=models.CASCADE)  # Описание актера
    date_born = models.DateField('Дата рождения')  # Дата рождения актера

    def __str__(self):  # Для отображения актера выводим его ФОИ
        return str(self.first_name) + str(self.father_name) + str(self.last_name)

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'


class Film(models.Model):  # Таблица "Фильм"
    name = models.CharField('Название', max_length=50)  # Название фильма
    director = models.CharField('Режиссер', max_length=50)  # Режиссер
    #director = models.ForeignKey('Режиссер', on_delete=models.CASCADE)
    poster = models.ImageField('Постер', upload_to='static/news/img/', blank=True)  # Афиша фильма
    description = models.ForeignKey(TextDescription, on_delete=models.CASCADE)  # Описание фильма
    date_premiere = models.DateField('Дата премьеры')  # Дата премьеры
    actors = models.ManyToManyField(Actor)  # Актеры, снимавшиеся в фильме

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class Director(models.Model):  # Таблица "Режиссер"
    first_name = models.CharField('Имя', max_length=50)  # Имя актера
    last_name = models.CharField('Фамилия', max_length=50)  # Фамилия актера
    father_name = models.CharField('Отчество', max_length=50, blank=True)  # Отчество актера
    date_born = models.DateField('Дата рождения')  # Дата рождения актера

    def __str__(self):  # Для отображения актера выводим его ФОИ
        return str(self.first_name) + str(self.father_name) + str(self.last_name)

    class Meta:
        verbose_name = 'Режиссер'
        verbose_name_plural = 'Режиссеры'
