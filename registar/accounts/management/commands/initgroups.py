from django.core.management import BaseCommand
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from registar import settings


class Command(BaseCommand):
    """
    Initializes the groups and permissions.
    """
    help = _('Initializes the groups and permissions.')
    required_settings = [
        "ROLES_PERMISSIONS",
        "ADMIN_ROLE",
        "REGULAR_USER_ROLE",
    ]
    
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--nooutput",
            action="store_true",
            help=_("Do not print any output."),
        )

    def handle(self, *args, **options):
        verbose = not options["nooutput"]

        for role_name, permissions_mapping in settings.ROLES_PERMISSIONS.items():
            if verbose:
                self.stdout.write(f"==== Initialiazing role '{ role_name }' ====\n")
            role, created = Group.objects.get_or_create(name=role_name)

            for model_name, permissions in permissions_mapping.items():
                model = self.get_model(model_name)
                
                if verbose:
                    self.stdout.write(f"Adding permissions for the model { model_name }\n")
                
                self._add_permissions_to_role(permissions, role, model, options=options)

        if verbose:
            self.stdout.write(f"==== Initialiazing admin role '{ settings.ADMIN_ROLE }' ====\n")
        
        admin_role, created = Group.objects.get_or_create(name=settings.ADMIN_ROLE)
        admin_role.permissions.set(Permission.objects.all())
        
        if verbose:
            self.stdout.write(f"Done!\n")

    @staticmethod
    def get_model(model_name):
        """
        Returns the model class.
        """
        try:
            return apps.get_model(model_name)
        except LookupError as exc:
            raise LookupError(f"Model { model_name } does not exist." \
                "Please check the ROLES_PERMISSIONS dictionary in settings.py.") from exc

    def _add_permissions_to_role(self, permissions, role, model, options):
        """
        Adds a permission to a role.
        """
        model_name = model._meta.model_name
        
        for perm_name in permissions:
            codename = f"{ perm_name }_{ model_name }"
            app_label = model._meta.app_label

            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model_name)
                permission = Permission.objects.get(codename=codename, content_type=content_type)

                role.permissions.add(permission)
                if not options["nooutput"]:
                    self.stdout.write(f"-> Added { codename }")

            except Permission.DoesNotExist as exc:
                raise Permission.DoesNotExist(f"Permission '{ codename }' does not exist, " \
                    "though it is mentioned in ROLES_PERMISSIONS.") from exc
  
    def _ensure_settings_exist(self):
        """
        Ensures that the settings are defined.
        """
        for setting in self.required_settings:
            if not hasattr(settings, setting):
                raise AttributeError(f"{ setting } is not defined in settings.py!")
