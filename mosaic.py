from PIL import Image
import random


class mosaic():
    """
    Returns mosaic object.

    Parameters
    ----------
    main_picture_path : str
        Path to file to use for the mosaic.

    Attributes
    ----------
    main_picture : Image object
    """
    def __init__(self, main_picture_path):
        self.main_picture = Image.open(main_picture_path)

    def create(self, database, cropSize, picLimit, targetMissmatch=25,
               minAlpha=0.6):
        """
        Creates mosaic image from mosaic object using a database.

        Parameters
        ----------
        database : database object
        cropSize : int
            Edge length of individual tiles of mosaic
        picLimit : int
            Maximum number of occurrences of a database image in mosaic
        targetMissmatch : int (default: 25)
            Maximum difference between RGB value of pixel and mean RGB value of
            picked database image for which database image is not blended with
            pixel RGB value.
        minAlpha : float (default: 0.6)
            Minimum alpha value used to blend picked database image with pixel
            RGB.

        Returns
        ----------
        out : Image object
        """
        mosaicSize = (self.main_picture.size[0]*cropSize,
                      self.main_picture.size[1]*cropSize)
        mosaic = Image.new('RGB', mosaicSize)

        xvals = list(range(self.main_picture.size[0]))
        yvals = list(range(self.main_picture.size[1]))
        pairs = [(x, y) for x in xvals for y in yvals]
        random.shuffle(pairs)

        for pair in pairs:
            matchColor = self.main_picture.getpixel(pair)
            matchPicture = database.returnPic(matchColor, picLimit,
                                              targetMissmatch, minAlpha)
            mosaic.paste(matchPicture,
                         box=(pair[0]*cropSize, pair[1]*cropSize))
        return mosaic
