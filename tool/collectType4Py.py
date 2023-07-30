import requests
import json
import os
import parameter

if not os.path.exists("./json"):
    os.makedirs("./json")

repo_list = os.listdir(parameter.Subject_Dir)

for i, item in enumerate(repo_list):
    print("正在对第{:4}/{:4}个仓库进行操作，仓库名称为：{}".format(i, len(repo_list), item))
    root_dir = os.path.join(parameter.Subject_Dir, item)
    for root, dirs, files in os.walk(root_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path) and file_name.endswith(".py"):
                str = file_name.replace(".py", "")
                path = root.replace(parameter.Subject_Dir, "")
                print("./json/" + path + "/" + str + '.json')
                if os.path.exists("./json/" + path + "/" + str + '.json'):
                    continue
                with open(file_path, "rb") as f:
                    r = requests.post("https://type4py.com/api/predict?tcx=0", f.read())
                if r.status_code == 200:
                    print("Success")
                else:
                    print("Fail")
                    input()
                    continue

                if not os.path.exists("./json/" + path):
                    os.makedirs("./json/" + path)
                with open("./json/" + path + "/" + str + '.json', 'w') as file:
                    file.write(json.dumps(r.json()))
