from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import DesignRequest, Category
from django.contrib import messages

def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def admin_panel(request):
    # Показываем заявки, которые НЕ выполнены (т.е. new и in_progress)
    requests = DesignRequest.objects.filter(status__in=['new', 'in_progress']).order_by('status', '-created_at')
    return render(request, 'requests/admin_panel.html', {'requests': requests})

@user_passes_test(superuser_required)
def change_status(request, pk):
    req = get_object_or_404(DesignRequest, pk=pk)
    current_status = req.status

    if request.method == 'POST':
        new_status = request.POST['status']

        # Проверяем, можно ли изменить статус
        if new_status == 'in_progress':
            if current_status != 'new':
                messages.error(request, 'Статус можно изменить только с "Новая".')
                return redirect('change_status', pk=pk)
            comment = request.POST.get('comment', '').strip()
            if not comment:
                messages.error(request, 'Комментарий обязателен.')
                return redirect('change_status', pk=pk)
            req.status = 'in_progress'
            req.admin_comment = comment
            req.save()
            messages.success(request, 'Статус успешно изменён на "Принято в работу".')
            return redirect('/superadmin/')

        elif new_status == 'done':
            # Разрешаем переход с 'new' или 'in_progress'
            if current_status not in ['new', 'in_progress']:
                messages.error(request, 'Статус можно изменить только с "Новая" или "Принято в работу".')
                return redirect('change_status', pk=pk)
            design_image = request.FILES.get('design_image')
            if not design_image:
                messages.error(request, 'Изображение дизайна обязательно.')
                return redirect('change_status', pk=pk)
            req.status = 'done'
            req.design_image = design_image
            req.save()
            messages.success(request, 'Статус успешно изменён на "Выполнено".')
            return redirect('/superadmin/')

    return render(request, 'requests/change_status.html', {'request': req})

@user_passes_test(superuser_required)
def manage_categories(request):
    if request.method == 'POST':
        name = request.POST['name'].strip()
        if name and not Category.objects.filter(name=name).exists():
            Category.objects.create(name=name)
        return redirect('manage_categories')
    categories = Category.objects.all()
    return render(request, 'requests/manage_categories.html', {'categories': categories})

@user_passes_test(superuser_required)
def delete_category(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    cat.delete() # CASCADE удалит связанные заявки
    return redirect('manage_categories')