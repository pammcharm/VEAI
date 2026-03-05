#!/usr/bin/env python3
"""
VEAI Vision Processor
AI Eyes - Computer Vision using Pre-trained Models

Models:
- OpenCV DNN (MobileNet-SSD) - Object detection
- MediaPipe - Face detection, hand tracking, pose
- YOLO - Object detection (optional)
"""

import os
import cv2
import numpy as np

class VisionProcessor:
    """AI Eyes - Computer Vision Processing"""
    
    def __init__(self):
        self.net = None
        self.class_names = []
        self.face_detector = None
        self.pose_detector = None
        self.hand_detector = None
        
    def init_mobilenet(self):
        """Initialize MobileNet-SSD for object detection"""
        try:
            # Load MobileNet-SSD model
            prototxt = os.path.join(os.path.dirname(__file__), "vision", "deploy.prototxt")
            caffemodel = os.path.join(os.path.dirname(__file__), "vision", "MobileNetSSD_deploy.caffemodel")
            
            if os.path.exists(prototxt) and os.path.exists(caffemodel):
                self.net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
                print("MobileNet-SSD loaded")
            else:
                print("MobileNet-SSD model files not found")
                # Use default OpenCV DNN
                self.net = cv2.dnn.readNetFromTensorflow(
                    os.path.join(os.path.dirname(__file__), "vision", "ssd_mobilenet_v2_coco.pb"),
                    os.path.join(os.path.dirname(__file__), "vision", "ssd_mobilenet_v2_coco.pbtxt")
                )
                
            # COCO class names
            self.class_names = [
                'background', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
                'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
                'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
                'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
                'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
                'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
                'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table',
                'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
                'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
            ]
            return True
        except Exception as e:
            print(f"MobileNet init failed: {e}")
            return False
            
    def init_mediapipe(self):
        """Initialize MediaPipe for face/hand/pose detection"""
        try:
            import mediapipe as mp
            
            # Face detection
            self.face_detector = mp.solutions.face_detection.FaceDetection(
                model_selection=0, min_detection_confidence=0.5
            )
            
            # Hand tracking
            self.hand_detector = mp.solutions.hands.Hands(
                max_num_hands=2, min_detection_confidence=0.5
            )
            
            # Pose estimation
            self.pose_detector = mp.solutions.pose.Pose(
                min_detection_confidence=0.5
            )
            
            self.mp_draw = mp.solutions.drawing_utils
            print("MediaPipe loaded (Face, Hands, Pose)")
            return True
        except Exception as e:
            print(f"MediaPipe init failed: {e}")
            return False
            
    def detect_objects(self, frame):
        """Detect objects in frame using MobileNet"""
        if not self.net:
            return []
            
        # Preprocess
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5
        )
        self.net.setInput(blob)
        detections = self.net.forward()
        
        results = []
        h, w = frame.shape[:2]
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                box = box.astype(int)
                
                results.append({
                    "class": self.class_names[class_id] if class_id < len(self.class_names) else "unknown",
                    "confidence": float(confidence),
                    "bbox": box.tolist()
                })
                
        return results
        
    def detect_faces(self, frame):
        """Detect faces using MediaPipe"""
        if not self.face_detector:
            return []
            
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detector.process(rgb)
        
        faces = []
        if results.detections:
            h, w = frame.shape[:2]
            for det in results.detections:
                box = det.location_data.relative_bounding_box
                faces.append({
                    "confidence": det.score[0],
                    "bbox": [
                        int(box.xmin * w), int(box.ymin * h),
                        int(box.width * w), int(box.height * h)
                    ]
                })
                
        return faces
        
    def detect_hands(self, frame):
        """Detect hands using MediaPipe"""
        if not self.hand_detector:
            return []
            
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hand_detector.process(rgb)
        
        hands = []
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                # Get hand bounding box from landmarks
                xs = [lm.x for lm in landmarks.landmark]
                ys = [lm.y for lm in landmarks.landmark]
                h, w = frame.shape[:2]
                
                hands.append({
                    "bbox": [
                        int(min(xs) * w), int(min(ys) * h),
                        int((max(xs) - min(xs)) * w), int((max(ys) - min(ys)) * h)
                    ],
                    "landmarks": [(lm.x, lm.y, lm.z) for lm in landmarks.landmark]
                })
                
        return hands
        
    def detect_pose(self, frame):
        """Detect human pose using MediaPipe"""
        if not self.pose_detector:
            return None
            
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose_detector.process(rgb)
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            h, w = frame.shape[:2]
            
            # Get key body points
            keypoints = {}
            for i, lm in enumerate(landmarks):
                keypoints[i] = (int(lm.x * w), int(lm.y * h), lm.visibility)
                
            return keypoints
            
        return None
        
    def draw_results(self, frame, objects=None, faces=None, hands=None, pose=None):
        """Draw detection results on frame"""
        result = frame.copy()
        
        # Draw objects
        if objects:
            for obj in objects:
                x1, y1, x2, y2 = obj["bbox"]
                cv2.rectangle(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{obj['class']}: {obj['confidence']:.2f}"
                cv2.putText(result, label, (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                           
        # Draw faces
        if faces:
            for face in faces:
                x1, y1, w, h = face["bbox"]
                cv2.rectangle(result, (x1, y1), (x1+w, y1+h), (255, 0, 0), 2)
                
        return result


class ObjectTracker:
    """Track objects across frames"""
    
    def __init__(self):
        self.tracked_objects = {}
        self.next_id = 0
        
    def update(self, detections, frame):
        """Update tracked objects with new detections"""
        # Simple tracking based on centroid distance
        tracked = []
        
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            
            # Find closest existing track
            best_match = None
            best_dist = float('inf')
            
            for track_id, track in self.tracked_objects.items():
                tx, ty = track["center"]
                dist = ((cx - tx) ** 2 + (cy - ty) ** 2) ** 0.5
                if dist < best_dist and dist < 50:
                    best_dist = dist
                    best_match = track_id
                    
            if best_match is not None:
                self.tracked_objects[best_match] = {
                    "class": det["class"],
                    "center": (cx, cy),
                    "bbox": det["bbox"],
                    "confidence": det["confidence"],
                    "frames": self.tracked_objects[best_match]["frames"] + 1
                }
                tracked.append((best_match, det))
            else:
                track_id = self.next_id
                self.next_id += 1
                self.tracked_objects[track_id] = {
                    "class": det["class"],
                    "center": (cx, cy),
                    "bbox": det["bbox"],
                    "confidence": det["confidence"],
                    "frames": 1
                }
                tracked.append((track_id, det))
                
        return tracked


# Demo
if __name__ == "__main__":
    print("VEAI Vision Processor Test")
    print("-" * 30)
    
    vision = VisionProcessor()
    
    # Try to initialize MediaPipe
    if vision.init_mediapipe():
        print("\nMediaPipe ready!")
        print("Functions available:")
        print("  - detect_objects(frame) - Object detection")
        print("  - detect_faces(frame) - Face detection")
        print("  - detect_hands(frame) - Hand tracking")
        print("  - detect_pose(frame) - Pose estimation")
    else:
        print("\nUsing OpenCV DNN fallback")
