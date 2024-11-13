from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from .models import UserActivityLog
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class UserActivityLogListView(View):
    """View to list all user activity logs."""
    
    def get(self, request):
        logs = UserActivityLog.objects.all().order_by('-timestamp')
        return render(request, 'admin_panel/user_activity_log_list.html', {'logs': logs})

@method_decorator(login_required, name='dispatch')
class UserActivityLogDetailView(View):
    """View to display details of a specific user activity log."""
    
    def get(self, request, log_id):
        log = get_object_or_404(UserActivityLog, id=log_id)
        return render(request, 'admin_panel/user_activity_log_detail.html', {'log': log})

@method_decorator(login_required, name='dispatch')
class UserActivityLogCreateView(View):
    """View to create a new user activity log."""
    
    def post(self, request):
        user = request.user
        action = request.POST.get('action')
        details = request.POST.get('details')
        ip_address = request.META.get('REMOTE_ADDR')  # Capture IP address
        
        # Create a new log entry
        log = UserActivityLog.objects.create(
            user=user,
            action=action,
            details=details,
            ip_address=ip_address
        )
        
        return JsonResponse({'status': 'success', 'log_id': log.id}, status=201)

# Optional: A view to clear all logs (for admin use)
@method_decorator(login_required, name='dispatch')
class UserActivityLogClearView(View):
    """View to clear all user activity logs."""
    
    def post(self, request):
        UserActivityLog.objects.all().delete()
        return JsonResponse({'status': 'success', 'message': 'All logs have been cleared.'}, status=204)
