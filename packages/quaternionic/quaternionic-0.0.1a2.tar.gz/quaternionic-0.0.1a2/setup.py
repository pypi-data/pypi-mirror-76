# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quaternionic']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.50,<0.51', 'numpy>=1.13,<2.0', 'scipy>=1.0,<2.0']

setup_kwargs = {
    'name': 'quaternionic',
    'version': '0.0.1a2',
    'description': 'Interpret numpy arrays as quaternion arrays with numba acceleration',
    'long_description': "# Quaternions by way of numpy arrays\n\nThis module subclasses numpy's array type, interpreting the array as an array of quaternions, and\naccelerating the algebra using numba.\n\nThis package has evolved from the [quaternion](https://github.com/moble/quaternion) package, which\nadds a quaternion dtype directly to numpy.  In many ways, that is a much better approach because\ndtypes are built in to numpy, making it more robust than this package.  However, that approach has\nits own limitations, including that it is harder to maintain, and requires much of the code to be\nwritten in C, which also makes it harder to distribute.  This package is written entirely in python\ncode, but should actually have comparable performance.\n\n\n\n\n# Similar packages\n\nPackages with similar features available on pypi include\n  * numpy-quaternion\n  * Quaternion\n  * quaternions\n  * pyquaternion\n  * rowan\n  * clifford\n  * scipy.spatial.transform.Rotation.as_quat\n  * mathutils (a Blender package with python bindings)\n\nAlso note that there is some capability to do symbolic manipulations of quaternions in these packages:\n  * galgebra\n  * sympy.algebras.quaternion\n\n",
    'author': 'Michael Boyle',
    'author_email': 'michael.oliver.boyle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moble/quaternionic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
