[![Build Status](https://travis-ci.com/hdamron17/mulberry.svg?branch=master)](https://travis-ci.com/hdamron17/mulberry)
[![Documentation Status](https://readthedocs.org/projects/mulberry/badge/?version=latest)](https://mulberry.readthedocs.io/en/latest/?badge=latest)

# mulberry
Coordinate transformation tree with a focus on efficiency

## Overview
The goal of this project is to provide the functionality of [ROS's TF2](http://wiki.ros.org/tf2)
but without the need for the ROS framework or intraprocess communication.
By removing that restriction, we aim to allow more efficient transform querying by allowing
truly static transforms, cached intermediate connections, and unrestricted tree merging.

Another library [pytransform3d](https://pypi.org/project/pytransform3d/) also brings the
functionality of TF2 to non-ROS users, but is still bound to some of the restrictions of TF2
and so it cannot be optimized for mostly static trees.

## Contributing
This project is still in the very early stages and is not yet ready for community contributions,
but please let us know if there are any features which would make this tool more helpful
and we hope to have the framework set up for community contributions soon.
