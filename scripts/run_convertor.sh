for srsd_category in 1_base; do
  for split_name in train val test; do
    python dataset_converter.py --src ./resource/datasets/srsd/${srsd_category}/${split_name}/ \
      --dst ./resource/datasets/srsd/${srsd_category}_csv/${split_name}/ --dst_ext .csv
  done
  cp ./resource/datasets/srsd/${srsd_category}/true_eq/ ./resource/datasets/srsd/${srsd_category}_csv/true_eq/ -r
done