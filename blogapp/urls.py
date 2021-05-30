
from  django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name="index"),
    path('author/<name>',views.getAuthor,name="author"),
    path('articles/<int:id>/',views.getSinglePost,name="single_post"),
    path('topic/<name>/',views.getTopic,name="topic"),
    path('login',views.getLogin,name="login"),
    path('logout',views.getLogout,name="logout"),
    path('create',views.getCreate,name="create"),
    path('profile',views.getProfile,name="profile"),
    path('update/<int:pid>',views.getUpdate,name="update"),
    path('delete/<int:pid>',views.getDelete,name="delete"),
    path('register',views.getRegister,name="register"),
    path('category',views.getCategory,name="category"),
    path('addcategory',views.getAddcategory,name="addcategory"),
    path('delete/category/<int:id>',views.getDeletecategory,name="delectcat"),
    ## For Class Based Fuction
    # path('', views.index.as_view(),name="index"),
    # path('author/<name>',views.getAuthor.as_view(),name="author"),

]
