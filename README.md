# Database Preprocessing

This script is used for preprocessing a database of images. It performs various operations such as selecting a frontal image, creating output folders, copying files, and detecting frontal faces.

## Usage

To use this script, you need to provide the following parameters:

- `dbName`: The name of the database.
- `upperFolderName`: The name of the upper folder.
- `inputOrAutoMod`: A boolean value indicating whether the script is in input or auto mode.
- `printFeaturesFlag`: A boolean value indicating whether to print features.
- `selectFirstImageAsFrontal`: A boolean value indicating whether to select the first image as the frontal image.
- `showAlignedImages`: A boolean value indicating whether to show aligned images.
- `alignImagesFlag`: A boolean value indicating whether to align images.
- `resetImagesFlag`: A boolean value indicating whether to reset images.

## File Structure

The script expects the following file structure:

FOLDER
├── dbName.txt
└── dbName
    ├── intra
    │   ├── inter.jpg
    │   ├── inter.jpg
    │   └── ...
    └── intra
        ├── inter.jpg
        ├── inter.jpg
        └── ...

```
dbName.txt should contain a list of filenames, each representing an image in the database. These filenames should follow a specific format:
"personID_intra_inter"
```

Breaking it down:

- `personID`: Represents the unique identifier for the subject/person in the image.
- `intra`: Represents the expression or pose of the subject in the image.
- `inter`: Represents the unique identifier for the image itself.

Each component of the filename should be separated by underscores (_) as shown in the example format "personID_intra_inter".

For example:
- A filename "00000_0_000000" represents:
  - `personID`: "00000"
  - `intra`: "0"
  - `inter`: "000000"

Ensure that the filenames in `dbName.txt` are synchronized with the sequence of images in the corresponding `dbName` folder.