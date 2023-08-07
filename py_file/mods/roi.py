import cv2

class BoundingBoxWidget(object):
    def __init__(self):
        self.original_image = cv2.imread('temp_img/test_rgb.jpg')
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points
        self.image_coordinates = []

    def extract_coordinates(self, event, x, y, flags, parameters):
        global x_cor,y_cor,w_cor,h_cor
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]

        # Record ending (x,y) coordintes on left mouse button release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            print('top left: {}, bottom right: {}'.format(self.image_coordinates[0], self.image_coordinates[1]))
            print('x,y,w,h : ({}, {}, {}, {})'.format(self.image_coordinates[0][0], self.image_coordinates[0][1], self.image_coordinates[1][0] - self.image_coordinates[0][0], self.image_coordinates[1][1] - self.image_coordinates[0][1]))
            
            x_cor = self.image_coordinates[0][0]
            y_cor = self.image_coordinates[0][1]
            w_cor = self.image_coordinates[1][0] - self.image_coordinates[0][0]
            h_cor = self.image_coordinates[1][1] - self.image_coordinates[0][1]
            val = f'{x_cor},{y_cor},{w_cor},{h_cor}'
            with open('temp_img/coordinates.txt', 'w') as f:
                f.write(val)
            # Draw rectangle 
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (240,255,250), 2)
            cv2.imshow("image", self.clone) 
            

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()
        elif event == ord('w'):
            cv2.destroyAllWindows()
            exit(1)

    def show_image(self):
        return self.clone

# if __name__ == '__main__':
    # boundingbox_widget = BoundingBoxWidget()
    # while True:
        
    #     cv2.imshow('image', boundingbox_widget.show_image())
    #     key = cv2.waitKey(1)

    #     # Close program with keyboard 'q'
    #     if key == ord('q'):
    #         cv2.destroyAllWindows()
    #         exit(1)
    #     elif key == ord('c'):
    #         print(x_cor,y_cor,w_cor,h_cor)
    #         cv2.destroyAllWindows()
    #         exit(1)