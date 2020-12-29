import sys
from database import database
from mosaic import mosaic
from additional_tools import returnFilepaths


sys.path.append('PATH_TO_MOSAIC_FILES')
cropSize = 160
imgs = returnFilepaths('PATH_OF_IMAGE_FOLDER')
db = database(imgs, cropSize)
mosaicImg = mosaic('PATH_TO_MOSAIC_PICTURE').create(db, cropSize, 10,
                                                    targetMissmatch=25,
                                                    minAlpha=0.6)
