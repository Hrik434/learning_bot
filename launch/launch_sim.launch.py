import os

from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument,  TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():

    package_name = 'learning_bot'

    # Robot State Publisher
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory(package_name),
                'launch',
                'rsp.launch.py'
            )
        ),
        launch_arguments={'use_sim_time': 'true'}.items()
    )


    # Launch Gazebo Classic

    world = LaunchConfiguration('world')

    world_arg = DeclareLaunchArgument(
        'world',
        default_value=os.path.join(
            get_package_share_directory(package_name),
            'worlds',
            'empty.world'
        ),
        description='Gazebo world file'
    )
    
    gazebo = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('gazebo_ros'),
            'launch',
            'gazebo.launch.py'
        )
    ),
    launch_arguments={
        'world': world
    }.items()

    )


    # Spawn robot into Gazebo Classic
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic',
            'robot_description',
            '-entity',
            'my_bot',
            '-z',
            '0.1'
        ],
        output='screen'
    )

    spawn_entity_delay = TimerAction(
        period=3.0,
        actions=[spawn_entity]
    )


    return LaunchDescription([
        world_arg,
        rsp,
        gazebo,
        spawn_entity_delay,
    ])