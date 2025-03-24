import mediapipe as mp
import cv2

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Read an image
image = cv2.imread('Yoga_final_dataset/Tree/00000004.jpg')
# Convert the image to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Process the image
results = pose.process(image_rgb)

# Access the landmarks
if results.pose_landmarks:
    landmarks = []
    for landmark in results.pose_landmarks.landmark:
        landmarks.append([landmark.x, landmark.y])
    print(landmarks)  # This will print the real landmarks for the given image
