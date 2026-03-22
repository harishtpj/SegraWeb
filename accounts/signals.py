import logging

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from accounts.models import User, UserFaceEmbedding
from ml_models.face_utils import register_face, FaceRecognitionError


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=User)
def cache_old_profile_photo(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_profile_photo_name = None
        return

    try:
        old_instance = User.objects.get(pk=instance.pk)
        instance._old_profile_photo_name = old_instance.profile_photo.name if old_instance.profile_photo else None
    except User.DoesNotExist:
        instance._old_profile_photo_name = None


@receiver(post_save, sender=User)
def sync_face_embedding_on_photo_change(sender, instance, created, **kwargs):
    new_photo_name = instance.profile_photo.name if instance.profile_photo else None
    old_photo_name = getattr(instance, "_old_profile_photo_name", None)

    photo_changed = created or (new_photo_name != old_photo_name)
    if not photo_changed:
        return

    if not instance.profile_photo:
        UserFaceEmbedding.objects.filter(user=instance).delete()
        logger.info(
            "Removed face embedding because profile photo was deleted",
            extra={"user_id": instance.id, "username": instance.username}
        )
        return

    try:
        instance.profile_photo.open("rb")
        image_bytes = instance.profile_photo.read()
    finally:
        instance.profile_photo.close()

    try:
        register_face(instance, image_bytes)
        logger.info(
            "Face embedding updated successfully",
            extra={"user_id": instance.id, "username": instance.username}
        )
    except FaceRecognitionError as exc:
        logger.warning(
            "Face embedding update skipped: %s",
            str(exc),
            extra={"user_id": instance.id, "username": instance.username}
        )
    except Exception:
        logger.exception(
            "Unexpected error while updating face embedding",
            extra={"user_id": instance.id, "username": instance.username}
        )
