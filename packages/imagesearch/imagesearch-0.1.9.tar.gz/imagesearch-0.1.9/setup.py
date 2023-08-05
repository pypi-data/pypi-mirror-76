# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imagesearch']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0', 'imagehash>=4.1.0,<5.0.0']

entry_points = \
{'console_scripts': ['imagesearch = imagesearch.__main__:main']}

setup_kwargs = {
    'name': 'imagesearch',
    'version': '0.1.9',
    'description': 'Measure visual similiarity of a reference image to other images.',
    'long_description': '# imagesearch\n\n![Build](https://github.com/t-mart/imagesearch/workflows/Build/badge.svg?branch=master)\n\n`imagesearch` measures visual similiarity between a reference image and a set of other\nimages. This can be used to search for a similar image in a large/deep directory structure.\n\n## Installation\n\n    pip install imagesearch\n\nSee [imagesearch on PyPI](https://pypi.org/project/imagesearch/).\n\n## Examples\n\n- Compare a reference image to all images in a search path:\n\n        > imagesearch needle.jpg haystack\\\n        28      haystack\\0.jpg\n        38      haystack\\1.jpg\n        12      haystack\\2.jpg\n        18      haystack\\3.jpg\n        32      haystack\\4.jpg\n        29      haystack\\5.jpg\n        0       haystack\\6.jpg\n        29      haystack\\7.jpg\n        5       haystack\\8.jpg\n        28      haystack\\9.jpg\n\n    In this example, `haystack\\6.jpg` is most similar.\n\n- Compare against a single image:\n\n        > imagesearch needle.jpg haystack\\1.jpg\n        38       haystack\\1.jpg\n\n- Only return images with similarity less than or equal to 10:\n\n        > imagesearch needle.jpg haystack\\ --threshold 10\n        0       haystack\\6.jpg\n        5       haystack\\8.jpg\n\n- Return the first image found under the threshold (0, in this case) and stop searching immediately:\n\n        > imagesearch needle.jpg haystack\\ -t 0 -1\n        0       haystack\\6.jpg\n\n- Specify a different algorithm:\n\n        > imagesearch needle.jpg haystack\\ --algorithm colorhash\n        ...\n\n- Get more help:\n\n        > imagesearch --help\n        ...\n\n## Visual Similiarity\n\n`imagesearch` returns a nonnegative integer that quantifies the visual similarity between the\nreference image and another image. It does this by creating an image fingerprint and looking at the\ndifference between them.\n\nA critical feature of these fingerprints is that they can be numerically compared (by Hamming Distance).\nImages that are different will have large differences in their fingerprints, and vice versa\n\n**A `0` value indicates the highest level of similarity, or possibly a true match.**\n\nUnless you have a good understanding of the algorihms used, values should be treated as\nopaque and subjective. It is dependent on the algorithm\nused to create the fingerprints and your criteria for what "similar" is.\n\nThis project uses the\n[imagehash](https://github.com/JohannesBuchner/imagehash) library to produce these fingerprints, and\nmore information about the techniques can be found there.\n\n## Algorithms\n\nAll the fingerprinting algorithms in `imagesearch` come from [imagehash](https://github.com/JohannesBuchner/imagehash). In `imagesearch`, you may specify which algorithm\nto use by passing the appropriate option value to the `-a` or `--algorithm` flag:\n\n- `ahash`: Average hashing (aHash)\n- `phash`: 2-axis perceptual hashing (pHash)\n- `phash-simple`: 1-axis perceptual hashing (pHash)\n- `dhash`: Horizontal difference hashing (dHash)\n- `dhash-vert`: Vertical difference hashing (dHash)\n- `whash-haar`: Haar wavelet hashing (wHash)\n- `whash-db4`: Daubechies wavelet hashing (wHash)\n- `colorhash`: HSV color hashing (colorhash)\n\n### Collisions\nThese algorithms trade away accuracy for speed and size, usually with acceptable results. Instead of producing an artifact that exactly identifies an image, there\'s analysis\ndone on some more abstract quality of the image, such as it\'s luminance or [signal frequency](https://en.wikipedia.org/wiki/Discrete_cosine_transform). This allows us\nto:\n- do less processing\n- get a fingerprint with a small size\n- get a fingerprint that exists in a linear space for comparison\n\nHowever, because the exact image analysis is abstract and produces a fixed-size fingerprint, it\'s absolutely possible for 2 different images to have the same fingerprint.\nThis is sort of an analog to cryptographic hash collosions, so it\'s important to understand what kinds of scenarios may cause this!\n\nSee\n[this section of the imagehash documentation](https://github.com/JohannesBuchner/imagehash#example-results)\nfor examples of different images that produce thesame fingerprint. The source code of that project also references other pages that explain the qualities of the algorithm.\n\n## Contributing\n\n### Bug Fixes/Features\n\nSubmit a PR from an appropriately named feature branch off of master.\n\n### Releasing\n\n1. Bump the version with `bumpversion [patch|minor|major]`. This will update the version number around the project, commit and tag it.\n2. Push the repo. A Github release will be made and published to PyPI.\n',
    'author': 'Tim Martin',
    'author_email': 'tim@timmart.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/t-mart/imagesearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
