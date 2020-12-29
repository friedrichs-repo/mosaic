from PIL import Image, ImageOps


def cropSquare_and_resize(im, cropSize):
    """
    Crops image im to quadratic size and resizes it to edge length cropSize.
    """
    width, height = im.size
    if(width > height):
        xMin = (width - height)/2
        yMin = 0
        xMax = width - (width - height)/2
        yMax = height
        im = im.crop((xMin, yMin, xMax, yMax))

    elif(height > width):
        xMin = 0
        yMin = (height - width)/2
        xMax = width
        yMax = height - (height-width)/2
        im = im.crop((xMin, yMin, xMax, yMax))

    return im.resize((cropSize, cropSize))


class center_picture():
    """
    Loads picture from path, crops it quadratically and resizes it.

    Parameters
    ----------
    path : str
        Path to picture that should be loaded
    cropSize : int
        Edge length to which size the quadratic picture should be resized

    Attributes
    ----------
    pic : Image object
    """
    def __init__(self, path, cropSize):
        self.path = path
        try:
            self.pic = ImageOps.exif_transpose(Image.open(self.path))
        except:
            self.pic = Image.open(self.path)
        self.pic = cropSquare_and_resize(self.pic, cropSize)

    def center_rgb(self):
        """
        Returns mean RGB value of quadratically cropped image.
        """
        centermean = self.pic.resize((1, 1), resample=0).getpixel((0, 0))
        return tuple(centermean)
