import sys
import os
sys.path.insert(0,"./UMUT")

import DB_Folder_Manipulator

DB_Folder_Manipulator. main(
        data_base_name='YoutubeFace', upper_folder_name='Elif',
        align_images_flag=True, reset_images_flag=True,
        auto_feature_select=False, print_features_flag=False,
        select_first_image_as_frontal=False, show_aligned_images=False
    )