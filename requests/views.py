from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DesignRequest, Category

def home(request):
    done_requests = DesignRequest.objects.filter(status='done').order_by('-created_at')[:4]
    in_progress_count = DesignRequest.objects.filter(status='in_progress').count()
    return render(request, 'requests/home.html', {
        'done_requests': done_requests,
        'in_progress_count': in_progress_count
    })

@login_required
def profile(request):
    status_filter = request.GET.get('status')
    qs = DesignRequest.objects.filter(user=request.user)
    if status_filter:
        qs = qs.filter(status=status_filter)
    requests = qs.order_by('-created_at')
    return render(request, 'requests/profile.html', {
        'requests': requests,
        'status_filter': status_filter
    })

@login_required
def create_request(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category_id = request.POST['category']
        image = request.FILES.get('image')

        if not image:
            messages.error(request, 'Изображение обязательно.')
            return redirect('create_request')
        if image.size > 2 * 1024 * 1024:
            messages.error(request, 'Размер изображения не должен превышать 2 МБ.')
            return redirect('create_request')
        if image.content_type not in ['image/jpeg', 'image/png', 'image/bmp']:
            messages.error(request, 'Недопустимый формат изображения.')
            return redirect('create_request')

        category = Category.objects.get(id=category_id)
        DesignRequest.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            image=image
        )
        return redirect('profile')

    categories = Category.objects.all()
    return render(request, 'requests/create_request.html', {'categories': categories})

@login_required
def delete_request(request, pk):
    req = get_object_or_404(DesignRequest, pk=pk, user=request.user)
    if req.status != 'new':
        messages.error(request, 'Нельзя удалить заявку, которая уже в работе или выполнена.')
        return redirect('profile')
    if request.method == 'POST':
        req.delete()
        return redirect('profile')
    return render(request, 'requests/confirm_delete.html', {'request_obj': req})