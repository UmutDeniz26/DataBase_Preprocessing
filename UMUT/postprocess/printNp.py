import numpy as np

def main(npy_folder_path):
    data = np.load(npy_folder_path, allow_pickle=True)
    data2 = np.load("esogu_sets_meta_10_people.npy", allow_pickle=True)
    print(data)
    print(data.shape)
    print(data2)
    print(data2.shape)
    data_concat = np.concatenate((data, data2))
    print(data_concat)
    print(data_concat.shape)

if __name__ == '__main__':
    main("AFW/AFW_Info.npy")
