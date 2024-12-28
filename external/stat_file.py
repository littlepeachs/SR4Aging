import os

dso_path = './dso'  # 请替换为实际的dso文件夹路径

for dir in os.listdir(dso_path):
    if dir.startswith('logs_w'):
        dir_path = os.path.join(dso_path, dir)
        if os.path.isdir(dir_path):
            sub_dir_count = len([name for name in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, name))])
            print(f"{dir} 包含 {sub_dir_count} 个子文件夹")
