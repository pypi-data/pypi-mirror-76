# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fractalai',
 'fractalai.classifier',
 'fractalai.datasets',
 'fractalai.engine',
 'fractalai.segmenter',
 'fractalai.utils']

package_data = \
{'': ['*']}

install_requires = \
['EasyDict>=1.9,<2.0',
 'albumentations>=0.4.1,<0.5.0',
 'click>=7.0,<8.0',
 'efficientnet_pytorch>=0.6.3,<0.7.0',
 'hyperdash>=0.15.3,<0.16.0',
 'loguru>=0.3.2,<0.4.0',
 'opencv-python>=4.1,<5.0',
 'pandas>=0.25.2,<0.26.0',
 'pretrainedmodels>=0.7.4,<0.8.0',
 'pycocotools>=2.0,<3.0',
 'pytorch-lightning>=0.7.1,<0.8.0',
 'scikit-learn>=0.21.3,<0.22.0',
 'segmentation_models_pytorch>=0.1.0,<0.2.0',
 'torch==1.4.0',
 'torchvision>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['avail_encoders = '
                     'fractalai.classifier.model:available_encoders',
                     'check_csv = fractalai.sanity:check_csv',
                     'check_data_loader = '
                     'fractalai.datasets.dataloader:make_data_loader',
                     'check_dataset = fractalai.datasets.dataset:run_dataset',
                     'check_metrics = fractalai.utils.metrics:check_metrics',
                     'check_transforms = '
                     'fractalai.datasets.agu:understand_transforms',
                     'class_imbalance_plot = '
                     'fractalai.datasets.dataloader:class_imbalance_plot',
                     'data_stat = fractalai.visual:get_data_statistic',
                     'extract_products_one_label = '
                     'fractalai.labelme2folder:make_extract_products_one_label',
                     'get_mean_std = fractalai.datasets.dataset:get_mean_std',
                     'infer_folder = fractalai.engine.infer:infer_folder',
                     'infer_img = fractalai.engine.infer:infer_img_click',
                     'infer_val_f1score = '
                     'fractalai.engine.infer:infer_val_f1score',
                     'infer_video = fractalai.engine.infer:infer_video_click',
                     'json_to_csv = fractalai.csv_utils:json_to_csv',
                     'labelme_counter = '
                     'fractalai.labelme2folder:make_label_counter',
                     'make_csv_given_folders = '
                     'fractalai.csv_utils:make_csv_given_folders',
                     'make_folders_from_csv = '
                     'fractalai.engine.infer:make_folders_from_csv',
                     'make_model = fractalai.engine.utils:make_model',
                     'name_classes = fractalai.csv_utils:get_classes',
                     'seg_model_params = '
                     'fractalai.engine.utils:seg_model_params',
                     'train = fractalai.engine.trainer:main',
                     'vis_random_example = '
                     'fractalai.datasets.dataset:visualize_random_example']}

setup_kwargs = {
    'name': 'fractalai',
    'version': '0.1.0',
    'description': 'Integrated image classification and semantic segmentation package',
    'long_description': None,
    'author': 'PrakashJay',
    'author_email': 'vanapalli.prakash@fractal.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.7.0',
}


setup(**setup_kwargs)
