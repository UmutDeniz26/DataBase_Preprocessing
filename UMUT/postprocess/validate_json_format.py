import os
import json

def main(folder_path):
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                txt_path = os.path.join(root, file)
                with open(txt_path, "r") as f:
                    content = f.read()
                if "pass_exception" in content or "info" in file.lower():
                    continue

                error_flag = False
                try:
                    
                    json_data = json.loads(content)
                    error_flag = True if len(json_data) == 0 else False
                    
                except:
                    error_flag = True

                if error_flag:
                    print(f"\nOld Content: {content}")
                    content = f"{{\"Error\": \"JsonError\"}}"
                    write_txt(txt_path, content)
                    print(f"Fixed: {txt_path}")
                    print(f"Content: {content}")
                    


def write_txt(txt_path, content):
    with open(txt_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    main("casia-webface_FOLDERED")