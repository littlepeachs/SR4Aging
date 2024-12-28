for i in {1..10}; do
    python equation_converter.py --summary ./logs_w_poly${i}/ --out ./extract_formulas/est_eq${i}/
done
