import sys
import os
sys.path.insert(0,"./UMUT")

import DB_Folder_Manipulator

DB_Folder_Manipulator.main(dbName='YoutubeFace', upperFolderName='Elif', 
        inputOrAutoMod=False, printFeaturesFlag=True,
          selectFirstImageAsFrontal=False, showAlignedImages=False, 
          alignImagesFlag=True, resetImagesFlag=False) #if resetImagesFlag is True, then the images will be recreated 

