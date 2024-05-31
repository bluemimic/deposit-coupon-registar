from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.contrib.auth.models import Group

from registar.settings import REGULAR_USER_ROLE


@receiver(post_save, sender=get_user_model())
def assign_default_group(sender, instance, created, **kwargs):
    """
    Assigns the user to the default group.
    """
    if not created:
        return

    try:
        group = Group.objects.get(name=REGULAR_USER_ROLE)
        instance.groups.add(group)

    except Group.DoesNotExist as exc:
        raise Group.DoesNotExist(f"Group '{ REGULAR_USER_ROLE }' does not exist. " \
            "Run 'python manage.py initgroups' to create groups and permissions.") from exc


@receiver(pre_save, sender=get_user_model())
def ensure_group_is_present(sender, instance, **kwargs):
    """
    Ensures that the default group is present.
    """
    try:
        group = Group.objects.get(name=REGULAR_USER_ROLE)

    except Group.DoesNotExist as exc:
        raise Group.DoesNotExist(f"Group '{ REGULAR_USER_ROLE }' does not exist. " \
            "Run 'python manage.py initgroups' to create groups and permissions.") from exc
