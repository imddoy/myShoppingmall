from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Item, Category, Tag, Comment, Company
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets
from .serializers import itemSerialzer

class itemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = itemSerialzer

# Create your views here.
class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['title', 'hook_text', 'content', 'image', 'price', 'company', 'tip', 'category']
    template_name = 'shop/item_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ItemUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(ItemUpdate,self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()  # 맨 앞뒤 공백 제거
            tags_str = tags_str.replace(',', ';')  # ,를 ;로 변경
            tag_list = tags_str.split(';')
            for t in tag_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemUpdate, self).get_context_data()
        if self.object.tags.exists:
            tag_str_list = list()
            for t in self.object.tags.all():
                tag_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tag_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count()
        return context

class ItemCreate(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = Item
    fields= ['title', 'hook_text', 'content', 'image', 'price', 'company', 'tip', 'category']
    #모델명_form.html

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(ItemCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip() #맨 앞뒤 공백 제거
                tags_str = tags_str.replace(',',';') #,를 ;로 변경
                tag_list = tags_str.split(';')
                for t in tag_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/shop/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['companies'] = Company.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count()
        return context

class ItemList(ListView):
    model = Item
    ordering = '-pk'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['companies'] = Company.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count()
        return context
    #템플릿은 모델명_list.html : item_list.html
    #매개변수 모델명_list : item_list


class ItemSearch(ItemList): #ListView 상속, item_list, item_list.html 상속
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        item_list = Item.objects.filter(Q(title__contains=q) | Q(tags__name__contains=q)).distinct()
        return item_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemSearch,self).get_context_data()
        q = self.kwargs['q']
        context['search_info']=f'Search: {q} ({self.get_queryset().count()})'
        return context

class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data() #오버라이딩 후 추가요소 context 딕셔너리에 담아 템플릿에 보낼 수 있음
        context['categories']=Category.objects.all()
        context['companies'] = Company.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['comment_form'] = CommentForm
        return context
    #템플릿은 모델명_detail.html : item_detail.html
    #매개변수 모델명 : item

# def index(request):
#     posts = Post.objects.all().order_by('-pk') #모든 books를 가져옴, pk역순으로 나열
#     return render(request, 'blog/index.html', {'posts': posts})
#
# def single_post_page(request, pk):
#     post1 = Post.objects.get(pk=pk)
#     return render(request, 'blog/single_post_page.html', {'post': post1})

#오류나서 잠시 주석핳게여
def new_comment(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.item = item
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else: #GET
            return redirect(item.get_absolute_url())
    else: #로그인 안한 사용자
        raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    item = comment.item
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(item.get_absolute_url())
    else:
        PermissionDenied


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    #comment_form

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def category_page(request,slug):
    category = Category.objects.get(slug=slug)
    item_list=Item.objects.filter(category=category)
    return render(request, 'shop/item_list.html', {
        'category' : category,
        'item_list' : item_list,
        'categories' : Category.objects.all(),
        'companies': Company.objects.all(),
        'no_category_item_count' : Item.objects.filter(category=None).count
    })
def company_page(request,slug):
    company = Company.objects.get(slug=slug)
    item_list=Item.objects.filter(company=company)
    return render(request, 'shop/item_list.html', {
        'company' : company,
        'item_list' : item_list,
        'categories' : Category.objects.all(),
        'companies': Company.objects.all(),
        'no_category_item_count' : Item.objects.filter(category=None).count
    })

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    item_list = tag.item_set.all()
    return render(request, 'shop/item_list.html',{
                  'tag' : tag,
                  'item_list' : item_list,
                  'categories': Category.objects.all(),
        'companies': Company.objects.all(),
        'no_category_item_count':Item.objects.filter(category=None).count
    })
def hottem(request):
    item_list=Item.objects.all()
    return render(request, 'shop/hottem_list.html', {
        'item_list' : item_list,
        'categories' : Category.objects.all(),
        'companies' : Company.objects.all(),
        'no_category_item_count' : Item.objects.filter(category=None).count
    })

def like_post(request, post_id):
    item = get_object_or_404(Item, id=post_id)
    if request.user in item.like_users.all():
        item.like_users.remove(request.user)
    else:
        item.like_users.add(request.user)
    return redirect(item.get_absolute_url())
# def likes(request, pk):
#     if request.user.is_authenticated:
#         item = get_object_or_404(Item, pk=pk)
#
#         if item.like.filter(id=request.user.id).exists():
#             item.like.remove(request.user)
#         else:
#             item.like.add(request.user)
#         # return redirect('likes')
#     return redirect('accounts:login')