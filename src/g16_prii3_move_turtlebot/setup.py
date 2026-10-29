import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'g16_prii3_move_turtlebot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='emin',
    maintainer_email='eminmujahid4@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'draw_number = g16_prii3_move_turtlebot.draw_number:main',
            'collision_avoidance = g16_prii3_move_turtlebot.collision_avoidance:main',
            'obstacle_avoidance = g16_prii3_move_turtlebot.obstacle_avoidance:main',
        ],
    },
)
