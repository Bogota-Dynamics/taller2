from setuptools import setup

package_name = 'taller2'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sebastian',
    maintainer_email='s.guerrero3@uniandes.edu.co',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = taller2.robot_bot_teleop:main',
            'listener = taller2.robot_bot_control:main',
            'pos = taller2.robot_bot_posicion:main',
            'inter = taller2.robot_bot_interface:main',
            'play = taller2.robot_bot_player:main'
        ],
    },
)
