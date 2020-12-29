from center_picture import center_picture
from joblib import Parallel, delayed
import multiprocessing
from PIL import Image


num_cores = multiprocessing.cpu_count()


def add_to_dict(img, cropSize):
    pic = center_picture(img, cropSize)
    return {pic.center_rgb(): pic}


class database:
    """
    Creates database containing tile images with mean colors
    from list of filepaths.

    Parameters
    ----------
    imageList : list
        List of filepaths (str) for database images.
    cropSize : int
        Edge length of database images

    Attributes
    ----------
    dict : dict
        Dictionnary with mean RGB values of database images as keys and
        cropped quadratical images as values
    couterDict : dict
        Dictionnary with mean RGB values of database images as keys and
        number of times an image was returned by returnPic method as
        values. Can be reset by resetPicCounter method.
    imageList : list
        List of paths to images that were used to create the database
    cropSize : int
        Edge length of database images
    """
    def __init__(self, imageList, cropSize):
        self.cropSize = cropSize
        self.imageList = imageList
        self.dict = dict()
        self.counterDict = dict()

        def add_to_dict_wrapper(img):
            try:
                return add_to_dict(img, self.cropSize)
            except:
                print('error occured')
                return {}
        results = Parallel(n_jobs=num_cores)(delayed(add_to_dict_wrapper)(img)
                                             for img in imageList)
        for r in results:
            self.dict.update(r)

        for key in self.dict.keys():
            self.counterDict[key] = 0

    def returnPic(self, rgb, picLimit, targetMissmatch, minAlpha):
        """
        Returns the database image that is most similar to the desired RGB
        value after blending this image with desired RGB value.

        Parameters
        ----------
        rgb : tuple
            RGB tuple specifying desired color of database image
        picLimit : int
            Defines how often an image can be returned by returnPic method.
        targetMissmatch : int
            Maximum difference between desired RGB value and mean RGB value of
            picked database image for which database image is not blended with
            pixel RGB value.
        minAlpha : float
            Minimum alpha value used to blend picked database image with
            desired RGB.

        Returns
        ----------
        out : Image object
        """
        matchRGB = self.match_rgb(rgb, picLimit)
        matchPic = self.dict[matchRGB[0]].pic
        bgImage = Image.new('RGB', (self.cropSize, self.cropSize), color=rgb)
        matchDist = matchRGB[1]
        if matchDist == 0:
            matchDist = 1e-6
        alpha = max(1-targetMissmatch/matchDist, minAlpha)
        picOut = Image.blend(matchPic, bgImage, alpha=alpha)
        return picOut

    def match_rgb(self, rgb, picLimit):
        """
        Identifies database image that fits best desired RGB value and that was
        returned less often than specified by picLimit. Used by returnPic
        method.

        Parameters
        ----------
        rgb : tuple
            RGB tuple specifying desired color of database image
        picLimit : int
            Defines how often an image can be returned by returnPic method.

        Returns
        ----------
        out : tuple
            Containing the mean RGB value of best-fitting database image and
            the maximum of the differences between the desired RGB values and
            those of the best-fitting database image.
        """
        r, g, b = rgb
        minKey = rgb
        minDist = 100000.0
        for key in self.dict:
            rT, gT, bT = key
            dist = max(abs(r - rT), abs(g - gT), abs(b - bT))
#            dist = (r - rT)**2 + (g - gT)**2 + (b - bT)**2
#            dist = abs((r - rT)*(g - gT)*(b - bT))
            if(dist < minDist) and self.counterDict[key] < picLimit:
                minDist = dist
                minKey = key

        self.counterDict[minKey] += 1
        return (minKey, minDist)

    def resetPicCounter(self):
        """
        Resets values of database attribute counterDict.
        """
        for key in self.dict.keys():
            self.counterDict[key] = 0
