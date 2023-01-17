from django.shortcuts import render
from shop.models import Item, User, Comment, Category
from django.contrib.auth.decorators import login_required
# Create your views here.

def landing(request):
    recent_item = Item.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html', {
        'recent_items' : recent_item
    })

def brand_story(request):
    category = Category.objects.all()
    return render(request, 'single_pages/brand_story.html',{
        'categories' : category
    })
def mypage(request):
    comments = Comment.objects.all()
    items = Item.objects.all()
    comment_list = comments.filter(author=request.user)  # 내가 쓴 댓글만
    item_list = items.filter(like_users=request.user) #내가 좋아요한 상품만
    return render(request, 'single_pages/mypage.html', {'comment_list': comment_list, 'item_list': item_list})
    # return render(request, 'single_pages/mypage.html')
# def category_page(request,slug):
#     category = Category.objects.get(slug=slug)
#     item_list=Item.objects.filter(category=category)
#     return render(request, 'shop/item_list.html', {
#         'category' : category,
#         'item_list' : item_list,
#         'categories' : Category.objects.all(),
#         'no_category_item_count' : Item.objects.filter(category=None).count
#     })