from setuptools import find_packages, setup
import os

package_name = 'perception'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(include=['perception', 'perception.*'], exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), ['launch/camera_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='anhphan',
    maintainer_email='anhphanvt2705@gmail.com',
    description='Manage all perception devices in the RP-1 Base Station',
    license='Private',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_node = perception.camera_node:main',
            'autofocus_node = perception.autofocus_node:main',
            'manual_focus_node = perception.manual_focus_node:main',
            'camera_splitter_node = perception.camera_splitter_node:main',
            'sync_capture_node = perception.sync_capture_node:main',
            'stereo_depth_node = perception.stereo_depth_node:main',
        ],
    },
)
