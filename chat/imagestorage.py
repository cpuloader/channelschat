import os, random, string
from django.utils.deconstruct import deconstructible
from django.core.files.uploadedfile import UploadedFile
from cloudinary_storage.storage import MediaCloudinaryStorage
import cloudinary.uploader

MAIN_SIZE = (1000, 1000)
MINI_SIZE = (100, 100)


@deconstructible
class MyMediaCloudinaryStorage(MediaCloudinaryStorage):
    image_size = MAIN_SIZE
    generate_thumb = False

    def _upload(self, name, content):
        if self.generate_thumb:
            fullpath, ext = os.path.splitext(name)
            filename = os.path.basename(fullpath)
            public_id = filename + '_mini'
        else:
            public_id = "".join(random.choice(string.hexdigits) for i in range(10))            
        options = {
                   'use_filename': False, 
                   'resource_type': self._get_resource_type(name), 
                   'tags': self.TAG,
                   'public_id': public_id,
                   'width' : self.image_size[0], 
                   'height' : self.image_size[1], 
                   'crop' : 'lfill'
                  }
        folder = os.path.dirname(name)
        if folder:
            options['folder'] = folder
        return cloudinary.uploader.upload(content, **options)

    def _save(self, name, content):
        name = self._normalise_name(name)
        name = self._prepend_prefix(name)
        content = UploadedFile(content, name)
        response = self._upload(name, content)
        # reset state:
        self.image_size = MAIN_SIZE
        self.generate_thumb = False
        return response['public_id']

    def set_image_size(self, image_size):
        self.image_size = image_size

    def is_thumb(self, is_thumb=False):
        self.generate_thumb = is_thumb