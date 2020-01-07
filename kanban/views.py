from django.shortcuts import render

# Create your views here.
# from django.http import HttpResponse

def index(request):
    return render(request, 'kanban/index.html')

def home(request):
    return render(request, 'kanban/home.html')

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
