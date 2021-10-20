from rest_framework.permissions import BasePermission

class BoardPermissions(BasePermission):
  def has_permission(self, request, view):

    if request.user.is_authenticated:
      return True
      
    return False

  def has_object_permission(self, request, view, obj):
    method = request.method

    if method == 'GET':
      return True
    if request.user.id == obj.owner.id:
      return True

    return False