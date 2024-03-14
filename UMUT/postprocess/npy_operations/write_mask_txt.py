import os
import numpy as np

def main(npy_path,init_inter,init_intra):
    data = np.load(npy_path)

    txt_destination = "UMUT/src/npy/"+npy_path.split("/")[-1]+"_mask.txt"
    masks = []
    for element in data:
        masks.append(element[3])

    masks = list(set(masks))
    masks.sort()

    with open(txt_destination, "w") as file:
        for index,mask in enumerate(masks):
            if index-1 != -1:
                prev_mask = masks[index-1]
                prev_inter = prev_mask.split("/")[1]
                prev_intra = prev_mask.split("/")[2]
            else:
                prev_inter = 'init'
                prev_intra = 'init'

            inter = mask[:].split("/")[1]
            intra = mask[:].split("/")[2]

            if prev_inter != inter and prev_intra != 'init':
                init_inter += 1
                if "LFW" in txt_destination:
                    init_intra+=1
                    file.write(f"{mask},{init_inter},{init_intra}\n")
                    continue
                """
                if prev_intra == intra:
                    print("mask:",mask," Prev: ",prev_mask)
                    print("Inter: ",inter," Intra: ",intra)
                    print("Prev Inter: ",prev_inter," Prev Intra: ",prev_intra)
                    exit()
                """

            if prev_intra != intra and prev_intra != 'init':
                init_intra += 1
                """
                if prev_intra == intra:
                    print("mask:",mask," Prev: ",prev_mask)
                    print("Inter: ",inter," Intra: ",intra)
                    print("Prev Inter: ",prev_inter," Prev Intra: ",prev_intra)
                    exit()
                """
                #print("Counter: ",index," Mask: ",mask," Inter: ",init_inter," Intra: ",init_intra)

            file.write(f"{mask},{init_inter},{init_intra}\n")
    return init_inter+1,init_intra+1

if __name__ == "__main__":
    init_inter=622
    init_intra=3201

    init_inter,init_intra = main("UMUT/src/npy/AFW_Info.npy",init_inter,init_intra)
    init_inter,init_intra = main("UMUT/src/npy/HELEN_Info.npy",init_inter,init_intra)
    init_inter,init_intra = main("UMUT/src/npy/CASIA-FaceV5_BMP_FOLDERED_Info.npy",init_inter,init_intra)
    init_inter,init_intra = main("UMUT/src/npy/LFPW_Info.npy",init_inter,init_intra)
    init_inter,init_intra = main("UMUT/src/npy/LFW_Info.npy",init_inter,init_intra)
    init_inter,init_intra = main("UMUT/src/npy/YoutubeVideos_Info.npy",init_inter,init_intra)

    print("Final inter: ",init_inter," Final intra: ",init_intra)
