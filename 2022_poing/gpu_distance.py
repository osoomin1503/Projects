#https://pysource.com
import cv2
#from realsense_camera import *
# https://pysource.com/instance-segmentation-mask-rcnn-with-python-and-opencv
import cv2
import numpy as np

point =(300,400)
class MaskRCNN:
    def __init__(self):
        # Loading Mask RCNN
        self.net = cv2.dnn.readNet("dnn/frozen_inference_graph_coco.pb", "dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")
        #self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        #self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        # Generate random colors
        np.random.seed(2)
        self.colors = np.random.randint(0, 255, (90, 3))

        # Conf threshold
        self.detection_threshold = 0.7
        self.mask_threshold = 0.3

        self.classes = []
        with open("dnn/classes.txt", "r") as file_object:
            for class_name in file_object.readlines():
                class_name = class_name.strip()
                self.classes.append(class_name)

        self.obj_boxes = []
        self.obj_classes = []
        self.obj_centers = []
        self.obj_contours = []

        # Distances
        self.distances = []
        self.area = []


    def detect_objects_mask(self, bgr_frame):
        blob = cv2.dnn.blobFromImage(bgr_frame, swapRB=True) # 알지비로 이미지 구현
        self.net.setInput(blob) # 색깔 제대로 바꾸고 삽임.
        boxes, masks = self.net.forward(["detection_out_final", "detection_masks"])
        # 박스로 정해진 객체,   마스크된 객체.

        # Detect objects
        frame_height, frame_width, _ = bgr_frame.shape # 칼라이미지 크기를 높이 넓이로 가져옴.
        detection_count = boxes.shape[2]

        # Object Boxes
        self.obj_boxes = [] # 다시 비우고 정의
        self.obj_classes = []
        self.obj_centers = []
        self.obj_contours = []
        self.area = []

        for i in range(detection_count): # 여러가지 감지된것 숫자.
            box = boxes[0, 0, i]
            class_id = box[1] # 지정된 클래스 이름
            score = box[2] # 지정된 클래스의 확률.
            color = self.colors[int(class_id)] # 클래스마다 색깔 지정가능.
            if score < self.detection_threshold: # 클래스의 확률이 일정이상 보다 작으면 다음.
                continue

            # Get box Coordinates
            x = int(box[3] * frame_width) # 인풋 사이즈 크기에 따라 박스가 다르게 설정할수있게!!
            y = int(box[4] * frame_height) # 따라서 박스는 인풋 사이즈와 크기를 고려한 값이다.
            x2 = int(box[5] * frame_width) # 따라서 박스 3,4는 1보다 작은 숫자로 픽셀의 위치를 표현한다.
            y2 = int(box[6] * frame_height)
            self.obj_boxes.append([x, y, x2, y2])
            ####### 중심점 대신 모멘텀으로 구할것이므로 밑에는 주석처리 하였다. ########'

            #cx = (x + x2) // 2 # 가운데의 포인트이다.
            #cy = (y + y2) // 2
            #self.obj_centers.append((cx, cy)) # 가운데 포인트 추가.

            # append class
            self.obj_classes.append(class_id) # 이름 추가.

            # Contours
            # Get mask coordinates
            # Get the mask
            mask = masks[i, int(class_id)] # 처음 가져온 마스크, : 마스크의 뭐와 클래스를 가져온다.
            #print(mask.shape) # 여기서는 15 * 15이다.
            roi_height, roi_width = y2 - y, x2 - x # ROI 길이 넓이 이다.
            mask = cv2.resize(mask, (roi_width, roi_height))
            _, mask = cv2.threshold(mask, self.mask_threshold, 255, cv2.THRESH_BINARY)
            #print(mask.shape) # 하지만 여기서 몇개 함수를 지나고 나면 박스의 크기가 맞춰져만들어진다.
            contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #area = cv2.contourArea(contours)
            #print(contours.shape)

            for c in contours:
                mmt = cv2.moments(c)

                if ['m00'] != 0:
                    cx = int(mmt['m10']/mmt['m00'])
                    cy = int(mmt['m01']/mmt['m00'])
                else:
                    cx, cy = 0, 0
            self.obj_centers.append((cx, cy))
            for cnt in contours:
                p_area = cv2.contourArea(cnt)
            areaMin = 0
            global point
            point = (cx, cy)
            print(point)
            self.obj_contours.append(contours)
            self.area.append(p_area)

        return self.obj_boxes, self.obj_classes, self.obj_contours, self.obj_centers,self.area


    def draw_object_info(self, bgr_frame, depth_frame):
        # loop through the detection
        for box, class_id, obj_center,area in zip(self.obj_boxes, self.obj_classes, self.obj_centers,self.area):
            x, y, x2, y2 = box

            color = self.colors[int(class_id)]
            color = (int(color[0]), int(color[1]), int(color[2]))

            cx, cy = obj_center

            # 여기서부터 면적과 깊이를 구하는 법.
            depth_mm = depth_frame[cy, cx]
            print(depth_mm)
            theta = 0
            pot_area = (depth_mm**2)*2.6563*area*(1E-9)/np.cos(theta)
            print(pot_area)
            cv2.line(bgr_frame, (cx, y), (cx, y2), color, 1)
            cv2.line(bgr_frame, (x, cy), (x2, cy), color, 1)

            class_name = self.classes[int(class_id)]
            cv2.rectangle(bgr_frame, (x, y), (x + 250, y + 70), color, -1)
            cv2.putText(bgr_frame, class_name.capitalize(), (x + 5, y + 25), 0, 0.8, (255, 255, 255), 2)
            cv2.putText(bgr_frame, "pothole depth : {} cm".format(depth_mm / 10), (x + 5, y + 60), 0, 1.0, (255, 255, 255), 2)
            cv2.rectangle(bgr_frame, (x, y), (x2, y2), color, 1)
            #cv2.putText(bgr_frame, 'area', (x + 5, y + 25), 0, 0.8, (255, 255, 255), 2)
            cv2.putText(bgr_frame,'pothole area : {}'.format(pot_area),(x + 5, y + 100), 0, 1.0, (255, 255, 255), 2)

    def draw_object_mask(self, bgr_frame):
        # loop through the detection
        for box, class_id, contours in zip(self.obj_boxes, self.obj_classes, self.obj_contours):
            x, y, x2, y2 = box
            roi = bgr_frame[y: y2, x: x2]
            roi_height, roi_width, _ = roi.shape
            color = self.colors[int(class_id)]

            roi_copy = np.zeros_like(roi)

            for cnt in contours:
                # cv2.f(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))
                cv2.drawContours(roi, [cnt], - 1, (int(color[0]), int(color[1]), int(color[2])), 3)
                cv2.fillPoly(roi_copy, [cnt], (int(color[0]), int(color[1]), int(color[2])))
                roi = cv2.addWeighted(roi, 1, roi_copy, 0.5, 0.0)
                bgr_frame[y: y2, x: x2] = roi
        return bgr_frame

    # def draw_object_info(self, bgr_frame, depth_frame):
    #     # loop through the detection
    #     for box, class_id, obj_center in zip(self.obj_boxes, self.obj_classes, self.obj_centers):
    #         x, y, x2, y2 = box

    #         color = self.colors[int(class_id)]
    #         color = (int(color[0]), int(color[1]), int(color[2]))

    #         cx, cy = obj_center

    #         # 여기서부터 면적과 깊이를 구하는 법.
    #         depth_mm = depth_frame[cy, cx]
    #         theta = 0
    #         pot_area = (depth_mm**2)*26.563*1/np.cos(theta)
    #         cv2.line(bgr_frame, (cx, y), (cx, y2), color, 1)
    #         cv2.line(bgr_frame, (x, cy), (x2, cy), color, 1)

    #         class_name = self.classes[int(class_id)]
    #         cv2.rectangle(bgr_frame, (x, y), (x + 250, y + 70), color, -1)
    #         cv2.putText(bgr_frame, class_name.capitalize(), (x + 5, y + 25), 0, 0.8, (255, 255, 255), 2)
    #         cv2.putText(bgr_frame, "{} cm".format(depth_mm / 10), (x + 5, y + 60), 0, 1.0, (255, 255, 255), 2)
    #         cv2.rectangle(bgr_frame, (x, y), (x2, y2), color, 1)




        return bgr_frame






