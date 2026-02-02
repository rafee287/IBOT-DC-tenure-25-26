from setuptools import find_packages, setup

package_name = 'my_turtle_project'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rafee',
    maintainer_email='rafee2587@gmail.com',
    description='Custom ROS2 package to spawn and control turtles in turtlesim',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'spawn_ball_turtle = my_turtle_project.spawn_ball_turtle:main',
            'follow_turtle = my_turtle_project.follow_turtle:main',
            'turtle_ball = my_turtle_project.turtle_ball:main',
            'turtle_player_1 = my_turtle_project.turtle_player_1:main',
            'turtle_player_2 = my_turtle_project.turtle_player_2:main',
            'spawn_player_2_turtle = my_turtle_project.spawn_player_2_turtle:main',
        ],
    },

)
