from PIL import Image
import os.path

PROFILE_SIZE = 1000 # 300 avatar size in profile
POST_SIZE = 150    # 80 in post
COMMENT_SIZE = 100 # 50 in comment

LAYOUT_POST_SIZE = 1000   # post picture size in layout
POST_PICTURE_MINI_SIZE = 150    # preview in post update window

def resize_avatar_picture(instance):
    width = instance.width
    height = instance.height
    fullname = instance.path
    max_size = max(width, height)
    min_size = min(width, height)
    image = Image.open(fullname)
    filename, ext = os.path.splitext(fullname)
    if max_size > PROFILE_SIZE:
        left = (width - min_size) // 2
        upper = (height - min_size) // 2
        image = image.convert('RGB').crop((left, upper, left + min_size, upper + min_size))
        image = image.resize((PROFILE_SIZE, PROFILE_SIZE), Image.ANTIALIAS)
    else:
        image = image.convert('RGB')
    image.save(filename + '.jpg', quality=95)
    image_post = image.copy()
    image_comment = image.copy()
    image_post = image_post.resize((POST_SIZE, POST_SIZE), Image.ANTIALIAS)
    image_post.save(filename + "_post" + '.jpg', quality=95)
    image_comment = image_comment.resize((COMMENT_SIZE, COMMENT_SIZE), Image.ANTIALIAS)
    image_comment.save(filename + "_comment" + '.jpg', quality=95)

def resize_post_picture(instance, size): # size = max x or y
    width = instance.width
    height = instance.height
    fullname = instance.path
    max_size = max(width, height)
    min_size = min(width, height)
    image = Image.open(fullname)
    if max_size > size:
        left = (width - min_size) // 2
        upper = (height - min_size) // 2
        image = image.crop((left, upper, left + min_size, upper + min_size))
        image = image.resize((size, size), Image.ANTIALIAS)
    image.save(fullname)