import os
import re

#This function is for see the features
def printFeatures( output_dict ):
    print(f"\n\nout_file_name: {output_dict['out_file_name']}\n"
          f"file_name_withoutExtension: {output_dict['file_name_withoutExtension']}\n"
          f"extension: {output_dict['extension']}\n"
          f"learnType: {output_dict['learnType']}\n"
          f"file_id: {output_dict['file_id']}\n"
          f"inner_id_right_side: {output_dict['inner_id_right_side']}\n"
          f"inner_id_left_side: {output_dict['inner_id_left_side']}"
    )

#Dynamic feature extraction
#This function will run only once, when the number of slices changed
def decideWhichElementsWhichFeatures( file_name_split,out_file_name ):
    file_id_index, inner_id_right_side_index, inner_id_left_side_index, learnType_index = 0, 0, 0, 0
    for element in file_name_split:
        os.system('cls')
        print("File Name: " + out_file_name)
        print(file_name_split)
        inputTemp = input("\nWhat is the feature of '" + element + "' ? \n"+  
                        " n -> next \n"
                        " f -> file_id \n" +
                        " ir -> inner_id_right_side \n" +
                        " il -> inner_id_left_side \n" +
                        " l -> learnType : " )
        if inputTemp == "f":
            file_id_index = file_name_split.index(element)
        elif inputTemp == "ir":
            inner_id_right_side_index = file_name_split.index(element)
        elif inputTemp == "il":
            inner_id_left_side_index = file_name_split.index(element)
        elif inputTemp == "l":
            learnType_index = file_name_split.index(element)
        elif inputTemp == "n":
            continue
        else:
            print("Wrong Input!")
            exit()

    print("\nElement indexes: \n" + "file_id_index: " + str(file_id_index) + "\n" +
            "inner_id_right_side_index: " + str(inner_id_right_side_index) + "\n" +
            "inner_id_left_side_index: " + str(inner_id_left_side_index) + "\n" +
            "learnType_index: " + str(learnType_index) + "\n")
    return file_id_index, inner_id_right_side_index, inner_id_left_side_index, learnType_index

#You should change this function according to your dataset,if you want to use auto mod !!!!!!!
#Adjusted for IBUG Dataset
def autoDetermineAccordingToFeatureCount( file_name_split, indexDict, isThereTrainTest = False):
    file_id_index = indexDict["file_id_index"];inner_id_right_side_index = indexDict["inner_id_right_side_index"]
    inner_id_left_side_index = indexDict["inner_id_left_side_index"];learnType_index = indexDict["learnType_index"]

    integerFeatureSliceCount = 0
    #calculate feature count but only numbers
    for element in file_name_split:
        if re.match("^\d+$", element):
            integerFeatureSliceCount += 1
    print("Integer Feature Slice Count: " + str(integerFeatureSliceCount))

    #Change these indexes according to your dataset
    if isThereTrainTest:
        if integerFeatureSliceCount == 2:
            file_id_index = 3
            inner_id_right_side_index = 4
            inner_id_left_side_index = 0
            learnType_index = 2
        else:
            print("Wrong Feature Count!")
            exit()
    else:
        if integerFeatureSliceCount == 3:
            file_id_index = 2
            inner_id_right_side_index = 4
            inner_id_left_side_index = 3
            learnType_index = False
        elif integerFeatureSliceCount == 2:
            file_id_index = 2
            inner_id_right_side_index = 3
            inner_id_left_side_index = False
            learnType_index = False
        else:
            print("Wrong Feature Count!")
            exit()
    
    return file_id_index, inner_id_right_side_index, inner_id_left_side_index, learnType_index

#This function will extract features from file name
def extractFeaturesFromFileName(out_file_name, indexDict, inputOrAutoMod=False, makeDeceisonFlag=True):
    file_id_index = indexDict["file_id_index"];inner_id_right_side_index = indexDict["inner_id_right_side_index"]
    inner_id_left_side_index = indexDict["inner_id_left_side_index"];learnType_index = indexDict["learnType_index"]

    #Don't change this part
    file_name_split = out_file_name.split('_')
    file_name_withoutExtension = out_file_name.split('.')[0]    
    extension = out_file_name.split('.')[-1] # jpg or mat
    
    file_name_split = file_name_split[:-1] + file_name_split[-1].split('.') 
    numberOfSlices = len(file_name_split)

    #Number of slices changed, we should extract which feature is which
    if makeDeceisonFlag == True:
        if inputOrAutoMod:
            file_id_index, inner_id_right_side_index, inner_id_left_side_index, learnType_index = autoDetermineAccordingToFeatureCount(file_name_split,indexDict)
        else:
            file_id_index, inner_id_right_side_index, inner_id_left_side_index, learnType_index = decideWhichElementsWhichFeatures(file_name_split, out_file_name)
        makeDeceisonFlag = False
        
    indexDict = {
        "file_id_index": file_id_index,
        "inner_id_right_side_index": inner_id_right_side_index,
        "inner_id_left_side_index": inner_id_left_side_index,
        "learnType_index": learnType_index
    }   

    file_id = file_name_split[file_id_index];inner_id_right_side = file_name_split[inner_id_right_side_index]
    inner_id_left_side = file_name_split[inner_id_left_side_index]
    
    # train or test only for LFPW Dataset
    learnType = file_name_split[learnType_index]
    if learnType != 'train' and learnType != 'test':
        learnType = False

    #Only for imgTxtDBs
    output_dict = {
            "out_file_name": out_file_name,           "file_name_withoutExtension": file_name_withoutExtension, 
            "extension": extension,                   "inner_id_right_side": inner_id_right_side, 
            "learnType": learnType,                   "file_id": file_id, 
            "inner_id_left_side": inner_id_left_side, "numberOfSlices": numberOfSlices
        }
    
    #Uncomment this to see the features
    printFeatures(output_dict)
    return output_dict, indexDict, makeDeceisonFlag