import os
import pickle

def read_pkl_files(directory):
    pkl_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pkl'):
                pkl_files.append(os.path.join(root, file))
    
    results = []
    for pkl_file in pkl_files:
        with open(pkl_file, 'rb') as f:
            data = pickle.load(f)
            results.append((pkl_file, data))
    
    return results

pysr_directory = './pysr/eqs/aging'  # 请替换为实际的pysr文件夹路径
pkl_data = read_pkl_files(pysr_directory)

for file_path, data in pkl_data:
    print(f"文件: {file_path}")
    print(f"内容: {data}")
    print("-" * 50)
