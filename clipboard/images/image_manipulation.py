from PIL import Image

from .s3_connections import upload_image_to_hf_bucket


def resize_bottle_image(src_img):
    maxwidth = 768
    maxheight = 1024

    im = Image.open(src_img)
    if not(im.size[0] == maxwidth and im.size[1] == maxheight):
        ratio = max(maxwidth / im.size[0], maxheight / im.size[1])
        resolution = im.width*ratio, im.height*ratio

        # Downscale the image before cropping to fit
        im.thumbnail(resolution, Image.ANTIALIAS)

        # Crop the middle 768 x 1024
        if(im.height == maxheight):
            half_the_width = im.size[0] / 2
            new_im = im.crop(
                (half_the_width - (maxwidth/2), 0, # x, y
                 half_the_width + (maxwidth/2), maxheight) # w, h
            )
            new_im.save(src_img)
        elif(im.width == maxwidth):
            half_the_height = im.size[1] / 2
            new_im = im.crop(
                (0, half_the_height - (maxheight / 2), # x, y
                 maxwidth, half_the_height + (maxheight / 2)) # w, h
            )
            new_im.save(src_img)

    upload_image_to_hf_bucket(src_img)


def create_bottle_thumb(bottle_img):
    max_dim = 512

    im = Image.open(bottle_img)

    old_size = im.size
    new_dim = max(im.size[0], im.size[1])

    # Create new square canvas
    new_size = (new_dim, new_dim)
    new_im = Image.new("RGBA", new_size, (0,0,0,0))

    new_im.paste(im, (int((new_size[0] - old_size[0])/2), int((new_size[1] - old_size[1])/2)))

    if not(new_dim == max_dim):
        ratio = max_dim/new_dim
        resolution = new_dim*ratio, new_dim*ratio

    # Downscale the image before cropping to fit
    new_im.thumbnail(resolution, Image.ANTIALIAS)

    img_name = bottle_img.split('.')
    thumb_name = "{}_thumb.{}".format(img_name[0], img_name[1])
    new_im.save(thumb_name)
    upload_image_to_hf_bucket(thumb_name)
