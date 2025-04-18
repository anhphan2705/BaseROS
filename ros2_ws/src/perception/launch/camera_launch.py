import launch
import launch_ros.actions

def generate_launch_description():
    camera_node = launch_ros.actions.Node(
        package='perception',
        executable='camera_node',
        name='camera_node',
        output='screen'
    )

    camera_splitter_node = launch_ros.actions.Node(
        package='perception',
        executable='camera_splitter_node',
        name='camera_splitter_node',
        output='screen'
    )

    manual_focus_node = launch_ros.actions.Node(
        package='perception',
        executable='manual_focus_node',
        name='manual_focus_node',
        output='screen'
    )

    sync_capture_node = launch_ros.actions.Node(
        package='perception',
        executable='sync_capture_node',
        name='sync_capture_node',
        output='screen'
    )

    delayed_manual_focus_node = launch.actions.TimerAction(
        period=10.0,
        actions=[manual_focus_node]
    )

    camera_rectification_node = launch_ros.actions.Node(
        package='calibration',
        executable='camera_rectification_node',
        name='camera_rectification_node',
        output='screen',
    )

    stereo_depth_node = launch_ros.actions.Node(
        package='perception',
        executable='stereo_depth_node',
        name='stereo_depth_node',
        output='screen',
        parameters=[
            {'sub_left_0': '/camera/rectified/split_0'},
            {'sub_right_0': '/camera/rectified/split_1'},
            {'sub_left_1': '/camera/rectified/split_2'},
            {'sub_right_1': '/camera/rectified/split_3'},
            {'horizontal_fov_deg': 66.0},
            {'baseline_m': 0.05},
            
        ]
    )

    yolov8_detection_0 = launch_ros.actions.Node(
        package='perception',
        executable='object_detection_node',
        name='yolo_detection_0',
        output='screen',
        parameters=[
            {'model_path': 'yolov8n.pt'},
            {'image_topic': '/camera/rectified/split_0'},
            {'detection_topic': '/yolo/detections_0'}
        ]
    )

    yolov8_detection_1 = launch_ros.actions.Node(
        package='perception',
        executable='object_detection_node',
        name='yolo_detection_1',
        output='screen',
        parameters=[
            {'model_path': 'yolov8s.pt'},
            {'image_topic': '/camera/rectified/split_2'},
            {'detection_topic': '/yolo/detections_1'}
        ]
    )
    
    object_depth_fusion_node_0 = launch_ros.actions.Node(
        package='perception',
        executable='object_depth_fusion_node',
        name='object_depth_fusion_node_0',
        output='screen',
        parameters=[
            {'detection_topic': '/yolo/detections_0'},
            {'depth_topic': '/camera/depth_map_0'},
            {'output_topic': '/yolo/detections_0/depth'}
        ]
    )
    
    object_depth_fusion_node_1 = launch_ros.actions.Node(
        package='perception',
        executable='object_depth_fusion_node',
        name='object_depth_fusion_node',
        output='screen',
        parameters=[
            {'detection_topic': '/yolo/detections_1'},
            {'depth_topic': '/camera/depth_map_1'},
            {'output_topic': '/yolo/detections_1/depth'}
        ]
    )
    
    # overlay_0 = launch_ros.actions.Node(
    #     package='perception',
    #     executable='bbox_overlay_node',
    #     name='bbox_overlay_0',
    #     output='screen',
    #     parameters=[
    #         {'image_topic': '/camera/rectified/split_0'},
    #         {'detection_topic': '/yolo/detections_0/depth'},
    #         {'output_topic': '/camera/yolo_overlay_0'}
    #     ]
    # )

    # overlay_1 = launch_ros.actions.Node(
    #     package='perception',
    #     executable='bbox_overlay_node',
    #     name='bbox_overlay_1',
    #     output='screen',
    #     parameters=[
    #         {'image_topic': '/camera/rectified/split_2'},
    #         {'detection_topic': '/yolo/detections_1/depth'},
    #         {'output_topic': '/camera/yolo_overlay_1'}
    #     ]
    # )

    # object_depth_fusion_tracked_node_0 = launch_ros.actions.Node(
    #     package='perception',
    #     executable='object_depth_fusion_tracked_node',
    #     name='object_depth_fusion_tracked_node_0',
    #     output='screen',
    #     parameters=[
    #         {'detection_topic': '/yolo/detections_0'},
    #         {'depth_topic': '/camera/depth_map_0'},
    #         {'output_topic': '/yolo/detections_0/depth'}
    #     ]
    # )

    # object_depth_fusion_tracked_node_1 = launch_ros.actions.Node(
    #     package='perception',
    #     executable='object_depth_fusion_tracked_node',
    #     name='object_depth_fusion_tracked_node_1',
    #     output='screen',
    #     parameters=[
    #         {'detection_topic': '/yolo/detections_1'},
    #         {'depth_topic': '/camera/depth_map_1'},
    #         {'output_topic': '/yolo/detections_1/depth'}
    #     ]
    # )

    byte_track_node_0 = launch_ros.actions.Node(
        package='perception',
        executable='byte_track_node',
        name='byte_track_node_0',
        output='screen',
        parameters=[
            {'input_topic': '/yolo/detections_0/depth'},
            {'output_topic': '/yolo/detections_0/depth/tracked'},
            {'image_topic': '/camera/rectified/split_0'},
            {'horizontal_fov_deg': 66.0},
            {'vertical_fov_deg': 49.5},
        ]
    )
    
    byte_track_node_1 = launch_ros.actions.Node(
        package='perception',
        executable='byte_track_node',
        name='byte_track_node_1',
        output='screen',
        parameters=[
            {'input_topic': '/yolo/detections_1/depth'},
            {'output_topic': '/yolo/detections_1/depth/tracked'},
            {'image_topic': '/camera/rectified/split_2'},
            {'horizontal_fov_deg': 66.0},
            {'vertical_fov_deg': 49.5},
        ]
    )
    
    tracked_overlay_0 = launch_ros.actions.Node(
        package='perception',
        executable='tracked_bbox_overlay_node',
        name='tracked_overlay_0',
        output='screen',
        parameters=[
            {'image_topic': '/camera/rectified/split_0'},
            {'tracked_topic': '/yolo/detections_0/depth/tracked'},
            {'output_topic': '/camera/yolo_overlay_tracked_0'}
        ]
    )
    
    tracked_overlay_1 = launch_ros.actions.Node(
        package='perception',
        executable='tracked_bbox_overlay_node',
        name='tracked_overlay_1',
        output='screen',
        parameters=[
            {'image_topic': '/camera/rectified/split_1'},
            {'tracked_topic': '/yolo/detections_1/depth/tracked'},
            {'output_topic': '/camera/yolo_overlay_tracked_1'}
        ]
    )

    return launch.LaunchDescription([
        camera_node,
        camera_splitter_node,
        delayed_manual_focus_node,
        sync_capture_node,
        camera_rectification_node,
        stereo_depth_node,
        yolov8_detection_0,
        # yolov8_detection_1,
        object_depth_fusion_node_0,
        # object_depth_fusion_node_1,
        # overlay_0,
        # overlay_1,
        # object_depth_fusion_tracked_node_0,
        # object_depth_fusion_tracked_node_1,   
        byte_track_node_0,
        # byte_track_node_1,
        tracked_overlay_0,
        # tracked_overlay_1,
    ])