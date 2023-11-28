from typing import Any
from django import http
from django.http.response import HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from .models import Post , Comment , Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages 
from .forms import CreateUpdatePostForm , CommentCreateForm , CommentReplyForm , PostSearchForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeVeiw(View):
    form_class = PostSearchForm
    def get(self,request):
        posts = Post.objects.all()         #order_by('body')  
        if request.GET.get('search_anythings'):
            posts = posts.filter( body__contains =request.GET['search_anythings'])
        return render(request ,'home/index.html' , {'posts' : posts , 'form' : self.form_class})

class PostDetailView(View):
    form_class=CommentCreateForm   
    form_class_reply=CommentReplyForm   

    
    def setup(self, request , *args , **kwargs ) :  #کمتر وصل بشیم دیتابیس
        self.post_instance=get_object_or_404(Post , pk=kwargs['post_id'] , slug=kwargs['post_slug']) 
        return super().setup(request, *args, **kwargs)


    def get(self,request, *args, **kwargs):
        #post = Post.objects.get(id = post_id , slug = post_slug)
        #post=get_object_or_404(Post , id=post_id ,  slug = post_slug) 
        comments = self.post_instance.pcomment.filter(is_reply=False)
        can_like=False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like=True
        return render(request , 'home/detail.html' , {'post':self.post_instance , 'comments':comments ,'form': self.form_class , 'reply_form':self.form_class_reply , 'can_like':can_like })


    @method_decorator(login_required)
    def post(self,request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.user=request.user
            new_post.post=self.post_instance
            new_post.save()
            messages.success(request , 'your post sent successfuly' , 'success')
            return redirect('home:post_detail' , self.post_instance.pk , self.post_instance.slug  )

class DeletePostView(LoginRequiredMixin,View):
    def get(self ,request , post_id ):
        #post=Post.objects.get(id=post_id)
        post=get_object_or_404(Post , id=post_id)
        if post.user.id == request.user.id :  #Post کلش هست اگه بزاری خطاست
            
            post.delete()
            messages.success(request , 'you  delete this post successfuly' , 'success')
        else:
            messages.error(request , 'you can t delete this post' , 'danger')

        return redirect('home:home')
    
class UpdatePostView(LoginRequiredMixin,View):
    form_class=CreateUpdatePostForm

    def setup(self, request , *args , **kwargs ) :  #کمتر وصل بشیم دیتابیس
        self.post_instance=Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request , *args , **kwargs ) :
        post=self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request,'you can t update this post')
            return redirect('home:hoeme')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request, *args, **kwargs):
        post=self.post_instance
        form=self.form_class(instance=post)
        return render(request,'home/update.html' , {'form':form})



    def post(self,request , *args, **kwargs):
        post=self.post_instance
        form=self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug= slugify(form.cleaned_data['body'][:30])             
            new_post.save()
            messages.success(request , 'post is updated successfuly' , 'success')
            return redirect('home:post_detail' , post.id , post.slug )
    
        
class CreatePostView(LoginRequiredMixin,View):
    form_class=CreateUpdatePostForm

    def get(self,request, *args, **kwargs):
        form=self.form_class
        return render(request , 'home/create.html' , {'form':form})


    def post(self,request , *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug= slugify(form.cleaned_data['body'][:30])
            new_post.user=request.user
            new_post.save()
            messages.success(request , 'new post is created successfuly' , 'success')
            return redirect('home:post_detail' , new_post.id , new_post.slug )
    

class PostAddReplyView(LoginRequiredMixin , View):
    form_class = CommentReplyForm

    def post(self , request , post_id , comment_id ):
        post = get_object_or_404(Post , id = post_id)
        comment = get_object_or_404(Comment , id = comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply=form.save(commit=False)
            reply.user=request.user
            reply.post=post
            reply.reply=comment
            reply.is_reply=True
            reply.save()
            messages.success(request , 'you reply on this post succussfuly . ' , 'success')
        return redirect('home:post_detail' , post.id , post.slug)



class PostLikeView(LoginRequiredMixin,View):
    def get(self , request , post_id):
        post=get_object_or_404(Post , id=post_id)
        vote=Vote.objects.filter(post=post , user=request.user)
        if vote.exists():
            messages.error(request , ' you liked it already ' , 'danger')
            
        else:
            Vote.objects.create(post=post , user=request.user)
            messages.success(request , ' you liked this post succussfuly ' , 'success')

        return redirect('home:post_detail' , post.id , post.slug)        

        

# def home(request):
#     return HttpResponse('hello fooooorriiiii')

# Create your views here.
