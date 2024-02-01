from rest_framework import permissions



class IsEditorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permitir el acceso a usuarios autenticados para operaciones de lectura
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        # Solo permitir el acceso a usuarios editores para operaciones de escritura
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='editor').exists()
