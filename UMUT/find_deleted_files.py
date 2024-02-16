import os


def main(changed_dataset, original_dataset,output_path):
    hold_inter = 'init'
    missing_numbers = []
    for root, dirs, files in os.walk(changed_dataset):
        for file in files:
            if file.endswith('.txt'):
                extensionless_file = file.split('.')[0]
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
            if "Info" in file or "frontal" in root.lower():
                continue
            extensionless_file = file.split('.')[0]
            inter = extensionless_file.split('_')[-1]
            if int(inter) in missing_numbers:
                missing_paths.append(os.path.join(root, file))

    print(f'missing_paths: {missing_paths}')
    print(f'len(missing_numbers): {len(missing_numbers)}')
    with open(output_path, 'w') as f:
        for item in missing_paths:
            f.write("%s\n" % item)


if __name__ == '__main__':
    main(changed_dataset = 'UMUT\Two_Face_Handle\HELEN_FOLDERED_copy', original_dataset = 'UMUT\HELEN_FOLDERED', output_path = 'UMUT\HELEN_deleted_files.txt')