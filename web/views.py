from django.shortcuts import render,redirect
# Create your views here.
from django.views.generic import CreateView,FormView,TemplateView,ListView
from .forms import LoginForm,UserRegistrationForm,PostForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from api.models import Posts,Comments
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class SignUpView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("signin")

class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self, request,*args,**kw):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                return render(request,self.template_name,{"form":form})


class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    success_url=reverse_lazy("index")
    model=Posts
    context_object_name="posts"

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"your question added successfully")
        return super().form_valid(form)
    def get_queryset(self):
        return Posts.objects.all()

def add_comment(request,*args,**kw):
        id=kw.get("id")
        pst=Posts.objects.get(id=id)
        cmt=request.POST.get("comment")

        Comments.objects.create(post=pst,comment=cmt,user=request.user)
        messages.success(request,"your answer posted successfully")
        return redirect("index")


def like_post_view(request,*args,**kwargs):
    id=kwargs.get("id")
    pst=Posts.objects.get(id=id)
    if pst.like.contains(request.user):
        pst.like.remove(request.user)
    else:
        pst.like.add(request.user)
    return redirect("index")

def signout_view(request,*args,**kw):
    logout(request)
    return redirect("signin")
