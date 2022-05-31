from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from Models import News, Comment, Film, Actor
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.base import TemplateView

from .form import CommentForm

class NewsDetailView(FormMixin, DetailView):  # Для отображения отдельных новостей
    model = News
    form_class = CommentForm
    template_name = 'news/detail_view.html'
    context_object_name = 'news'  # Имя ключа для словаря при передаче в render

    def check_status_comments(self):
        res_comments = []
        now_news_comments = super(DetailView, self).get_object().description.comment_set.all()
        now_groups = self.request.user.groups.all().values_list('name')[0]
        for comment in now_news_comments:
            res = [comment]
            comment_groups = comment.author.groups.all().values_list('name')[0]
            if (('moderator' in now_groups and
                 'moderator' not in comment_groups and
                 'admin' not in comment_groups) or
                    'admin' in now_groups or comment.author.username == self.request.user.username):
                res += [True]
            else:
                res += [False]
            res_comments += [res]
        return res_comments

    def get_context_data(self, *args, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['comments'] = self.check_status_comments()
        return context

    def get_object(self):
        news = super(DetailView, self).get_object()
        if self.request.method != 'POST':
            news.description.count_views += 1  # Увеличиваем счетчик просмотров
            news.description.save()
        return news

    def get_success_url(self):
        return '/news/' + str(self.get_object().id)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.description = self.get_object().description
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


def delete_comment(request, id):  # Удаление комментария
    comment = Comment.objects.get(id=id)
    comment.delete()
    return HttpResponseRedirect(f"/news/{comment.description.id}")


def news_home(request):
    news = News.objects.order_by('-datetime')[:10]  # 10 последних новостей на экране
    return render(request, 'news/home.html', {'news' : news})

def main(request):  # Главная страница сайта
    return render(request, 'main/main.html')


def about(request):  # Страница описания компании
    return render(request, 'main/about.html')


class FilmsDetailView(FormMixin, DetailView):  # Для отображения отдельных фильмов
    model = Film
    form_class = CommentForm
    template_name = 'main/films_detail_view.html'
    context_object_name = 'film'  # Имя ключа для словаря при передаче в render

    def check_status_comments(self):
        res_comments = []
        now_news_comments = super(DetailView, self).get_object().description.comment_set.all()
        now_groups = self.request.user.groups.all().values_list('name')[0]
        for comment in now_news_comments:
            res = [comment]
            comment_groups = comment.author.groups.all().values_list('name')[0]
            if (('moderator' in now_groups and
                 'moderator' not in comment_groups and
                 'admin' not in comment_groups) or
                    'admin' in now_groups or comment.author.username == self.request.user.username):
                res += [True]
            else:
                res += [False]
            res_comments += [res]
        return res_comments

    def get_context_data(self, *args, **kwargs):
        context = super(FilmsDetailView, self).get_context_data(**kwargs)
        context['comments'] = self.check_status_comments()
        return context

    def get_object(self):
        film = super(DetailView, self).get_object()
        if self.request.method != 'POST':
            film.description.count_views += 1  # Увеличиваем счетчик просмотров
            film.description.save()
        return film

    def get_success_url(self):
        return '/films/' + str(self.get_object().id)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.description = self.get_object().description
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


def delete_comment_films(request, id):  # Удалить комментарий к фильму
    comment = Comment.objects.get(id=id)
    comment.delete()
    return HttpResponseRedirect(f"/films/{comment.description.film_set.all()[0].id}")


def films(request):  # Страница с фильмами
    filmss = Film.objects.order_by('name')
    return render(request, 'main/films.html', {'films' : filmss})


class ActorsDetailView(FormMixin, DetailView):  # Для отображения отдельных актеров
    model = Actor
    form_class = CommentForm
    template_name = 'main/actor_detail_view.html'
    context_object_name = 'actor'  # Имя ключа для словаря при передаче в render

    def check_status_comments(self):
        res_comments = []
        now_news_comments = super(DetailView, self).get_object().description.comment_set.all()
        now_groups = self.request.user.groups.all().values_list('name')[0]
        for comment in now_news_comments:
            res = [comment]
            comment_groups = comment.author.groups.all().values_list('name')[0]
            if (('moderator' in now_groups and
                 'moderator' not in comment_groups and
                 'admin' not in comment_groups) or
                    'admin' in now_groups or comment.author.username == self.request.user.username):
                res += [True]
            else:
                res += [False]
            res_comments += [res]
        return res_comments

    def get_context_data(self, *args, **kwargs):
        context = super(ActorsDetailView, self).get_context_data(**kwargs)
        context['comments'] = self.check_status_comments()
        return context

    def get_object(self):
        actor = super(DetailView, self).get_object()
        if self.request.method != 'POST':
            actor.description.count_views += 1  # Увеличиваем счетчик просмотров
            actor.description.save()
        return actor

    def get_success_url(self):
        return '/actors/' + str(self.get_object().id)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.description = self.get_object().description
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


def delete_comment_actors(request, id):  # Удалить комментарий к актерам
    comment = Comment.objects.get(id=id)
    comment.delete()
    return HttpResponseRedirect(f"/actors/{comment.description.actor_set.all()[0].id}")


def actors(request):  # Страница с актерами
    actorss = Actor.objects.order_by('first_name')
    return render(request, 'main/actors.html', {'actors' : actorss})


class MainView(TemplateView):
    template_name = 'main/main.html'

    def get(self, request):
        return render(request, self.template_name, {})


class RegisterFormView(FormView):  # Форма для регистрации нового пользователя
    form_class = UserCreationForm
    success_url = '../login'

    template_name = 'main/register.html'

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.groups.add(Group.objects.get(name='visitor'))
        new_user.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


class LoginFormView(FormView):  # Форма для авторизации нового пользователя
    form_class = AuthenticationForm
    success_url = "../"

    template_name = "main/login.html"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):  # Форма для выхода из аккаунта
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("../")
