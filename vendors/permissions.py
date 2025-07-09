from rest_framework.permissions import BasePermission

# Allows only authenticated users in the 'Vendor' group
class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='Vendor').exists()
        )

# Allows only authenticated users in the 'Admin' group or superusers
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and (
                request.user.is_superuser or
                request.user.groups.filter(name='Admin').exists()
            )
        )

# Allows both Admins and Vendors (for read-only views, etc.)
class IsAdminOrVendor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and (
                request.user.is_superuser or
                request.user.groups.filter(name__in=['Admin', 'Vendor']).exists()
            )
        )
