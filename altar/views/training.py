from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from altar.utils.expressions import SELECT_RELATED_TRAININGS
from altar.utils.factory import GetSerializedData
from altar.models.branch import Branches
from altar.forms.training import TrainingSessionExtrasForm, TrainingSessionForm
from altar.models.training import TrainingSession

# Create your views here.
class TrainingManagement(LoginRequiredMixin, View):
    template_name = 'app/training/training_management.html'

    def get(self, request):
        if "action" in request.GET.keys():
            action = request.GET["action"]
            q = request.GET.get("q")
            if action == "get_branches":
                if q:
                    branches = Branches.objects.filter(Q(branch__icontains=q))
                else:
                    branches = Branches.objects.all().order_by('-id')
                return JsonResponse({
                    "branches": [{"id":branch.id, "branch_name":branch.branch} for branch in branches]
                }, safe=False)

        if "action" in request.GET.keys():
            action = request.GET["action"]
            if action == "filter":
                date = request.GET.get('date')
                branch = request.GET.get('branch')

                date = date.split(' - ')
                if date:
                    start = date[0]
                    end = date[1]
                    if start == end:
                        filter = Q(Q(date=start))
                    else:
                        filter = Q(date__range=date)

                if branch:
                    branches = Branches.objects.filter(Q(id__in=branch.split(',')))
                    filter.add(Q(training_branch__in=branches), Q.AND)

                response = GetSerializedData(request=request, app_name="altar", model_name="TrainingSession",
                                             query=filter, data_type='trainings', select_related=SELECT_RELATED_TRAININGS,
                                             prefetch_related=None, paginated=True, jsonify=True)
                
                return JsonResponse(
                    {
                        **response.response,
                    }
                )
        
        context = {
            'trainings': TrainingSession.objects.all().order_by("-id"),
            'form': TrainingSessionForm(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Training schedule created and saved successfully.")
            return redirect('training_management')
        else:
            messages.warning(request, f"Failed to create training session.")
            form = TrainingSessionForm()

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class TrainingDetails(LoginRequiredMixin, View):
    template_name = 'app/training/training_details.html'

    def get(self, request, training_id):
        training = get_object_or_404(TrainingSession, id=training_id)
        form = TrainingSessionExtrasForm(instance=training)

        context = {
        'training': training,
        'form': form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, training_id):
        training = get_object_or_404(TrainingSession, id=training_id)
        form = TrainingSessionExtrasForm(instance=training)
        if request.method == 'POST':
            form = TrainingSessionExtrasForm(request.POST, request.FILES, instance=training)
            if form.is_valid():
                form.save()
                messages.success(request, f"Training session has been updated successfully.")
                return redirect('training_details', training_id=training.id)
            else:
                form = TrainingSessionExtrasForm()

        context = {
        'training': training,
        'form': form
        }
        return render(request, self.template_name, context)
