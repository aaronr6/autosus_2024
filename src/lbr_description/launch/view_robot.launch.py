# import os
# from ament_index_python.packages import get_package_share_directory, get_package_share_path
# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument
# from launch.substitutions import LaunchConfiguration, Command
# from launch_ros.actions import Node
# from launch_ros.parameters_type import ParameterValue


# def generate_launch_description():

#     use_sim_time = LaunchConfiguration('use_sim_time', default='false')

#     urdf_file_name = 'iiwa14.urdf.xacro'
#     path_to_urdf = get_package_share_path('lbr_description') / 'urdf' / urdf_file_name
#     # urdf = os.path.join(
#     #     get_package_share_directory('lbr_description'),
#     #     urdf_file_name)
#     # with open(urdf, 'r') as infp:
#     #     robot_desc = infp.read()

#     return LaunchDescription([
#         DeclareLaunchArgument(
#             'use_sim_time',
#             default_value='false',
#             description='Use simulation (Gazebo) clock if true'),
#         Node(
#             package='robot_state_publisher',
#             executable='robot_state_publisher',
#             name='robot_state_publisher',
#             output='screen',
#             parameters=[{'use_sim_time': use_sim_time, 'robot_description': Command(['xacro', ' ', str(path_to_urdf)])}]
#             )
#         # Node(
#         #     package='lbr_description',
#         #     executable='state_publisher',
#         #     name='state_publisher',
#         #     output='screen'),
#     ])


# from launch import LaunchDescription
# from launch_ros.actions import Node
# from launch.actions import IncludeLaunchDescription
# from launch.substitutions import PathJoinSubstitution
# from launch_ros.substitutions import FindPackageShare


# def generate_launch_description() -> LaunchDescription:
#     ld = LaunchDescription()

#     ld.add_action(IncludeLaunchDescription(
#         PathJoinSubstitution([FindPackageShare("lbr_description"), "launch", "view_robot.launch.py"]),
#         launch_arguments={
#             'urdf_package': 'lbr_description',
#             'urdf_package_path': PathJoinSubstitution(['urdf', 'iiwa14.urdf'])}.items()
#     ))
    
#     ld.add_action(
#         Node(
#             package="robot_state_publisher",
#             executable="robot_state_publisher",
#             output="screen"
#         )
#     )
#     return ld


import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    urdf_file_name = 'iiwa14_description.urdf'
    urdf = os.path.join(
        get_package_share_directory('lbr_description'),
        urdf_file_name)
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[urdf]),
        Node(
            package='lbr_description',
            executable='state_publisher',
            name='state_publisher',
            output='screen'),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', 'src/lbr_description/config/rviz_config.rviz']),
    ])