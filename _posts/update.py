import os

# 获取当前文件夹中的所有文件
files = os.listdir()

# 遍历所有文件
for file in files:
    # 检查文件名是否以 "2021-" 开头
    if file.startswith("2021-"):
        # 构造新的文件名
        new_file = "2023-" + file[5:]
        # 重命名文件
        os.rename(file, new_file)
