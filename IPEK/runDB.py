import sys
import os
sys.path.insert(0,"./UMUT")

import DB_Folder_Manipulator

DB_Folder_Manipulator.main(dbName='lfw-deepfunneled', 
                           logFolderPath='./IPEK/lfw-deepfunneled', 
                           txtInfoPath='./IPEK/lfw-deepfunneled.txt', 
                           showFrontalFaceExamples=False, 
                           isThereTrainTest=False, 
                           inputOrAutoMod=False,
                           upperFolderName='IPEK')


