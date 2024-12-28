#!/bin/bash

# 查找所有以 "logs_wo" 开头的目录
log_dirs=$(find . -type d -name "*wo_const*" | sort)

missing_summary_dirs=()
poly_counts=()

for log_dir in $log_dirs; do
    # 检查每个子目录
    subdirs=$(find "$log_dir" -mindepth 1 -maxdepth 1 -type d | sort)
    for subdir in $subdirs; do
        # 检查是否存在 summary.csv 文件
        # if [ ! -f "$subdir/summary.csv" ]; then
        if [[ $log_dir == *"wo_const"* ]]; then
            poly_num=$(echo $subdir | grep -oP 'wo_const\K\d+')
            poly_counts+=($poly_num)
            truncated_path=$(echo $subdir | sed 's/.*\.\.//')
            missing_summary_dirs+=("$truncated_path")
        fi
        # fi
    done
    # 移除这行，因为它可能导致大量输出
    # echo $missing_summary_dirs
done

# 添加调试信息
echo "总共找到 ${#missing_summary_dirs[@]} 个缺少 summary.csv 的目录"
echo "总共找到 ${#poly_counts[@]} 个 wo_const 数字"


for i in "${!missing_summary_dirs[@]}"; do
  dir="${missing_summary_dirs[$i]}"
  seed="${poly_counts[$i]}"
  log_w_poly_dir="./logs_wo_const${seed}"
  filepath="../..${dir}"
  # 处理文件路径
  filepath=$(echo "$filepath" | sed 's/1_/1_/' | sed 's/_/\//g')
  filepath=$(echo "$filepath" | sed 's/\/[^/]*$//')
  filepath=$(echo "$filepath" | sed 's/1\//1_/')
  filepath=$(echo "$filepath" | sed 's/\/csv/_csv/')
  if [ -d "$log_w_poly_dir" ]; then
    # 查找包含$missing_summary_dirs的子目录
    # 将filepath中所有的/替换为_
    filepath_underscore=$(echo "$filepath" | sed 's/\//_/g')
    # 使用修改后的filepath_underscore来查找匹配的目录
    matching_dirs=$(find "$log_w_poly_dir" -type d -name "*${filepath_underscore}*" | sort)
    
    # 如果找到匹配的目录
    if [ ! -z "$matching_dirs" ]; then
      # 获取最后一个（最新的）目录
      echo "$matching_dirs"
      latest_dir=$(echo "$matching_dirs" | sort -r | head -n 1)
      echo "找到最新的匹配目录: $latest_dir"
      # 删除除最新目录外的所有匹配目录
      for dir in $matching_dirs; do
        if [ "$dir" != "$latest_dir" ]; then
          echo "删除旧的匹配目录: $dir"
          rm -rf "$dir"
        fi
      done
    else
      echo "在 $log_w_poly_dir 中未找到匹配 ${missing_summary_dirs[$i]} 的目录"
    fi
  else
    echo "目录 $log_w_poly_dir 不存在"
  fi
done
