# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_adaptive_computation_time', 'pytorch_adaptive_computation_time.tasks']

package_data = \
{'': ['*']}

install_requires = \
['pytorch-lightning==0.8.5', 'torch>=1.5.0,<2.0.0']

extras_require = \
{'docs': ['sphinx>=3.2.0,<4.0.0', 'sphinx-argparse>=0.2.5,<0.3.0']}

entry_points = \
{'console_scripts': ['train = pytorch_adaptive_computation_time.training:main']}

setup_kwargs = {
    'name': 'pytorch-adaptive-computation-time',
    'version': '0.1.2',
    'description': 'Implements adaptive computation time RNNs in PyTorch, with the same interface as builtin RNNs.',
    'long_description': '# pytorch-adaptive-computation-time\n\nThis library implements PyTorch modules for recurrent neural networks that can learn to execute variable-time algorithms,\nas presented in [Adaptive Computation Time for Recurrent Neural Networks (Graves 2016)](https://arxiv.org/abs/1603.08983/).\nThese models can learn patterns requiring varying amounts of computation for a fixed-size input,\nwhich is difficult or impossible for traditional neural networks.\nThe library aims to be clean, idiomatic, and extensible, offering a similar interface to PyTorch’s builtin recurrent modules.\n\nThe main features are:\n - A nearly drop-in replacement for torch.nn.RNN- and torch.nn.RNNCell-style RNNs, but with the power of variable computation time.\n - A wrapper which adds adaptive computation time to any RNNCell.\n - Data generators, configs, and training scripts to reproduce experiments from the paper.\n\n## Example\nVanilla PyTorch GRU:\n\n```\nrnn = torch.nn.GRU(64, 128, num_layers=2)\noutput, hidden = rnn(inputs, initial_hidden)\n```\n\nGRU with adaptive computation time:\n\n```\nrnn = models.AdaptiveGRU(64, 128, num_layers=2, time_penalty=1e-3)\noutput, hidden, ponder_cost = rnn(inputs, initial_hidden)\n```\n\n## Documentation\nDocumentation is [hosted on Read the Docs](https://github.com/iamishalkin/cyrtd).\n\n## BibTeX\n\nYou don’t need to cite this code, but if it helps you in your research and you’d like to:\n\n```\n@misc{swope2020ACT,\n  title   = "pytorch-adaptive-computation-time",\n  author  = "Swope, Aidan",\n  journal = "GitHub",\n  year    = "2020",\n  url     = "https://github.com/maxwells-daemons/pytorch-adaptive-computation-time"\n}\n```\n\nIf you use the experiment code, please also consider [citing PyTorch Lightning](https://github.com/PyTorchLightning/pytorch-lightning#bibtex/).\n',
    'author': 'maxwells-daemons',
    'author_email': 'aidanswope@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxwells-daemons/pytorch-adaptive-computation-time',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.10,<4.0.0',
}


setup(**setup_kwargs)
