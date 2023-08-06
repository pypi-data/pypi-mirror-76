from django.db.models.signals import pre_delete, post_init, post_save
from django.dispatch import receiver

from fagsoft.app_configurations.models import GeneralInfoConfiguration


@receiver(pre_delete, sender=GeneralInfoConfiguration)
def logo_pre_delete(sender, instance, **kwargs):
    instance.logo.delete(False)


@receiver(post_init, sender=GeneralInfoConfiguration)
def backup_logo_path(sender, instance, **kwargs):
    instance._current_logo = instance.logo


@receiver(post_save, sender=GeneralInfoConfiguration)
def delete_logo(sender, instance, **kwargs):
    if hasattr(instance, '_current_logo'):
        if instance._current_logo != instance.logo:
            instance._current_logo.delete(save=False)


@receiver(pre_delete, sender=GeneralInfoConfiguration)
def favicon_pre_delete(sender, instance, **kwargs):
    instance.favicon.delete(False)


@receiver(post_init, sender=GeneralInfoConfiguration)
def backup_favicon_path(sender, instance, **kwargs):
    instance._current_favicon = instance.favicon


@receiver(post_save, sender=GeneralInfoConfiguration)
def delete_favicon(sender, instance, **kwargs):
    if hasattr(instance, '_current_favicon'):
        if instance._current_favicon != instance.favicon:
            instance._current_favicon.delete(save=False)
