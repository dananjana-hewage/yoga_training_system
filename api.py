from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
import mediapipe as mp

# Initialize Flask app
app = Flask(__name__)

# Load trained model
model = tf.keras.models.load_model('pose_estimation_model.keras')

# Load class names (should match training data)
class_names = ["Downdog", "Goddess", "Mountain", "Plank", "Tree", "Warrior1", "Warrior2"]  # Replace with actual class names

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose


# Function to get center point
def get_center_point(landmarks, hip_left_idx, hip_right_idx, shoulder_left_idx, shoulder_right_idx):
    hip_center = (landmarks[hip_left_idx][:2] + landmarks[hip_right_idx][:2]) / 2
    shoulder_center = (landmarks[shoulder_left_idx][:2] + landmarks[shoulder_right_idx][:2]) / 2
    return (hip_center + shoulder_center) / 2


# Function to get pose size
def get_pose_size(landmarks, torso_size_multiplier=2.5):
    pose_center = get_center_point(landmarks,
                                   mp_pose.PoseLandmark.LEFT_HIP.value,
                                   mp_pose.PoseLandmark.RIGHT_HIP.value,
                                   mp_pose.PoseLandmark.LEFT_SHOULDER.value,
                                   mp_pose.PoseLandmark.RIGHT_SHOULDER.value)

    hip_center = (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value][:2] + landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value][
                                                                       :2]) / 2
    shoulder_center = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][:2] + landmarks[
                                                                                     mp_pose.PoseLandmark.RIGHT_SHOULDER.value][
                                                                                 :2]) / 2
    torso_size = tf.norm(shoulder_center - hip_center)

    return tf.maximum(torso_size * torso_size_multiplier, tf.reduce_max(tf.norm(landmarks - pose_center, axis=1)))


# Function to normalize pose landmarks
def normalize_pose_landmarks(landmarks):
    landmarks = tf.convert_to_tensor(landmarks, dtype=tf.float32)
    pose_center = get_center_point(landmarks,
                                   mp_pose.PoseLandmark.LEFT_HIP.value,
                                   mp_pose.PoseLandmark.RIGHT_HIP.value,
                                   mp_pose.PoseLandmark.LEFT_SHOULDER.value,
                                   mp_pose.PoseLandmark.RIGHT_SHOULDER.value)
    landmarks = landmarks[:, :2] - pose_center
    pose_size = get_pose_size(landmarks)
    return landmarks / pose_size


# Function to convert landmarks to embedding
def landmarks_to_embedding(landmarks):
    normalized_landmarks = normalize_pose_landmarks(landmarks)
    return tf.reshape(normalized_landmarks, [-1])


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        user_landmarks = np.array(data['user_landmarks']).reshape(33, 3)
        processed_input = tf.convert_to_tensor([landmarks_to_embedding(user_landmarks)], dtype=tf.float32)
        predictions = model.predict(processed_input)
        predicted_class_index = np.argmax(predictions)
        confidence = np.max(predictions) * 100
        predicted_class = class_names[predicted_class_index]

        return jsonify({
            "predicted_class": predicted_class,
            "confidence": f"{confidence:.2f}%"
        })
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
