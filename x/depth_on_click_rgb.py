

import pyrealsense2 as rs
import numpy as np
import cv2

cursor_x, cursor_y = 0, 0  
depth_value = 0
depth_frame = None  

def on_mouse_click(event, x, y, flags, param):
    global cursor_x, cursor_y, aligned_depth_frame,depth_value
    if event == cv2.EVENT_LBUTTONDOWN:
        cursor_x, cursor_y = x, y
        if aligned_depth_frame:
            depth_value = aligned_depth_frame.get_distance(cursor_x, cursor_y)
            print(f"Depth ({cursor_x}, {cursor_y}): {depth_value*100:.5f} Cm")
            return f"Depth ({cursor_x}, {cursor_y}): {depth_value*100:.5f} Cm"

pipeline = rs.pipeline()


config = rs.config()


pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))
# cv2.setMouseCallback("depth_colormap", on_mouse_click)
found_rgb = True
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth : " , depth_scale)

clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

align_to = rs.stream.color
align = rs.align(align_to)

try:
    global aligned_depth_frame
    
    while True:

        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)


        aligned_depth_frame = aligned_frames.get_depth_frame() 
        color_frame = aligned_frames.get_color_frame()

        # Validate 
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Remove background
        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image = 1 channel, color = 3 channels
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        # tumpuk
        # images = np.hstack((bg_removed, depth_colormap))
        depth_image_with_cursor = depth_colormap.copy()
        cv2.circle(depth_image_with_cursor, (cursor_x, cursor_y), 5, (0, 255, 0), -1)
        
        cv2.namedWindow('depth_colormap')
        cv2.setMouseCallback("depth_colormap", on_mouse_click)
        text =f"Depth: {depth_value*100:.5f} Cm"
        # cv2.imshow('Align Example', images)
        cv2.imshow('bg', bg_removed)
        cv2.putText(depth_image_with_cursor,text,(100,50),cv2.FONT_HERSHEY_SIMPLEX,1,(29,180,200),2)
        
        cv2.imshow('depth_colormap', depth_image_with_cursor)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('c'):
            cv2.imwrite('data/test_depth.jpg',depth_image_with_cursor)
            cv2.imwrite('data/test_rgb.jpg',bg_removed)
            
            
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()