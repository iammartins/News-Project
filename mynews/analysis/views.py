from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import SiteVisit, PostView, CategoryRead, UserActivity
from django.db.models import Count
from news.models import Post, Category
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from .utils import get_client_info

@user_passes_test(lambda u: u.is_superuser)
def analysis_dashboard(request):
    recent_visits = SiteVisit.objects.order_by('-timestamp')[:10]
    daily_visits = SiteVisit.objects.annotate(visit_date=TruncDate('timestamp')).values('visit_date').annotate(count=Count('id')).order_by('visit_date')
    post_views_by_device = PostView.objects.values('device_type').annotate(count=Count('id')).order_by('-count')
    category_reads_by_device = CategoryRead.objects.values('device_type').annotate(count=Count('id')).order_by('-count')
    user_activity_by_action = UserActivity.objects.values('action').annotate(count=Count('id')).order_by('-count')

    context = {
        'recent_visits': recent_visits,
        'daily_visits': daily_visits,
        'post_views_by_device': post_views_by_device,
        'category_reads_by_device': category_reads_by_device,
        'user_activity_by_action': user_activity_by_action,
    }
    return render(request, 'analysis/dashboard.html', context)

def track_site_visit(request):
    client_info = get_client_info(request)
    SiteVisit.objects.create(
        user=request.user if request.user.is_authenticated else None,
        page_url=request.path,
        http_referer=client_info['http_referer'],
        user_agent=client_info['user_agent'],
        device_type=client_info['device_type']
    )
    return HttpResponse('')

def track_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    client_info = get_client_info(request)
    PostView.objects.create(
        post=post,
        user=request.user if request.user.is_authenticated else None,
        http_referer=client_info['http_referer'],
        user_agent=client_info['user_agent'],
        device_type=client_info['device_type']
    )
    return HttpResponse('')

def track_category_read(request, pk):
    category = get_object_or_404(Category, pk=pk)
    client_info = get_client_info(request)
    CategoryRead.objects.create(
        category=category,
        user=request.user if request.user.is_authenticated else None,
        http_referer=client_info['http_referer'],
        user_agent=client_info['user_agent'],
        device_type=client_info['device_type']
    )
    return HttpResponse('')
