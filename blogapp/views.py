from django import forms
from django.contrib import auth
from django.db.models.fields import related
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect,Http404 # redirect 
from django.views.static import serve
from .models import article,author,category, comment
from django.contrib.auth import authenticate,login,logout # For Authntication
from django.contrib.auth.models import User
from django.core.paginator import Paginator #for Pagination
from django.db.models import Q # For Search
from .form import createForm,userCrationFrom,createAuthor,commentForm,addCategoryForm,updateCategory # for submit post (ei Function ami make korechi)
from django.contrib import messages # for Message Alert
from django.contrib.auth.forms import UserCreationForm ## For Registration
from django.http import HttpResponseRedirect ## for redirect same Page
# Create your views here.
from django.shortcuts import render,HttpResponse
from django.views import View # for Class Based View Function

from blogapp import form
def index(request):

        post = article.objects.all().order_by('id').reverse()
        search = request.GET.get('q')
        if search:
            post = post.filter(
                Q(title__icontains=search) | # title=> kothai search korbe icontains=> caseinsensetive
                Q(body__icontains=search)
            )

        
        paginator = Paginator(post, 4) # Show 25 contacts per page. => pagination
        page_number = request.GET.get('page') # => pagination
        total_article = paginator.get_page(page_number)# => pagination
        context ={
            "post":total_article,
            # "total_article":total_article
        }
        return render(request,"index.html",context)

def getAuthor(request,name):
    post_author = get_object_or_404(User, username=name) # author er name khojlo 
    auth = get_object_or_404(author,name=post_author.id)
    post = article.objects.filter(article_author=auth)
    context = {
        "auth":auth,
        "post":post
    }
    return render(request,"profile.html",context)

def getSinglePost(request,id):
    post = get_object_or_404(article, pk=id)
    first= article.objects.first()
    get_comment= comment.objects.filter(post=id) # id onujayi Comment dekhabe
    last = article.objects.last()
    related= article.objects.filter(category=post.category).exclude(id=id)[:4] ## [For related post] => exclude(id=id) means je category er post e click korbe sei post chara onno post dekhabe  >> [:4] means=> limit 4
    form= commentForm(request.POST or None, request.FILES or None) # for show Comment Form
    if form.is_valid():
        isinstance= form.save(commit=False)
        isinstance.post=post # ekhane Id dewa jabena 
        isinstance.save()
        messages.success(request, 'Your Comment Added')
        return HttpResponseRedirect(request.path_info)
    context ={
        "post":post,
        "first":first,
        "last":last,
        "related":related,
        "form":form,
        "comments":get_comment,
    }
    return render(request,'single.html',context)

def getTopic(request,name):
    cat = get_object_or_404(category, name=name) # URL e je category name aslo ta dhore cat e rakhlam
    post = article.objects.filter(category=cat.id) # category (Jake Forenkey Kora ache)=cat.id (je name cat e pabe tar id) => so category id diye sob category post pawawa jabe
    return render(request,'category.html',{"post":post,"cat":cat})
def getLogin(request):
    if request.user.is_authenticated: ##  Jodi user login thake
       return redirect('index') 
    else:
        if request.method == "POST":
            user = request.POST.get('username')
            password = request.POST.get('password')
            auth = authenticate(request,username=user, password=password) # check username and password database ache na ki
            if auth is not None:
                login(request,auth)
                messages.success(request, 'Welcome '+user)
                return redirect('index')
            else:
                messages.error(request, 'Username Or Password Dose Not Match!!')
    return render(request,'login.html')

def getLogout(request):
    logout(request)
    return redirect('login')

def getCreate(request):
    if request.user.is_authenticated: ## jodi user login thake tahole create page e jete dibe
            user= get_object_or_404(User, id=request.user.id)
            author_profile= author.objects.filter(name = user.id)
            if author_profile:
                # form =createForm()
                u = get_object_or_404(author, name=request.user.id) # for Current user id
                form =createForm(request.POST or None, request.FILES or None) ## request.FILES => jodi kono file upload kori
                if form.is_valid():
                    isinstance= form.save(commit=False)
                    isinstance.article_author=u # current username ke article_author e pathabe
                    isinstance=form.save()
                    messages.success(request, 'Thanks For Posting Articles ')
                    return redirect('index')
                return render(request,"create_post.html",{'form':form})
            else:
                return redirect('profile')

    else:
        return redirect('login')

