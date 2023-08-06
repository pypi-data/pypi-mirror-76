import sys
import xml.etree.cElementTree as et
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.validators import (FileExtensionValidator,
                                    get_available_image_extensions)
from django.forms import ImageField as DjangoImageField
from PIL import Image


def validate_image_and_svg_file_extension(value):
    allowed_extensions = get_available_image_extensions() + ['svg']
    return FileExtensionValidator(allowed_extensions=allowed_extensions)(value)


class SVGAndImageFormField(DjangoImageField):
    """
    Form field which handles validation of raster images and svg files.

    Author: Nick Khlestov (ambivalentno)
    https://gist.github.com/ambivalentno/9bc42b9a417677d96a21
    Adapted for Django 3 by ramsrib
    """
    default_validators = [validate_image_and_svg_file_extension]

    def to_python(self, data):
        """
        Checks that the file-upload field data contains a valid image (GIF, JPG,
        PNG, possibly others -- whatever the Python Imaging Library supports).
        """

        # that's intentional
        # pylint: disable=bad-super-call
        test_file = super(DjangoImageField, self).to_python(data)
        if test_file is None:
            return None

        # We need to get a file object for Pillow. We might have a path or we might
        # have to read the data into memory.
        if hasattr(data, 'temporary_file_path'):
            input_file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                input_file = BytesIO(data.read())
            else:
                input_file = BytesIO(data['content'])

        try:
            # load() could spot a truncated JPEG, but it loads the entire
            # image in memory, which is a DoS vector. See #3848 and #18520.
            image = Image.open(input_file)
            # verify() must be called immediately after the constructor.
            image.verify()

            # Annotating so subclasses can reuse it for their own validation
            test_file.image = image
            test_file.content_type = Image.MIME[image.format]
        # pylint: disable=broad-except
        except Exception:
            # add a workaround to handle svg images
            if not self.is_svg(test_file):
                raise ValidationError(
                    self.error_messages['invalid_image'], code='invalid_image',
                ).with_traceback(sys.exc_info()[2])
        if hasattr(test_file, "seek") and callable(test_file.seek):
            test_file.seek(0)
        return test_file

    def is_svg(self, input_file):
        """
        Check if provided file is svg
        """
        input_file.seek(0)
        tag = None
        try:
            for _, element in et.iterparse(input_file, ('start',)):
                tag = element.tag
                break
        except et.ParseError:
            pass
        return tag == '{http://www.w3.org/2000/svg}svg'
