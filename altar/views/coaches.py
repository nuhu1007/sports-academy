from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from altar.models import Coach
from altar.forms import CoachForm

# Create Here
class CoachesView(LoginRequiredMixin, View):
    template_name = 'app/coaches/coaches_list.html'

    def get(self, request):
        filter_param = request.GET.get('filter')
        if filter_param == 'inactive':
            coaches = Coach.objects.filter(is_active=False)
        else:
            if filter_param:
                coaches = Coach.objects.filter(is_active=True, id=filter_param)
            else:
                coaches = Coach.objects.filter(is_active=True)

        context = {
            'coaches': coaches,
            'form': CoachForm()
        }

        if "action" in request.GET.keys():
            action = request.GET["action"]
            q = request.GET.get("q")
            if action == "get_coaches":
                if q:
                    coaches = Coach.objects.filter(
                        Q(full_name__icontains=q) | Q(phone_number__icontains=q))
                else:
                    coaches = Coach.objects.filter(is_active=True).order_by("-id")

            return JsonResponse({"coaches": [
                {"id": coach.id, "text": coach.full_name + ' ' + str(coach.phone_number or "")} for coach in coaches]})

        return render(request, self.template_name, context)
    

    def post(self, request):
        if 'add_coach' in request.POST:
            form = CoachForm(request.POST, request.FILES)
            if form.is_valid():
                coach = form.save(commit=False)
                coach.save()
                messages.success(request, f"{coach.full_name} registered and saved successfully.")
                return redirect('coaches')
            else:
                messages.warning(request, f"Failed to register coach.")
                form = CoachForm()

        elif 'edit_coach' in request.POST:
            coach_id = request.POST.get('coach_id')
            coach = get_object_or_404(Coach, pk=coach_id)
            edit_form = CoachForm(request.POST, instance=coach)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, f"Coach edited and saved successfully.")
                return redirect('coaches')
            else:
                messages.warning(request, f"Failed to edit.")
                edit_form = CoachForm(instance=coach)

        context = {
            'form': form
        }
        return render(request, self.template_name, context)
    

class DeactivateCoach(LoginRequiredMixin, View):
    def post(self, request, coach_id):
        coach = get_object_or_404(Coach, id=coach_id)
        coach.is_active = False
        coach.date_of_separation = timezone.now()
        coach.save()
        messages.info(request, f"{coach.full_name} has been deactivated successfully.")
        return redirect('coaches')


class ReactivateCoach(LoginRequiredMixin, View):
    def post(self, request, coach_id):
        coach = get_object_or_404(Coach, id=coach_id)
        coach.is_active = True
        coach.date_of_reactivation = timezone.now()
        coach.save()
        messages.info(request, f"{coach.full_name} has been reactivated successfully.")
        return redirect('coaches')
      
