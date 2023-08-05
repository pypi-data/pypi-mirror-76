# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sorting_gym', 'sorting_gym.agents', 'sorting_gym.envs']

package_data = \
{'': ['*']}

install_requires = \
['gym>=0.17.2,<0.18.0', 'numpy>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'sorting-gym',
    'version': '0.0.7',
    'description': 'OpenAI Gym Environments for Sorting',
    'long_description': "# Sorting Gym\n\nOpenAI Gym Environments for Sorting based on the 2020 paper\n[_Strong Generalization and Efficiency in Neural Programs_](https://arxiv.org/abs/2007.03629) by \n_Yujia Li, Felix Gimeno, Pushmeet Kohli, Oriol Vinyals_.\n\nThis repository includes implementations of the neural interface environments for sorting.\n\nInstall from pypi (recommended) with:\n```\npip install sorting-gym\n```\n\nImporting the Python package `sorting_gym` will expose the following Gym environments:\n\n- `SortTapeAlgorithmicEnv-v0` - Tape based environment based on [Gym's algorithmic environment](https://github.com/openai/gym/blob/master/gym/envs/algorithmic/algorithmic_env.py#L242))\n- `BasicNeuralSortInterfaceEnv-v0` - an interface where agents can implement simple algorithms such as bubble sort and insertion sort.\n- `FunctionalNeuralSortInterfaceEnv-v0` - extends the `BasicNeuralSortInterfaceEnv-v0` interface to include instructions for entering and exiting functions.\n\nTo define the parametric action space we introduce the `DiscreteParametric(Space)` type,\nallowing environments to describe disjoint output spaces, conditioned on a discrete space.\nFor example:\n\n```python\nfrom gym.spaces import Discrete\nfrom sorting_gym import DiscreteParametric\naction_space = DiscreteParametric(2, ([Discrete(2), Discrete(3)]))\n```\n\nIn the `sorting_gym.agents.scripted` module we implement the scripted agents from the paper.\n\nRL Agents may want to consider supporting parametric/auto-regressive actions:\n- https://docs.ray.io/en/master/rllib-models.html#autoregressive-action-distributions\n- https://arxiv.org/abs/1502.03509\n\n\n### Goals:\n\n- [x] Implement bubblesort/insertion sort environment.\n- [x] Implement bubblesort/insertion sort agents as tests.\n- [x] Implement function environment.\n- [x] Implement quick sort scripted agent to test function environment.\n- [ ] Wrap the environment to expose a vanilla action space (probably MultiDiscrete)\n- [ ] Include an example solution to train an agent via RL\n- [ ] Environment rendering (at least text based, optional dependency for rendering graphically with e.g. pygame)\n- [ ] Remove the tape environment from open ai gym (used to generate longer data as agent levels up)\n- [x] Housekeeping - license and ci\n\n### Ideas to take it further:\n\n- Accelerate environment with cython (if required)\n- Open PR to `gym` for a discrete parametric space\n- Abstract out a Neural Controller Mixin/Environment Wrapper?\n- Consider a different/enhanced instruction set. \n  Instead of always comparing every pointer and data element in the view (and neighbours), \n  have explicit comparison instructions. Could extend to other math instructions, including\n  accounting for variable cost of the instructions.\n- Instead of passing previous arguments, consider passing in the number of instructions\n  executed in the current scope as a cheap program counter.\n\n\n## Run test with pytest\n\n```\npytest\n```\n\n## Building/Packaging\n\n```\npoetry update\npoetry build\npoetry publish\n```\n",
    'author': 'Brian Thorne',
    'author_email': 'brian@hardbyte.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hardbyte/sorting-gym',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.7',
}


setup(**setup_kwargs)
