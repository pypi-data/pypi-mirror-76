from os.path import join

from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "v42ut0d27#6cqek=v&a69b*0%pjwackaky&n#$nv4k4^oo)24k"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

STATIC_ROOT = join(BASE_DIR, "static")  # noqa: F405
BUILD_DIR = join(BASE_DIR, "build")  # noqa: F405
MEDIA_ROOT = join(BASE_DIR, "media")  # noqa: F405
