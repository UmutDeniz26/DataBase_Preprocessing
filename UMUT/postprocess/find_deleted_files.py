import os

def main(changed_dataset, original_dataset):
    hold_inter = 'init'
    missing_numbers = []
    for root, dirs, files in os.walk(changed_dataset):
        for file in files:
            #print(file)
            if file.endswith('.txt'):  
                #_, inter = os.path.split(root)
                extensionless_file = file.split('.')[0]
                """
                if len(file.split('\\')[-1].split('.')[0].split('_')) == 1:
                    file_path = os.path.join(root,file)
                    intra = file.split('\\')[-2]
                    inter = file.split('.')[0]
                else:
                    intra = file.split('\\')[-1].split('.')[0].split('_')[1]
                """
                inter = extensionless_file.split('_')[-1]
                
                if hold_inter != 'init':
                    if int(inter) - int(hold_inter) != 1 and int(inter) - int(hold_inter) != 0:
                        #print(f'-------------------\ninter: {inter} hold_inter: {hold_inter}')
                        if int(inter) > int(hold_inter):
                            for num in list(range(int(hold_inter)+1, int(inter))):
                                missing_numbers.append(num)
                        else:
                            for num in list(range(int(inter)+1, int(hold_inter))):
                                missing_numbers.append(num)
                hold_inter = inter
    missing_numbers = list(set(missing_numbers))
    missing_paths = []
    
    for root, dirs, files in os.walk(original_dataset):
        for file in files:
            if "Info" in file or "frontal" in root.lower() or "readme" in os.path.join(root,file).lower():
                continue
            extensionless_file = file.split('.')[0]
            inter = extensionless_file.split('_')[-1]
            if int(inter) in missing_numbers:
                missing_paths.append(os.path.join(root, file))

    print(f'missing_paths: {missing_paths}')
    print(f'len(missing_numbers): {len(missing_numbers)}')
    output_path = os.path.join("Elif","Two_Face_Handle", "deleted_files.txt")
    with open(output_path, 'w') as f:
        for item in missing_paths:
            f.write("%s\n" % item)


if __name__ == '__main__':
    main(changed_dataset = 'Elif\Two_Face_Handle\Output_copy', original_dataset = 'Elif/Two_Face_Handle/first_Output_copy')
    