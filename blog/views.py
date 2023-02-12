from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserAccount, Post, Comment
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required


def create_account(request):
    if request.method == "POST":
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        email = request.POST["email"]
        username = request.POST["username"]
        pass1 = request.POST["password1"]
        pass2 = request.POST["password2"]
        
        try:
            validate_email(email)
            if pass1 == pass2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email exists..')
                    return render(request, 'create_account.html')
                else:
                    user = User.objects.create_user(username=email, password=pass1)
                    new_user = UserAccount()
                    new_user.user = user
                    new_user.first_name = first_name
                    new_user.last_name = last_name
                    new_user.email = email   
                    new_user.username = username             
                    new_user.save()
                    return redirect("login")
            else:
                messages.info(request, 'Password not matched..')
                return render(request, 'create_account.html')               
        except ValidationError as e:
            messages.info(request, 'Enter a valid e-mail address')
            return render(request, "create_account.html")
    else:
        return render(request, 'create_account.html')
    

def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        
        try:
            validate_email(email)
            user = authenticate(username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("create-post")
            else:
                messages.info(request, 'Email or Password incorrect')
                return render(request, "login.html")
            
        except ValidationError as e:
            messages.info(request, 'Enter a valid e-mail address')
            return render(request, "login.html")
    context = {}
    return render(request, "login.html", context)


@login_required(login_url='/signin')
def create_post(request):   
    if request.method == "POST":       
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES['image']
        
        Post.objects.create(user=request.user, title=title, description=description, image=file)
        
        return redirect('all-post')            
    else:
        context = {}
        return render(request, 'create_post.html', context)  
    

def all_post(request):
    posts = Post.objects.all()
    print(request.user)
    context = {'posts': posts}
    return render(request, "all_post.html", context)


def detail_post(request, post_id):
    posts = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(posts=posts.id)
    print(comments)
    context = {'posts': posts, 'comments': comments}
    return render(request, "detail_post.html", context)


@login_required(login_url='/signin')
def create_comment(request, post_id):
    if request.method=="POST":
        comment = request.POST['comment']
        
        post1 = Post.objects.get(id=post_id)

        new_comment = Comment()
        new_comment.comments = comment
        new_comment.user = request.user
        new_comment.posts = post1
        new_comment.save()
        return redirect('detail-post', post_id=post_id)
       
    posts = Post.objects.get(id=post_id)
    context = {'posts': posts}
    return render(request, "detail_post.html", context)


@login_required(login_url='/signin')
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect("all-post")


@login_required(login_url='/signin')
def all_users(request): 
    users = UserAccount.objects.all()  
    context = {"users": users}
    return render(request, 'all_users.html', context)  


@login_required(login_url='/signin')
def delete_user(request, user_id): 
    user = UserAccount.objects.get(id=user_id)
    user.delete()
    return redirect("all-users")


def user_logout(request):
    logout(request)
    return redirect('login')
    
    
