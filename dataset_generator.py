import argparse
import json
import os
import pickle

import numpy as np
from sympy import srepr
from torchdistill.common.file_util import make_parent_dirs
from torchdistill.common.yaml_util import load_yaml_file

from datasets.registry import get_eq_obj
from datasets.sampling import build_sampling_objs


def get_argparser():
    parser = argparse.ArgumentParser(description='Dataset generator')
    parser.add_argument('--config', required=True, help='config file path')
    parser.add_argument('--train', type=float, default=8.0, help='default training ratio')
    parser.add_argument('--val', type=float, default=1.0, help='default validation ratio')
    parser.add_argument('--test', type=float, default=1.0, help='default test ratio')
    parser.add_argument('--eq', help='output json file path for equations')
    return parser


def split_dataset(dataset, train_ratio, val_ratio, test_ratio):
    total = train_ratio + val_ratio + test_ratio
    train_ratio /= total
    val_ratio /= total
    num_samples = len(dataset)
    num_train_samples = int(train_ratio * num_samples)
    num_val_samples = int(val_ratio * num_samples)
    num_test_samples = num_samples - (num_train_samples + num_val_samples)
    train_dataset = dataset[:num_train_samples] if num_train_samples > 0 else None
    val_dataset = dataset[num_train_samples:num_train_samples + num_val_samples] if num_val_samples > 0 else None
    test_dataset = dataset[-num_test_samples:] if num_test_samples > 0 else None
    return train_dataset, val_dataset, test_dataset


def generate_dataset(dataset_name, dataset_config, default_train_ratio, default_val_ratio, default_test_ratio):
    print('\n====================================')
    print(f'Generating dataset `{dataset_name}` ...')
    print(dataset_config)
    dataset_kwargs = dataset_config['kwargs']
    if dataset_kwargs is None:
        dataset_kwargs = dict()

    # Instantiate equation object
    sampling_objs = \
        build_sampling_objs(dataset_kwargs.pop('sampling_objs')) if 'sampling_objs' in dataset_kwargs else None
    eq_instance = get_eq_obj(dataset_name, sampling_objs=sampling_objs, **dataset_kwargs)

    # Generate tabular dataset
    dataset = eq_instance.create_dataset(dataset_config['sample_size'])
    if dataset_config["noise_rate"] > 0:
        y = dataset[:, -1]
        sigma = np.mean(y**2)
        noise = np.random.normal(0, dataset_config["noise_rate"]*sigma, len(y))
        dataset[:, -1] += noise
    train_ratio = dataset_config.get('train_ratio', default_train_ratio)
    val_ratio = dataset_config.get('val_ratio', default_val_ratio)
    test_ratio = dataset_config.get('test_ratio', default_test_ratio)
    train_dataset, val_dataset, test_dataset = split_dataset(dataset, train_ratio, val_ratio, test_ratio)

    # Write out each split
    prefix = dataset_config.get('prefix', None)
    suffix = dataset_config.get('suffix', None)
    eq_name = eq_instance.get_eq_name(prefix=prefix, suffix=suffix)
    output_dir_path = os.path.expanduser(dataset_config['output_dir'])
    output_ext = dataset_config['output_ext']
    delimiter = dataset_config.get('output_delim', '\t' if output_ext == '.tsv' else ' ')
    for sub_dataset, split_name in zip((train_dataset, val_dataset, test_dataset), ('train', 'val', 'test')):
        if sub_dataset is None:
            continue

        print(f'Writing out {len(sub_dataset)} samples for {split_name} split')
        output_file_path = os.path.join(output_dir_path, split_name, eq_name + output_ext)
        make_parent_dirs(output_file_path)
        # Save tabular dataset
        np.savetxt(output_file_path, sub_dataset, delimiter=delimiter)

    # Save ground-truth sympy expression
    pickle_file_path = os.path.join(output_dir_path, 'true_eq', eq_name + '.pkl')
    make_parent_dirs(pickle_file_path)
    with open(pickle_file_path, 'wb') as fp:
        pickle.dump(eq_instance.sympy_eq, fp)
    return eq_name, eq_instance.sympy_eq


def main(args):
    print(args)
    config = load_yaml_file(args.config)
    default_train_ratio, default_val_ratio, default_test_ratio = args.train, args.val, args.test
    total = default_train_ratio + default_val_ratio + default_test_ratio
    default_train_ratio /= total
    default_val_ratio /= total
    default_test_ratio /= total
    if isinstance(config, dict):
        key_config_pairs = [(dataset_key, dataset_config) for dataset_key, dataset_config in config.items()]
    elif isinstance(config, list):
        key_config_pairs = [(dataset_key, dataset_config) for sub_config in config
                            for dataset_key, dataset_config in sub_config.items()]
    else:
        raise TypeError(f'config type `{type(config)}` is not expected')

    eq_dict = dict()
    for dataset_key, dataset_config in key_config_pairs:
        eq_name, sympy_eq = \
            generate_dataset(dataset_key, dataset_config, default_train_ratio, default_val_ratio, default_test_ratio)
        sympy_eq_str = repr(sympy_eq)
        sympy_eq_srepr = srepr(sympy_eq)
        eq_dict[eq_name] = {
            'dataset_class_key': dataset_key,
            'sympy_eq_str': sympy_eq_str,
            'sympy_eq_srepr': sympy_eq_srepr
        }

    eq_file_path = args.eq
    if eq_file_path is not None:
        eq_file_path = os.path.expanduser(eq_file_path)
        make_parent_dirs(eq_file_path)
        with open(eq_file_path, 'w') as fp:
            json.dump(eq_dict, fp)


if __name__ == '__main__':
    argparser = get_argparser()
    main(argparser.parse_args())
