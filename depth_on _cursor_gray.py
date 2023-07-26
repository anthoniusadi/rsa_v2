import cv2
import numpy as np
import pyrealsense2 as rs

cursor_x, cursor_y = 320, 240  # Initial cursor position (center of the frame)
depth_value = 0
depth_frame = None  # Global variable for the depth frame

def on_mouse_click(event, x, y, flags, param):
    global cursor_x, cursor_y, depth_value
    if event == cv2.EVENT_LBUTTONDOWN:
        cursor_x, cursor_y = x, y
        if depth_frame:
            depth_value = depth_frame.get_distance(cursor_x, cursor_y)
            print(f"Depth value at cursor position ({cursor_x}, {cursor_y}): {depth_value:.2f} meters")

def main():
    global depth_frame  # Declare the depth_frame variable as global

    # Initialize the RealSense pipeline
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    # Start the pipeline
    pipeline.start(config)

    cv2.namedWindow("Depth Camera")
    cv2.setMouseCallback("Depth Camera", on_mouse_click)

    try:
        while True:
            # Wait for a new frame from the camera
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()

            if not depth_frame:
                continue

            # Convert the depth frame to a NumPy array
            depth_image = np.asanyarray(depth_frame.get_data())

            # Show the depth image with the cursor position marked
            depth_image_with_cursor = depth_image.copy()
            cv2.circle(depth_image_with_cursor, (cursor_x, cursor_y), 5, (0, 255, 0), -1)

            # Show the combined image
            cv2.imshow("Depth Camera", depth_image_with_cursor)

            # Exit the loop when the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Stop the pipeline and release resources
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
