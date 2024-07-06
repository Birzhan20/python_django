from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)

    agreement_accepted = models.BooleanField(default=False)


def profile_images_directory_path(instance, filename):
    return "users/user_{id}/images/{filename}".format(
        id=instance.user.id,
        filename=filename,
    )


def profile_preview_directory_path():
    pass


class ProductImage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(null=True, blank=True, upload_to=profile_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)
