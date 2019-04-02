from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View


# Create your views here.

class SignUpView(View):
    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, 'signup.html', context)

    def post(self, request):
        print(request.POST)
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/accounts/login')

        context = {
            'form': form
        }
        return render(request, 'signup.html', context)
