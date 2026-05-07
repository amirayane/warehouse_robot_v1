from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'warehouse_robot'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            glob('launch/*.py')),
        ('share/' + package_name + '/urdf',
            glob('urdf/*')),
        ('share/' + package_name + '/config',
            glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='amira',
    maintainer_email='amira@todo.todo',
    description='Warehouse robot with arm and gesture control',
    license='MIT',
    tests_require=['pytest'],
   entry_points={
    'console_scripts': [
        'hand_control = warehouse_robot.hand_control:main',
    ],
},
)