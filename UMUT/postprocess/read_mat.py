
import scipy.io as sio
def main(mat_path):
    mat = sio.loadmat(mat_path)
    print(mat)


if __name__ == "__main__":
    main("UMUT/300W_LP_First/landmarks/AFW/AFW_134212_1_0_pts.mat")
