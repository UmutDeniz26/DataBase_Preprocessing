import os


def main():
    database_path = "./src/dataset/"
    txt_path = "./src/text/dataset.txt"
    # Create a txt file for each class

    # First iteration
    first_iter = True

    with open(txt_path, 'w') as train_txt:
        for root, dirs, files in os.walk(database_path):
            for file in files:
                file_path = os.path.join(root, file)
                path_components = os.path.normpath(file_path).split(os.sep)
                path_components[-1] = path_components[-1].split('.')[0]

                if first_iter:
                    inter_index, intra_index = obtain_indexes(path_components)
                    first_iter = False

                if file.endswith('.jpg'):
                    inter = path_components[inter_index]
                    intra = path_components[intra_index]
                    write_string = f"{inter}_{inter}_{intra}\n"
                    train_txt.write(write_string)
                
def obtain_indexes(path_components):
    print(path_components)
    inter_index = int(input("Enter the index of the inter class: "))
    intra_index = int(input("Enter the index of the intra class: "))
    return inter_index, intra_index

if __name__ == '__main__':
    main()