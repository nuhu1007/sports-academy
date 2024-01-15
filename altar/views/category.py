from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from altar.forms.category import CategoryForm
from altar.models.category import Categories

# Create your views here.

# Category View
@login_required
def categories(request):
    categories = Categories.objects.annotate(player_count=Count('player_category'))
    form = CategoryForm()

    # Creating or Editing a category
    if request.method == 'POST':
        if 'add_category' in request.POST:  # Check if the form is for adding a category
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.save()
                messages.success(request, f"Category added and saved successfully.")
                return redirect('categories')
            else:
                messages.error(f"Failed to add.")
                form = CategoryForm()
            
        elif 'edit_category' in request.POST:  # Check if the form is for editing a category
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Categories, pk=category_id)
            edit_form = CategoryForm(request.POST, instance=category)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, f"Category edited and saved successfully.")
                return redirect('categories')
            else:
                messages.error(request, f"Failed to edit.")
                edit_form = CategoryForm(instance=category)

    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'app/categories.html', context)

@require_POST
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Categories, pk=category_id)
    category.delete()
    return JsonResponse({'message': 'Category deleted successfully.'})


class DeleteCategory(LoginRequiredMixin, View):
    def post(self, request, category_id):
        category = get_object_or_404(Categories, id=category_id)
        category.delete()
        messages.info(request, f"Category deleted successfully.")
        return redirect('categories')