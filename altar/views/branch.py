from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, OuterRef, Subquery, IntegerField

from altar.forms.branch import BranchForm
from altar.models.branch import Branches
from altar.models.coaches import Coach
from altar.models.players import Player

# Create your views here.

@login_required
def branches(request):
    # Subquery to get the player count & coach count for each branch
    player_count_subquery = Player.objects.filter(player_branch=OuterRef('pk')).values('player_branch').annotate(count=Count('*')).values('count')
    coach_count_subquery = Coach.objects.filter(coaching_branch=OuterRef('pk')).values('coaching_branch').annotate(count=Count('*')).values('count')
    branches = Branches.objects.annotate(player_count=Subquery(player_count_subquery, output_field=IntegerField()), coach_count=Subquery(coach_count_subquery, output_field=IntegerField()))
    form = BranchForm()

    # Creating or Editing a branch
    if request.method == 'POST':
        if 'add_branch' in request.POST: # Check if the form is for adding a branch
            form = BranchForm(request.POST)
            if form.is_valid():
                branch = form.save(commit=False)
                branch.save()
                messages.success(request, f"Branch added and saved successfully.")
                return redirect('branches')
            else:
                messages.error(request, f"Failed to add.")
                form = BranchForm()

        elif 'edit_branch' in request.POST:
            branch_id = request.POST.get('branch_id')
            branch = get_object_or_404(Branches, pk=branch_id)
            edit_form = BranchForm(request.POST, instance=branch)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, f"Branch edited and saved successfully.")
                return redirect('branches')
            else:
                messages.error(request, f"Failed to edit and save.")
                edit_form = BranchForm(instance=branch)

    context = {
        'branches': branches,
        'form': BranchForm(),
    }
    return render(request, 'app/branches.html', context)


class BranchesView(LoginRequiredMixin, View):
    template_name = 'app/branches.html'

    def get(self, request):
        # Subquery to get the player count & coach count for each branch
        player_count_subquery = Player.objects.filter(player_branch=OuterRef('pk')).values('player_branch').annotate(count=Count('*')).values('count')
        coach_count_subquery = Coach.objects.filter(coaching_branch=OuterRef('pk')).values('coaching_branch').annotate(count=Count('*')).values('count')
        branches = Branches.objects.annotate(player_count=Subquery(player_count_subquery, output_field=IntegerField()), coach_count=Subquery(coach_count_subquery, output_field=IntegerField()))
        form = BranchForm()

        context = {
            'branches': branches,
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = BranchForm(request.POST)
        if 'add_branch' in request.POST: # Check if the form is for adding a branch
            form = BranchForm(request.POST)
            if form.is_valid():
                branch = form.save(commit=False)
                branch.save()
                messages.success(request, f"Branch added and saved successfully.")
                return redirect('branches')
            else:
                messages.error(request, f"Failed to add.")
                form = BranchForm()

        elif 'edit_branch' in request.POST: # Check if the form is for editing a branch
            branch_id = request.POST.get('branch_id')
            branch = get_object_or_404(Branches, pk=branch_id)
            edit_form = BranchForm(request.POST, instance=branch)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, f"Branch edited and saved successfully.")
                return redirect('branches')
            else:
                messages.error(request, f"Failed to edit and save.")
                edit_form = BranchForm(instance=branch)

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

class DeleteBranch(LoginRequiredMixin, View):
    def post(self, request, branch_id):
        branch = get_object_or_404(Branches, id=branch_id)
        branch.delete()
        messages.info(request, f"Branch deleted successfully")
        return redirect('branches')