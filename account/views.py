from typing import Any
from django import http
from django.views import View
from django.shortcuts import render , redirect ,get_object_or_404
from .forms import UserRegestrationForm , UserLoginForm
from  django.contrib.auth.models import User 
from  django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation



class UserRegesterVeiw(View):
    form_class = UserRegestrationForm
    template_name='account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self,request):
        form = self.form_class()
        return render(request,self.template_name,{'form':form})
    
    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password1'])
            messages.success(request ,'you loggedin successfuly', 'success')
            return redirect('home:home')
        return render(request,self.template_name,{'form':form})
    
    
class UserLogInView(View):

    def setup(self, request , *args , **kwargs ):
        self.next = request.GET.get('next')  #get('next' , 'kooft') --اگه next نبود کوفت 
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    form_class = UserLoginForm
    template_name='account/login.html'

    def get(self , request):
        form =self.form_class
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user = authenticate(request , username=cd['username'] , password=cd['password'] )
            if user is not None:
                login(request,user)
                messages.success(request,'log in sucessusfuly ' , 'success' )
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request , 'your password or username is wrong' , 'warning' )
            
        return render(request,self.template_name,{'form':form})
        
class UserLogoutView(LoginRequiredMixin , View):

    #login_url='/account/login/'  #اگه اینو نزاری acounts در نظرش می گیره
    #می تونی همینو با حروف بزرگ تو setting بنویسی
    #تو ستینگ بهتره

    def get(self , request):
        logout(request)
        messages.success(request,'you logged out successfuly' , 'success' )
        return redirect('home:home')
    
class UserProfileView(LoginRequiredMixin,View):
    template_name = 'account/profile.html'

    def get(self , request , user_id):
        is_following = False
        user=User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user , to_user=user)
        if relation.exists():
            is_following=True
        #posts=Post.objects.filter(user=user)
        posts=user.posts.all()
        return render(request, self.template_name ,{'user':user , 'posts' : posts , 'is_following': is_following } )  
    
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name= 'account/password_reset_confirm.html'
    success_url=reverse_lazy('account:password_reset_complete')



class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UsrFollowView(LoginRequiredMixin,View):
    def get( self ,request ,user_id ):
        user = User.objects.get( pk = user_id)
        relation = Relation.objects.filter( from_user=request.user , to_user=user )
        if relation.exists():
            messages.error(request , 'you followed this user already' , 'danger')
            
        else:
            #Relation.objects.create( from_user=request.user , to_user=user )
            #Relation( from_user=request.user , to_user=user ).save()
            relation=Relation( from_user=request.user , to_user=user )
            relation.save()
            messages.success(request , 'you followed this user successfuly' , 'success')

        return redirect('account:user_profile' , user.id)

    

class UsrUnFollowView(LoginRequiredMixin,View):
        
        def get( self ,request ,user_id ):
            user = User.objects.get( pk = user_id)
            relation = Relation.objects.filter( from_user=request.user , to_user=user )
            if  relation.exists():
                relation.delete()
                messages.success(request , 'you unfollowed this user successfuly' , 'success')
                
                
            else:
                messages.error(request , 'you are not following this user' , 'danger')

            return redirect('account:user_profile' , user.id)
    





        
    

    
    
