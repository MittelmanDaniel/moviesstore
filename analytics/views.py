from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Region, UserProfile
from cart.models import Order, Item
from movies.models import Movie

def map_index(request):
    """Main map view showing regional popularity"""
    template_data = {
        'title': 'Local Popularity Map',
        'regions': Region.objects.all()
    }
    return render(request, 'analytics/map.html', {'template_data': template_data})

def get_regional_data(request):
    """API endpoint returning trending movies by region (last 30 days)"""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    regions_data = []
    
    for region in Region.objects.all():
        # Get trending movies in this region (last 30 days)
        trending = Item.objects.filter(
            order__user__profile__region=region,
            order__date__gte=thirty_days_ago
        ).values(
            'movie__id', 'movie__name'
        ).annotate(
            total_purchases=Sum('quantity')
        ).order_by('-total_purchases')[:5]  # Top 5
        
        regions_data.append({
            'code': region.code,
            'name': region.name,
            'lat': float(region.latitude),
            'lng': float(region.longitude),
            'trending_movies': [
                {
                    'movie_id': item['movie__id'],
                    'title': item['movie__name'],
                    'count': item['total_purchases']
                }
                for item in trending
            ],
            'total_purchases': sum(item['total_purchases'] for item in trending)
        })
    
    return JsonResponse({'regions': regions_data})

def region_detail(request, region_code):
    """Detailed view of trending movies in a specific region"""
    region = get_object_or_404(Region, code=region_code.upper())
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Get trending movies in this region
    trending_items = Item.objects.filter(
        order__user__profile__region=region,
        order__date__gte=thirty_days_ago
    ).values(
        'movie__id', 'movie__name', 'movie__price', 'movie__image'
    ).annotate(
        total_purchases=Sum('quantity'),
        unique_buyers=Count('order__user', distinct=True)
    ).order_by('-total_purchases')[:10]
    
    # Get user's purchases if logged in
    user_purchases = []
    if request.user.is_authenticated:
        user_purchases = Item.objects.filter(
            order__user=request.user,
            order__date__gte=thirty_days_ago
        ).values('movie__id', 'movie__name').annotate(
            total=Sum('quantity')
        ).order_by('-total')
    
    template_data = {
        'title': f'Trending in {region.name}',
        'region': region,
        'trending_items': trending_items,
        'user_purchases': user_purchases,
    }
    
    return render(request, 'analytics/region_detail.html', {'template_data': template_data})
