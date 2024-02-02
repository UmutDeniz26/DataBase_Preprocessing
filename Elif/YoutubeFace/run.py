import sys
import os
sys.path.insert(0,"./UMUT")

import DB_Folder_Manipulator

DB_Folder_Manipulator.main(dbName='YoutubeFace', 
                           logFolderPath='./Elif/LOG/YoutubeFace', 
                           txtInfoPath='./Elif/youtubeFaceDB.txt', 
                           showFrontalFaceExamples=False, 
                           isThereTrainTest=False, 
                           inputOrAutoMod=False,
                           upperFolderName='Elif')


