from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event, EventAttendee, UserActivityLog
from .serializers import EventSerializer, EventAttendeeSerializer, UserParticipationSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404

class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        attendee, created = EventAttendee.objects.get_or_create(user=request.user, event=event)
        
        # Log the registration
        UserActivityLog.objects.create(
            user=request.user,
            event=event,
            action="Registered",
            timestamp=timezone.now()
        )

        serializer = EventAttendeeSerializer(attendee)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserEventHistoryView(generics.ListAPIView):
    serializer_class = UserParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventAttendee.objects.filter(user=self.request.user)

class EventActivityLogView(generics.ListAPIView):
    serializer_class = EventAttendeeSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return UserActivityLog.objects.filter(event_id=event_id)

class CalendarView(gen(myenv) (base) mark@mark-HP-EliteBook-840-G3:~/FutureFemTech/tech_api$ python manage.py migrate
Traceback (most recent call last):
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/core/checks/urls.py", line 136, in check_custom_error_handlers
    handler = resolver.resolve_error_handler(status_code)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/urls/resolvers.py", line 732, in resolve_error_handler
    callback = getattr(self.urlconf_module, "handler%s" % view_type, None)
                       ^^^^^^^^^^^^^^^^^^^
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/utils/functional.py", line 47, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
                                         ^^^^^^^^^^^^^^^^^^^
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/urls/resolvers.py", line 711, in urlconf_module
    return import_module(self.urlconf_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mark/anaconda3/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/home/mark/FutureFemTech/tech_api/tech_api/urls.py", line 10, in <module>
    from apps.events.views import EventViewSet, EventAttendeeViewSet, UserActivityLogViewSet
ImportError: cannot import name 'EventViewSet' from 'apps.events.views' (/home/mark/FutureFemTech/tech_api/apps/events/views.py)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/mark/FutureFemTech/tech_api/manage.py", line 22, in <module>
    main()
  File "/home/mark/FutureFemTech/tech_api/manage.py", line 18, in main
    execute_from_command_line(sys.argv)
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
    utility.execute()
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/core/management/__init__.py", line 436, in execute
    self.fetch_command(subcommand).run_from_argv(self.argv)
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/core/management/base.py", line 413, in run_from_argv
    self.execute(*args, **cmd_options)
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/core/management/base.py", line 459, in execute
    output = self.handle(*args, **options)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/core/management/base.py", line 107, in wrapper
    res = handle_func(*args, **kwargs)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/core/management/commands/migrate.py", line 101, in handle
    self.check(databases=[database])
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/core/management/base.py", line 486, in check
    all_issues = checks.run_checks(
                 ^^^^^^^^^^^^^^^^^^
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/core/checks/registry.py", line 88, in run_checks
    new_errors = check(app_configs=app_configs, databases=databases)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/core/checks/urls.py", line 138, in check_custom_error_handlers
    path = getattr(resolver.urlconf_module, "handler%s" % status_code)
                   ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/utils/functional.py", line 47, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
                                         ^^^^^^^^^^^^^^^^^^^
  File "/home/mark/FutureFemTech/myenv/lib/python3.12/site-packages/django/urls/resolvers.py", line 711, in urlconf_module
    return import_module(self.urlconf_name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/mark/anaconda3/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/home/mark/FutureFemTech/tech_api/tech_api/urls.py", line 10, in <module>
    from apps.events.views import EventViewSet, EventAttendeeViewSet, UserActivityLogViewSet
ImportError: cannot import name 'EventViewSet' from 'apps.events.views' (/home/mark/FutureFemTech/tech_api/apps/events/views.py)
(myenv) (base) mark@mark-HP-EliteBook-840-G3:~/FutureFemTech/tech_api$ 

erics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # You can implement additional logic to format events for calendar
        return super().get_queryset()

class ParticipationView(generics.ListAPIView):
    serializer_class = UserParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventAttendee.objects.filter(user=self.request.user).select_related('event')
