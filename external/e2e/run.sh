CKPT_FILE=./resource/ckpt/model.pt
mkdir -p ./logs_e2e

rest_files=(
../../resource/datasets/srsd/1_base/train/feynman-i.12.1.txt \
# ../../resource/datasets/srsd/1_aging/train/Hardness_fold_1.txt \
)
group_names=(aging)

for i in {0..0}; do
    filepath=${rest_files[$i]}
    group_name=${group_names[$i]}
    OUT_DIR=./e2e-sr_w_transformer-results/1_${group_name}
    mkdir ${OUT_DIR} -p
    PARENT_DIR=$(dirname $(dirname $filepath))
    FILE_NAME=$(basename $filepath)
    TRAIN_FILE=${PARENT_DIR}/train/${FILE_NAME}
    TEST_FILE=${PARENT_DIR}/test/${FILE_NAME}
    python runner.py --train ${TRAIN_FILE} --test ${TEST_FILE} \
        --ckpt ${CKPT_FILE} --out ${OUT_DIR}/${FILE_NAME} \
        > ./logs_e2e/1_${group_name}_${FILE_NAME}.log 2>&1
done
