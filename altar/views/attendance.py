from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from altar.utils.expressions import SELECT_RELATED_TRAININGS, PREFETCH_RELATED_TRAININGS
from altar.utils.factory import GetSerializedData
from altar.forms.training import AttendanceForm
from altar.models.players import Player
from altar.models.training import Attendance, TrainingSession

# Create your views here.
class AttendanceManagement(LoginRequiredMixin, View):
    template_name = 'app/attendance/attendance_management.html'

    def get(self, request):
        if "action" in request.GET.keys():
            action = request.GET["action"]
            if action == "filter":
                date = request.GET.get('date')

                date = date.split(' - ')
                if date:
                    start = date[0]
                    end = date[1]
                    if start == end:
                        filter = Q(Q(date=start))
                    else:
                        filter = Q(date__range=date)

                response = GetSerializedData(request=request, app_name="altar", model_name="TrainingSession",
                                             query=filter, data_type='sessions', select_related=SELECT_RELATED_TRAININGS,
                                             prefetch_related=PREFETCH_RELATED_TRAININGS, paginated=True, jsonify=True)
                
                return JsonResponse(
                    {
                        **response.response,
                    }
                )
        
        context = {
            'sessions': TrainingSession.objects.all().order_by("-id"),
        }
        return render(request, self.template_name, context)


@login_required
def record_attendance(request, session_id):
    session = get_object_or_404(TrainingSession, pk=session_id)
    ballers = session.players.all()

    # Retrieve the branch associated with the training session
    branch = session.training_branch

    # Filter players based on the branch
    players = Player.objects.filter(player_branch=branch)

    attendance_records = {}
    for player in players:
        attendance = Attendance.objects.filter(player=player, training_session=session).first()
        attendance_records[player] = attendance

    # Marking the attendance
    if request.method == 'POST':
        form = AttendanceForm(request.POST, training_session=session)
        if form.is_valid():
            form.request = request
            form.save(session)
            messages.success(request, f"Attendance marked and saved successfully.")
            return redirect('record_attendance', session_id=session.id)
    else:
        form = AttendanceForm(training_session=session)

    context = {
        'session': session,
        'players': players,
        'ballers': ballers,
        'attendance_records': attendance_records,
        'form': form,
    }
    return render(request, 'app/attendance/attendance_details.html', context)