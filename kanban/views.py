from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.views.generic import DetailView, UpdateView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserForm, ListForm, CardForm, CardCreateFromHomeForm
from .mixin import OnlyYouMixin
from .models import List, Card


class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "kanban/cards/create.html"
    form_class = CardForm
    success_url = reverse_lazy("kanban:home")

    def form_valid(self, form):
        # バリデーションに通った時、下記の挙動
        form.instance.user = self.request.user
        return super().form_valid(form)


class CardCreateFromHomeView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "kanban/cards/create.html"
    form_class = CardCreateFromHomeForm
    success_url = reverse_lazy("kanban:home")

    def from_valid(self, form):
        # バリデーションに通った時、下記の挙動
        list_pk = self.kwargs['list_pk']
        list_instance = get_object_or_404(List, pk=list_pk)
        form.instance.list = list_instance
        form.instance.user = self.request.user
        return super().form_valid(form)  # 実際の保存を行っているコード


class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = "kanban/cards/list.html"


class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "kanban/cards/detail.html"


class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    template_name = "kanban/cards/update.html"
    form_class = CardForm
    success_url = reverse_lazy("kanban:home")

    def get_success_url(self):
        return resolve_url("kanban:cards_detail", pk=self.kwargs['pk'])


class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "kanban/cards/delete.html"
    form_class = CardForm
    success_url = reverse_lazy("kanban:home")


class ListCreateView(LoginRequiredMixin, CreateView):
    model = List
    template_name = "kanban/lists/create.html"
    form_class = ListForm
    success_url = reverse_lazy("kanban:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)  # 実際の保存を行っているコード


class ListListView(LoginRequiredMixin, ListView):
    model = List
    template_name = "kanban/lists/list.html"


class ListDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "kanban/lists/detail.html"


class ListUpdateView(LoginRequiredMixin, UpdateView):
    model = List
    template_name = "kanban/lists/update.html"
    form_class = ListForm

    def get_success_url(self):
        return resolve_url('kanban:lists_detail', pk=self.kwargs['pk'])


class ListDeleteView(LoginRequiredMixin, DeleteView):
    model = List
    template_name = "kanban/lists/delete.html"
    form_class = ListForm
    success_url = reverse_lazy("kanban:lists_list")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "kanban/users/detail.html"


class UserUpdateView(OnlyYouMixin, UpdateView):
    model = User
    template_name = 'kanban/users/update.html'
    form_class = UserForm
    success_url = reverse_lazy("kanban:index")

    # 確認必要
    # def get_succcess_url(self):
    #     return resolve_url('kanban:users_detail', pk=self.kwargs['pk'])


def index(request):
    return render(request, 'kanban/index.html')


class HomeView(LoginRequiredMixin, ListView):
    model = List
    template_name = "kanban/home.html"


def signup(request):
    if request.method == 'POST':        # POSTする際の挙動書く
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect('kanban:home')

    else:                               # GETする際の挙動書く
        form = UserCreationForm()
    context = {
        "form": form
    }
    return render(request, 'kanban/signup.html', context)
