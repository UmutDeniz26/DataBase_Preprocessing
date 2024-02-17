import os

def printList(lst):
    for i in lst:
        print(i.replace('\n','').replace('\t',''))
def validate_database_folder_txt(database_folder, txt_file):
    print("Database folder: ", database_folder)
    print("Txt file: ", txt_file)

    persons = sorted(os.scandir(database_folder), key=lambda entry: entry.name)

    txt_informations = []
    with open(txt_file, 'r') as file:
        txt_informations = file.readlines()


    all_images = []
    for person in persons:
        if person.is_dir():
            intras = sorted(os.scandir(person), key=lambda entry: entry.name)
            for intra in intras:
                if intra.is_dir():
                    inters = sorted(os.scandir(intra), key=lambda entry: entry.name)
                    for inter in inters:
                        if inter.is_file():
                            all_images.append(inter.path)
                        else:
                            print("Inter is not a file")
                            exit()
                else:
                    print("Intra is not a directory")
                    exit()
        else:
            print("Person is not a directory")
            exit()


    persons = sorted(os.scandir(database_folder), key=lambda entry: entry.name)
    counter_intra = 0
    counter_inter = 0

    # Check if the txt file contains the same number of intra as the database folder
    for index_p,person in enumerate(sorted(persons, key=lambda entry: entry.name)):
        if person.is_dir():
            intras = os.scandir(person)
            for index_a,intra in enumerate(sorted(intras, key=lambda entry: entry.name)):
                if intra.is_dir():
                    inters = os.scandir(intra)
                    for index_e,inter in enumerate(sorted(inters, key=lambda entry: entry.name)):
                        if inter.is_file():
                            try:
                                txt_split = txt_informations[counter_inter].split('_')
                                txt_dict = {'person': int(txt_split[0]), 'intra': int(txt_split[1]), 'inter': int(txt_split[2])}
                            except:
                                print("IndexError in txt file\n", "txt: ",txt_dict," path:",inter.path)
                                print("Person: ", index_p, "Intra: ", counter_intra, "Inter: ", counter_inter)
                                exit()

                            if txt_dict['person'] != index_p or txt_dict['intra'] != counter_intra or txt_dict['inter'] != counter_inter:
                                print("Error in txt file\n", "txt: ",txt_dict," path:",inter.path)
                                print("Person: ", index_p, "Intra: ", counter_intra, "Inter: ", counter_inter)

                                files_to_investigate = all_images[counter_inter-5:counter_inter+5]
                                print("files: ")
                                printList(files_to_investigate)
                                print("txt: ")
                                printList(txt_informations[counter_inter-5:counter_inter+5])

                                exit()

                            counter_inter += 1
                        else:
                            print("Inter is not a file")
                            exit()
                    counter_intra += 1
                else:
                    print("Intra is not a directory")
                    exit()
        else:
            print("Person is not a directory")
            exit()
    print("Validation is successful")


folder_path='.\IPEK\LFW'
txt_path='.\IPEK\LFW.txt'
if __name__ == "__main__":
    validate_database_folder_txt('./Ali/YoutubeFace', './Ali/YoutubeFace.txt')
