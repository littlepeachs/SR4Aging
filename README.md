# Symbolic Regression in Advancing the Discovery of Aging Mechanisms of Polymer Materials
This code repository is related to the research on material aging, especially focusing on using symbolic regression algorithms to explore the correspondence between the microscopic characteristics and macroscopic properties of polymeric materials (especially rubber) during the aging process. Polymeric materials play a crucial role in modern life and manufacturing, but the aging problem poses serious challenges to their stability and service life. The symbolic regression algorithm has great potential in exploring the intrinsic quantitative relationships in the experimental data of material aging due to its strong interpretability. This repository aims to provide a comprehensive evaluation framework to screen symbolic regression algorithms suitable for aging experimental data and conduct further validation and knowledge discovery based on it. 

![Framework](./assets/framework.jpg)

## Setup 

You can use conda or local Python environments.
Use `requirements.txt` if you use either conda or local Python environments.
e.g., 
```shell
# Activate your conda environment if you use conda, and run the following commands
pip install pip --upgrade
pip install -r requirements.txt
```

## Prepare Data
This section will show how to prepare the datasets for the experiments. We want to prepare the datasets for the experiments. For Dummy condtion, you should run `dummy_column_mixer.py`. To get right format for DSO/uDSR, you should run `run_convertor.sh`.
```shell
# Activate your conda environment if you use conda, and run the following commands
python dataset_generator.py --config configs/datasets/feynman/1_base.yaml
python dummy_column_mixer.py --input ./resource/datasets/srsd/1_base/ --output ./resource/datasets/srsd/1_dummy
bash ./scripts/run_convertor.sh
```
Also, you can follow the configs in `configs/datasets/feynman` to prepare other datasets for the experiments.(like 1_domain)
In the repository, we provide the processed datasets for the experiments. **All dependent variables (target variables) are placed in the last column of the datasets.**

## E2E SR4Real Experiment
This section will show how to reproduce the end-to-end (E2E) SR4Real experiments. You can follow the following steps to reproduce the experiments.
```shell
# Activate your conda environment if you use conda, and run the following commands
conda env create -f e2e.yml
conda activate e2e
pip install torch==2.1.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html

git clone https://github.com/facebookresearch/symbolicregression org
mv org/* ./
rm org -rf

cd ./external/e2e/
mkdir resource/ckpt -p
wget https://dl.fbaipublicfiles.com/symbolicregression/model1.pt
mv model1.pt resource/ckpt/model.pt

bash run.sh
```
The log files are stored in `./external/e2e/log_e2e/`.
The results are stored in `./external/e2e/e2e-sr_w_transformer-results/`.

## DSO/uDSR SR4Real Experiment
This section will show how to reproduce the DSO/uDSR SR4Real experiments. You can follow the following steps to reproduce the experiments.
```shell
# Activate your conda environment if you use conda, and run the following commands
conda env create -f dso.yml
conda activate dso

git clone https://github.com/dso-org/deep-symbolic-optimization.git
cd deep-symbolic-optimization
pip install -e ./dso

cd ./external/dso/
bash run_dso.sh
bash run_udsr.sh
```
The log files are stored in `./external/dso/logs/`.
The results are stored in `./external/dso/logs_w_poly{i}/` (uDSR) or `./external/dso/logs_w(o)_const{i}/` (DSO).

You can use `run_eq_converter.sh` to extract the estimated equations from the results directories. And return to the root directory to select the best model per dataset for DSO and uDSR.
```shell
bash run_eq_converter.sh
cd ../../
bash ./scripts/model_select.sh
```
The best equations are stored in `./results/dso_models/`.

And evaluate the performance of the best model per dataset for DSO and uDSR.
```shell
bash ./scripts/run_R2.sh
bash ./scripts/run_NED.sh
```

## DSO/uDSR Polymer Aging Data Experiment
This section will show how to reproduce the DSO/uDSR experiments on polymer aging data. The original data contains material aging conditions including:
- Temperature: 50°C, 60°C, 70°C 
- Strain: 5%, 10%, 15%
- Aging time: 7-91 days

The raw and processed datasets are provided under the `resource` directory.

You can follow these steps to reproduce the experiments:
```shell
cd ./external/dso_aging/
bash run_dso.sh
bash run_udsr.sh
```
The follow the same steps as the DSO/uDSR SR4Real Experiment to select the best model and evaluate the performance.

## Reproduce the Results
You can directly run the python notebooks `data_analysis_Fe.ipynb` and `data_analysis_hard.ipynb` to reproduce the results. The equations from DSO/uDSR have been pre-trained and saved. The error scatter plots will be saved in the `final_figs` directory.

## Tips
All experiments can be reproduced in RTX 3090.

## Acknowledgments
This repository is built based on the [Deep Symbolic Optimization](https://github.com/dso-org/deep-symbolic-optimization) and [srsd-benchmark](https://github.com/omron-sinicx/srsd-benchmark). We thank the authors for their contributions.