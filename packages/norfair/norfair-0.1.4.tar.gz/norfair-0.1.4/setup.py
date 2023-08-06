# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['norfair']

package_data = \
{'': ['*']}

install_requires = \
['filterpy>=1.4.5,<2.0.0', 'opencv-python>=3.2.0,<5.0.0', 'rich>=5.0.0,<6.0.0']

setup_kwargs = {
    'name': 'norfair',
    'version': '0.1.4',
    'description': 'Simple object tracker',
    'long_description': '# Norfair  [ TODO: Mention <points> in the intro ]\nNorfair is a Python library for adding tracking to any detector. It aims at being easy to use, providing tools for creating your video tracking program using Norfair, while being modular enough to integrate only the parts of Norfair you need into an already existing program.\n\nA typical use case would be any software alrady using a detector (such as object detection, instance segmentantion, pose estimation, etc) on video, seeking to easily add tracking to it. Another way we\'ve seen it used is to speed up video inference, by only running the detector every x frames, and using Norfair to interpolate the detections on the skipped frames.\n\n## Usage overview\nWe know that using the latest SOTA detector usually requires running the code associated to a research paper, which sometimes means getting an eval script working as an inference script, and generally having to tweak a code base which wasn\'t built with modularity and ease of use in mind. Therefore we designed Norfair so that it could seamlessly plug in into this way of working with research projects.\n\nNorfair consists of a set of tracking and video processing tools which are each designed to be usable on their own. You can create your video processing loop using just the tools Norfair provides, or plug parts of Norfair into your already existing video processing code.\n\nA simple example of an all Norfair loop:\n\n```python\n# Your detector\ndetector = SomeDetector()\n\n# Norfair\nvideo = Video(input_path="video.mp4")\ntracker = Tracker(distance_function=distance_fn)\n\nfor frame in video:\n    detections = detector(frame)\n    detections = convert_fn(detections)\n    tracked_objects = tracker.update(detections=detections)\n\n    norfair.draw_tracked_objects(frame, tracked_objects)\n    video.write(frame)\n```\n\nIt isn\'t alway easy to extract a SOTA detector into a nice single `detector` object, so here is a simple example of plugging Norfair into a research repo:\n\n```python\n### Find a good repo to use as a canonical Norfair demo\n```\n\n## Installation\n```bash\npip install norfair\n```\n\n## API\nNorfair provides a `Video` class to provide a simple and pythonic api to interact with video. It returns regular OpenCV frames which allows you to use the huge number of tools OpenCV provides to modify images.\n\nYou can get a simple video inference loop with just:\n```python\nvideo = Video(input_path="video.mp4")\nfor frame in video:\n    # Your modifications to the frame\n    video.write(frame)\n```\nwe think the api is a bit more pythonic than the standard OpenCV api, and it provides several nice ammenities such as an optional progress bar, and lets you not have to handle video formats, input validation, output file saving.\n\n\n',
    'author': 'joaqo',
    'author_email': 'joaquin.alori@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tryolabs/norfair',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
