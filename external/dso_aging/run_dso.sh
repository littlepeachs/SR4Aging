
mkdir -p ./logs
rest_files=(
# ../../resource/datasets/srsd/1_base_csv/train/feynman-i.12.1.txt.csv \
../../resource/datasets/srsd/1_aging_csv/train/Hardness_fold_1.txt.csv \
)
for filepath in ${rest_files[@]}; do
  filename=$(basename "$filepath")
  for i in {1..5}; do
    python -m dso.run ./configs/dsr/config_wo_const${i}.json --b ${filepath} --seed ${i} > ./logs/1_aging_config_wo_const${i}_${filename}.log 2>&1 &
    python -m dso.run ./configs/dsr/config_w_const${i}.json --b ${filepath} --seed ${i} > ./logs/1_aging_config_w_const${i}_${filename}.log 2>&1
    echo "start aging_config_wo_const${i} and aging_config_w_const${i}"
  done
done
# 等待所有进程完成
wait