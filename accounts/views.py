from django.contrib import messages
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView,LogoutView
from user.serializers import RegisterSerializer
from .forms import LoginForm,RegisterForm

# Create your views here.
class RegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        serializer = RegisterSerializer(data=form.cleaned_data)

        if serializer.is_valid():
            serializer.save()
            messages.success(self.request,"Account created sucessfully.")
            return redirect("login")
        
        for field,errors in  serializer.errors.items():
            for error in errors:
                form.add_error(field,error)
        return self.form_invalid(form)


class UserLoginView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    next_page = "home"

class UserLogoutView(LogoutView):
    next_page = "login" 