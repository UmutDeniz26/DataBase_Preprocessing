import os
import json

def main(folder_path, fix_json=False, print_flag=False):
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt") and "_Info" not in file:
                # Get the content of the txt file
                txt_path = os.path.join(root, file)
                content = get_content(txt_path)

                error_flag = False
                try:
                    json_data = json.loads(content);json_data
                except:
                    if "Low Confidence" in content:
                        content = content.replace("\"(Low Confidence)\",", "")
                    content = content.replace("(", "[").replace(")", "]")
                    error_flag = True

                if len(content)<200 and len(content)>25:
                    print(f"\n{txt_path} - {len(content)}")
                    print(f"Content: {content}")
                    print(f"Error: {error_flag}")
                   # input("Press Enter to continue...")

                error_flag = True if len(json_data) == 0 else error_flag
                error_flag = False if "pass_exception" in content else error_flag
                if error_flag:
                    if "right_eye" not in content:
                        content = f"{{\"Error\": \"JsonError\"}}"
                    print(f"\n\nError Flag is true\n{txt_path}\n{len(content)}")
                    if fix_json:
                        write_txt(txt_path, content)
                        print(f"\nFixed: {txt_path}")
            
                if print_flag:
                    person_id = os.path.normpath(txt_path).split(os.sep)[-2]   
                    if int(person_id) % 100 == 0:    
                        print(f"\nFixed: {txt_path} - Error: {error_flag}")
                        print(f"Content: {content}")
            

def get_content(txt_path):
    with open(txt_path, "r") as f:
        content = f.read()
    return content

def write_txt(txt_path, content):
    with open(txt_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main("UMUT/casia-webface_FOLDERED", fix_json=False,print_flag=False)