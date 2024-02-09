import sys
import os
sys.path.insert(0,"./UMUT")

import DB_Folder_Manipulator

DB_Folder_Manipulator.main(dbName='LFW', upperFolderName='IPEK', 
        inputOrAutoMod=False, printFeaturesFlag=True,
          selectFirstImageAsFrontal=False, showAlignedImages=False, 
          alignImagesFlag=True, resetImagesFlag=False)
