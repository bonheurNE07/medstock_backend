from rest_framework.permissions import BasePermission

from django.contrib.auth.models import Group

# Create groups in admin: "Admin", "Agent"

class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Agent").exists()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Admin").exists()