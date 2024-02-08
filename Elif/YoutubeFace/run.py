import sys
import os
sys.path.insert(0,"./UMUT")

import DB_Folder_Manipulator

DB_Folder_Manipulator.main(dbName='YoutubeFace', upperFolderName='Elif', 
         showFrontalFaceExamples=False, inputOrAutoMod=False, 
        printFeaturesFlag=False, selectFirstImageAsFrontal=False)


