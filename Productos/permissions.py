from rest_framework import permissions

class IsBodeguero(permissions.BasePermission):
    """
    Permiso personalizado para permitir que solo los usuarios de tipo 'bodeguero' puedan editar.
    """

    def has_permission(self, request, view):
        # Comprueba si el usuario está autenticado y si su tipo es 'bodeguero'
        return request.user.is_authenticated and request.user.tipo == 'bodeguero'