#https://pysource.com
import pyrealsense2 as rs
import numpy as np
import cv2

class RealsenseCamera:
    def __init__(self):
        # Configure depth and color streams
        print("Loading Intel Realsense Camera")
        self.pipeline = rs.pipeline()

        config = rs.config()
        config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

        # Start streaming
        self.pipeline.start(config)
        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def get_frame_stream(self):
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        
        if not depth_frame or not color_frame:
            # If there is no frame, probably camera not connected, return False
            print("Error, impossible to get the frame, make sure that the Intel Realsense camera is correctly connected")
            return False, None, None
        
        # Apply filter to fill the Holes in the depth image
        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.holes_fill, 3)
        filtered_depth = spatial.process(depth_frame)

        hole_filling = rs.hole_filling_filter()
        filled_depth = hole_filling.process(filtered_depth)

        
        # Create colormap to show the depth of the Objects
        colorizer = rs.colorizer()
        depth_colormap = np.asanyarray(colorizer.colorize(filled_depth).get_data())
        
        
        # Convert images to numpy arrays
        # distance = depth_frame.get_distance(int(50),int(50))
        # print("distance", distance)
        depth_image = np.asanyarray(filled_depth.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # cv2.imshow("Colormap", depth_colormap)
        # cv2.imshow("depth img", depth_image)

        return True, color_image, depth_image

    def release(self):
        self.pipeline.stop()
        #print(depth_image)
        
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        #depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.10), 2)

        # Stack both images horizontally
        
        #images = np.hstack((color_image, depth_colormap))


###################################
###############################
# Load Realsense camera
rs1 = RealsenseCamera()
mrcnn = MaskRCNN()
point = (0,0)

while True:
	# Get frame in real time from Realsense camera
	ret, bgr_frame, depth_frame = rs1.get_frame_stream()

	# Get object mask
	boxes, classes, contours, centers,areas = mrcnn.detect_objects_mask(bgr_frame)
	# Draw object mask
	bgr_frame = mrcnn.draw_object_mask(bgr_frame)
    #dist = mrcnn.obj_centers
    #distance = depth_frame[dist[0],dist[1]]
	# Show depth info of the objects
	mrcnn.draw_object_info(bgr_frame, depth_frame)
    

	cv2.imshow("depth frame", depth_frame)
	cv2.imshow("Bgr frame", bgr_frame)

	key = cv2.waitKey(1)
	if key == 27:
		break

rs1.release()
cv2.destroyAllWindows()
