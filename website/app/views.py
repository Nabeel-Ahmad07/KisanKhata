from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import MarketItem, Post, Comment
from django.db.models import Count, Avg


# Create your views here.
def home(request):
    return render(request, 'home.html')

# ✅ Check if user is admin
def is_admin(user):
    return user.is_superuser

# ✅ Admin Dashboard
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    items = MarketItem.objects.all()
    total_items = items.count()
    total_categories = items.values('category').distinct().count()
    total_provinces = items.values('province').distinct().count()
    avg_price = round(items.aggregate(Avg('price'))['price__avg'] or 0, 2)

    return render(request, 'admin_dashboard.html', {
        'items': items,
        'total_items': total_items,
        'total_categories': total_categories,
        'total_provinces': total_provinces,
        'avg_price': avg_price,
    })

# ✅ Add new market item
@login_required
@user_passes_test(is_admin)
def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        province = request.POST.get('province')
        category = request.POST.get('category')

        MarketItem.objects.create(
            name=name,
            price=price,
            province=province,
            category=category
        )
        messages.success(request, 'Item added successfully!')
        return redirect('admin_dashboard')

    return render(request, 'add_item.html')

# ✅ Edit existing market item
@login_required
@user_passes_test(is_admin)
def edit_item(request, item_id):
    item = get_object_or_404(MarketItem, id=item_id)
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.price = request.POST.get('price')
        item.province = request.POST.get('province')
        item.category = request.POST.get('category')
        item.save()
        messages.success(request, 'Item updated successfully!')
        return redirect('admin_dashboard')

    return render(request, 'edit_item.html', {'item': item})

# ✅ Delete market item
@login_required
@user_passes_test(is_admin)
def delete_item(request, item_id):
    item = get_object_or_404(MarketItem, id=item_id)
    item.delete()
    messages.success(request, 'Item deleted successfully!')
    return redirect('admin_dashboard')


def farmer_dashboard(request):
    province = request.GET.get('province')
    category = request.GET.get('category')

    items = MarketItem.objects.all()

    if province:
        items = items.filter(province=province)
    if category:
        items = items.filter(category=category)

    # Mock weather data (can replace later with API)
    weather_data = {
        'Punjab': {'temp': 30, 'condition': 'Sunny ☀️'},
        'Sindh': {'temp': 34, 'condition': 'Hot 🔥'},
        'KPK': {'temp': 22, 'condition': 'Rainy 🌧️'},
        'Balochistan': {'temp': 26, 'condition': 'Cloudy ☁️'},
    }

    selected_weather = weather_data.get(province, None)

    context = {
        'items': items,
        'weather': selected_weather,
        'province': province,
        'category': category,
    }

    return render(request, 'farmer_dashboard.html', context)


from django.contrib import messages
from django.shortcuts import get_object_or_404

# ---------- COMMUNITY FORUM ----------

@login_required
def forum_home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'forum_home.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(author=request.user, title=title, content=content)
        messages.success(request, 'Post created successfully!')
        return redirect('forum_home')
    return render(request, 'create_post.html')


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        comment = request.POST.get('comment')
        if comment:
            Comment.objects.create(post=post, author=request.user, content=comment)
            messages.success(request, 'Comment added!')
            return redirect('post_detail', post_id=post_id)

    comments = post.comments.all().order_by('-created_at')
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Post deleted!')
    return redirect('forum_home')


def market(request):
    province = request.GET.get('province')
    category = request.GET.get('category')

    items = MarketItem.objects.all().order_by('-date')

    if province:
        items = items.filter(province=province)
    if category:
        items = items.filter(category=category)

    context = {
        'items': items,
        'province': province,
        'category': category,
    }
    return render(request, 'market.html', context)

def weather(request):
    return render(request, 'weather.html')