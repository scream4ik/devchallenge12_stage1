from accounts.models import User

from PIL import Image
import io


class SetUpUserMixin:
    """
    Mixin class for user setup
    """

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username='user', email='user@example.com', password='adminadmin'
        )
        self.client.force_login(self.user)


def generate_image_file(format: str = 'png') -> Image:
    """
    Generate test photo file
    """
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, format)
    file.name = 'test.{}'.format(format)
    file.seek(0)
    return file