def getProfile(request):
    if request.user.is_authenticated:
        user= get_object_or_404(User, id=request.user.id)
        author_profile= author.objects.filter(name = user.id)
        if author_profile: # jodi user er Auth profile Thake
            user= get_object_or_404(author, name=request.user.id)
            auth = get_object_or_404(author,name=request.user.id)
            post= article.objects.filter(article_author=auth).order_by('id').reverse()
            paginator = Paginator(post, 5) # Show 25 contacts per page. => pagination
            page_number = request.GET.get('page') # => pagination
            total_article = paginator.get_page(page_number)# => pagination
            context ={
                "post":total_article,
                "user":user
            }

            return render(request,"user_profile.html",context)
        else:
            u= get_object_or_404(User, id=request.user.id)
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                isinstance= form.save(commit=False)
                isinstance.name=u
                isinstance.save()
                messages.success(request, 'Author Profile Updated !! ')
                return redirect('profile')
            return render(request,"create_author.html",{"form":form})
    else:
        return redirect("login")

def getUpdate(request,pid):
    if request.user.is_authenticated: ## jodi user login thake tahole create page e jete dibe
            u = get_object_or_404(author, name=request.user.id) # for Current user id
            post= get_object_or_404(article,id=pid) # post er id dhora holo
            form =createForm(request.POST or None, request.FILES or None, instance=post) ## request.FILES => jodi kono file upload kori
            if form.is_valid():
                isinstance= form.save(commit=False)
                isinstance.article_author=u # current username ke article_author e pathabe
                isinstance=form.save()
                messages.success(request, 'Post Succesfully Updated !! ')
                return redirect('profile')
            return render(request,"create_post.html",{'form':form})

    else:
        return redirect('login')
def getDelete(request,pid):
    if request.user.is_authenticated:
        post = get_object_or_404(article,id=pid)
        post.delete()
        messages.warning(request, 'Post Deleted Succesfully!!!! ')
        return redirect('profile')
    else:
        return redirect('login')

def getRegister(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        form = userCrationFrom(request.POST or None)
        if form.is_valid():
            isinstance= form.save(commit=False)
            isinstance.save()
            messages.success(request,"Registration Completed Succesfully")
            return redirect('login')
        return render(request,"register.html",{"form":form})



def getCategory(request):
    query = category.objects.all()
    return render(request,"category_list.html",{"category":query})
def getAddcategory(request):
    form = addCategoryForm(request.POST or None)
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            if form.is_valid():
                isinstance = form.save(commit=False)
                isinstance.save()
                messages.success(request, "Category Succesfully Added")

                return redirect ("category")
        else:
            return redirect("category")
    return render(request,"create_category.html",{"form":form})

def getDeletecategory(request,id):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            post = get_object_or_404(category,id=id)
            post.delete()
            messages.warning(request, 'Post Deleted Succesfully!!!! ')
            return redirect ("category")
    else:
        return redirect("category")





# Class Based View START
# class index(View):
#     def get(self, request):
#         post = article.objects.all().order_by('id').reverse()
#         search = request.GET.get('q')
#         if search:
#             post = post.filter(
#                 Q(title__icontains=search) | # title=> kothai search korbe icontains=> caseinsensetive
#                 Q(body__icontains=search)
#             )

        
#         paginator = Paginator(post, 4) # Show 25 contacts per page. => pagination
#         page_number = request.GET.get('page') # => pagination
#         total_article = paginator.get_page(page_number)# => pagination
#         context ={
#             "post":total_article,
#             # "total_article":total_article
#         }
#         return render(request,"index.html",context)

# class getAuthor(View):
#     def get(self, request,name):
#         post_author = get_object_or_404(User, username=name) # author er name khojlo 
#         auth = get_object_or_404(author,name=post_author.id)
#         post = article.objects.filter(article_author=auth)
#         context = {
#             "auth":auth,
#             "post":post
#         }
#         return render(request,"profile.html",context)

## Class Based View END