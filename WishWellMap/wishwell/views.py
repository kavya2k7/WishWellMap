import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
from .models import Shelf, BucketItem, Memory, MemoryPhoto, FlowProgress
from .forms import ShelfForm, BucketItemForm, MemoryForm

MOTIVATIONAL_QUOTES = [
    "Your potential is endless. Keep wishing, keep doing!",
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "Every small step brings you closer to your deepest wish.",
    "Believe you can and you're halfway there.",
    "Your dreams don't have an expiration date.",
    "Small daily improvements over time lead to stunning results.",
    "Fill your wish well with endless possibilities.",
    "Dream big, start small, act now.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "You are capable of achieving far more than you imagine.",
    "Don't count the days, make the days count.",
    "A journey of a thousand miles begins with a single step.",
    "Your wish well is limitless—keep adding, keep growing!",
    "Trust the process. The best is coming.",
    "Action is the foundational key to all success.",
    "Make today count towards your future self.",
    "Great things never came from comfort zones.",
    "Turn your wishes into your reality.",
    "Every wish you make is a seed planted for tomorrow.",
    "Stay patient and trust your journey.",
    "Success is the sum of small efforts repeated day in and day out.",
    "Your only limit is your mind.",
    "Start where you are. Use what you have. Do what you can.",
    "Fill your life with wishes, memories, and zero regrets."
]

def award_flow_points(user, pts):
    progress, _ = FlowProgress.objects.get_or_create(user=user)
    progress.points += pts
    progress.save()

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'wishwell/landing.html')

@login_required
def dashboard(request):
    user = request.user
    flow, _ = FlowProgress.objects.get_or_create(user=user)
    total_items = BucketItem.objects.filter(user=user).count()
    completed_items = BucketItem.objects.filter(user=user, status__iexact='Completed').count()
    memories_count = Memory.objects.filter(user=user).count()
    
    upcoming_plans = BucketItem.objects.filter(
        user=user, target_date__isnull=False
    ).exclude(status__iexact='Completed').order_by('target_date')[:5]
    
    recent_memories = Memory.objects.filter(user=user).order_by('-created_at')[:3]
    shelves = Shelf.objects.filter(user=user)

    context = {
        'flow': flow,
        'total_items': total_items,
        'completed_items': completed_items,
        'memories_count': memories_count,
        'upcoming_plans': upcoming_plans,
        'recent_memories': recent_memories,
        'shelves': shelves,
        'quote': random.choice(MOTIVATIONAL_QUOTES),
    }
    return render(request, 'wishwell/dashboard.html', context)

@login_required
def edit_shelf(request, pk):
    shelf = get_object_or_404(Shelf, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ShelfForm(request.POST, instance=shelf)
        if form.is_valid():
            form.save()
            return redirect('shelf_list')
    else:
        form = ShelfForm(instance=shelf)

    return render(request, 'wishwell/shelf_form.html', {
        'form': form,
        'title': 'Edit Shelf',
        'shelf': shelf
    })

@login_required
def shelf_list(request):
    shelves = Shelf.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ShelfForm(request.POST)
        if form.is_valid():
            shelf = form.save(commit=False)
            shelf.user = request.user
            shelf.save()
            award_flow_points(request.user, 5)
            return redirect('shelf_list')
    else:
        form = ShelfForm()
    return render(request, 'wishwell/shelf_list.html', {'shelves': shelves, 'form': form})

@login_required
def bucket_item_list(request):
    items = BucketItem.objects.filter(user=request.user)
    search_query = request.GET.get('search', '')
    shelf_filter = request.GET.get('shelf', '')
    status_filter = request.GET.get('status', '')

    if search_query:
        items = items.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    if shelf_filter:
        items = items.filter(shelf_id=shelf_filter)
    if status_filter:
        # Case-insensitive filtering ensures clicking 'Completed' card works smoothly
        items = items.filter(status__iexact=status_filter)

    shelves = Shelf.objects.filter(user=request.user)
    return render(request, 'wishwell/item_list.html', {
        'items': items,
        'shelves': shelves,
        'search_query': search_query,
        'shelf_filter': shelf_filter,
        'status_filter': status_filter,
    })

@login_required
def add_bucket_item(request):
    if request.method == 'POST':
        form = BucketItemForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            award_flow_points(request.user, 10)
            return redirect('bucket_item_list')
    else:
        form = BucketItemForm(user=request.user)
    return render(request, 'wishwell/item_form.html', {'form': form, 'title': 'Add New Goal'})

@login_required
def edit_bucket_item(request, pk):
    item = get_object_or_404(BucketItem, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BucketItemForm(request.POST, request.FILES, instance=item, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('bucket_item_list')
    else:
        form = BucketItemForm(instance=item, user=request.user)
    
    return render(request, 'wishwell/item_form.html', {
        'form': form, 
        'title': 'Edit Goal',
        'item': item
    })

@login_required
def delete_bucket_item(request, pk):
    item = get_object_or_404(BucketItem, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('bucket_item_list')
    return render(request, 'wishwell/item_confirm_delete.html', {'item': item})

@login_required
def delete_memory(request, pk):
    memory = get_object_or_404(Memory, pk=pk, user=request.user)
    if request.method == 'POST':
        memory.delete()
        return redirect('memories_album')
    return render(request, 'wishwell/item_confirm_delete.html', {'item': memory})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('landing')
    return render(request, 'accounts/delete_account_confirm.html')

@login_required
def add_memory(request, item_id):
    item = get_object_or_404(BucketItem, pk=item_id, user=request.user)
    if request.method == 'POST':
        form = MemoryForm(request.POST)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.bucket_item = item
            memory.user = request.user
            memory.save()

            item.status = 'Completed'
            item.save()

            images = request.FILES.getlist('images')
            for img in images:
                MemoryPhoto.objects.create(memory=memory, image=img)

            award_flow_points(request.user, 30)
            return redirect('memories_album')
    else:
        form = MemoryForm()
    return render(request, 'wishwell/memory_form.html', {'form': form, 'item': item})

@login_required
def memories_album(request):
    memories = Memory.objects.filter(user=request.user).order_by('-completion_date')
    return render(request, 'wishwell/memories_album.html', {'memories': memories})

@login_required
def calendar_view(request):
    return render(request, 'wishwell/calendar.html')

@login_required
def calendar_events_api(request):
    user = request.user
    events = []
    
    # Bucket list target dates
    items = BucketItem.objects.filter(user=user, target_date__isnull=False)
    for item in items:
        events.append({
            'title': f"🎯 {item.title}",
            'start': item.target_date.strftime('%Y-%m-%d'),
            'color': '#005B5C' if item.status.lower() != 'completed' else '#C57B8A'
        })
        
    # Memory completions
    memories = Memory.objects.filter(user=user)
    for mem in memories:
        events.append({
            'title': f"📸 Memory: {mem.bucket_item.title}",
            'start': mem.completion_date.strftime('%Y-%m-%d'),
            'color': '#C57B8A'
        })

    return JsonResponse(events, safe=False)