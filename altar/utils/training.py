from django.db.models import Max

class TrainingAttributes(object):
    attrs = {
        'pk': 'pk',
        'training_branch': 'training_branch.branch',
        'date': 'date',
        'start_time': 'start_time',
        'end_time': 'end_time',
        'location': 'location',
    }

class SessionAttributes(object):
    attrs = {
        'pk': 'pk',
        'training_branch': 'training_branch.branch',
        'date': 'date',
        'players_count': 'get_players_count',
        'last_recorded_at': 'get_last_recorded_at',
    }

    def get_players_count(self, instance):
        return instance.players.count()
    
    def get_last_recorded_at(self, instance):
        # Assuming 'session_attendance' is the reverse related name
        last_attendance = instance.session_attendance.last()
        return last_attendance.recorded_at if last_attendance else 'Not yet recorded'