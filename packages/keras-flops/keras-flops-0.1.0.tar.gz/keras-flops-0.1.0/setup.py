# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keras_flops']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow>=2.2,<3.0']

setup_kwargs = {
    'name': 'keras-flops',
    'version': '0.1.0',
    'description': 'FLOPs calculator for neural network architecture written in tensorflow 2.x (tf.keras)',
    'long_description': '# keras-flops\n\n![](https://github.com/tokusumi/keras-flops/workflows/Tests/badge.svg)\n\nFLOPs calculator for neural network architecture written in tensorflow (tf.keras) v2.2+\n\nThis stands on the shoulders of giants, [tf.profiler](https://www.tensorflow.org/api_docs/python/tf/compat/v1/profiler/Profiler). \n\n## Requirements\n\n* Python 3.6+\n* Tensorflow 2.2+\n\n## Installation\n\nThis implementation is simple thanks to stands on the shoulders of giants, [tf.profiler](https://www.tensorflow.org/api_docs/python/tf/compat/v1/profiler/Profiler). Only one function is defined.\n\nCopy and paste [it](https://github.com/tokusumi/keras-flops/blob/master/keras_flops/flops_calculation.py).\n\n## Example\n\nSee colab examples [here](https://github.com/tokusumi/keras-flops/tree/master/notebooks) in details.\n\n```python\nfrom tensorflow.keras import Model, Input\nfrom tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout\n\nfrom keras_flops import get_flops\n\n# build model\ninp = Input((32, 32, 3))\nx = Conv2D(32, kernel_size=(3, 3), activation="relu")(inp)\nx = Conv2D(64, (3, 3), activation="relu")(x)\nx = MaxPooling2D(pool_size=(2, 2))(x)\nx = Dropout(0.25)(x)\nx = Flatten()(x)\nx = Dense(128, activation="relu")(x)\nx = Dropout(0.5)(x)\nout = Dense(10, activation="softmax")(x)\nmodel = Model(inp, out)\n\n# Calculae FLOPS\nflops = get_flops(model, batch_size=1)\nprint(f"FLOPS: {flops / 10 ** 9:.03} G")\n# >>> FLOPS: 0.0338 G\n```\n\n## Support\n\nSupport `tf.keras.layers` as follows,\n\n| name | layer | \n| -- | -- |\n| Conv | Conv[1D/2D/3D]|\n| | Conv[1D/2D]Transpose |\n| | DepthwiseConv2D |\n| | SeparableConv[1D/2D] |\n| Pooling | AveragePooling[1D/2D] |\n| | GlobalAveragePooling[1D/2D/3D]|\n| | MaxPooling[1D/2D] |\n| | GlobalMaxPool[1D/2D/3D] |\n| Normalization | BatchNormalization |\n| Activation | Softmax |\n| Attention | Attention |\n| | AdditiveAttention |\n| others | Dense |\n\n## Not supported\n\nNot support `tf.keras.layers` as follows. They are calculated as zero or smaller value than correct value.\n\n| name | layer | \n| -- | -- |\n| Conv | Conv3DTranspose |\n| Pooling | AveragePooling3D |\n| | MaxPooling3D |\n| | UpSampling[1D/2D/3D] |\n| Normalization | LayerNormalization |\n| RNN | SimpleRNN |\n| | LSTM |\n| | GRU |\n| others | Embedding |',
    'author': 'tokusumi',
    'author_email': 'tksmtoms@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tokusumi/keras-flops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
