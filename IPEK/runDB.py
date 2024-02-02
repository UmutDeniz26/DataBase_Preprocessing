import sys
import os
sys.path.insert(0,"./UMUT")

import DB_Folder_Manipulator

DB_Folder_Manipulator.main(dbName='LFW', 
                           logFolderPath='./IPEK/LOG/LFW', 
                           txtInfoPath='./IPEK/LFWDB.txt', 
                           showFrontalFaceExamples=False, 
                           isThereTrainTest=False, 
                           inputOrAutoMod=False,
                           upperFolderName='IPEK')


