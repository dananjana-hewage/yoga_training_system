from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import logging

# Initialize Flask App
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

try:
    # Load the saved model
    model = tf.keras.models.load_model('pose_estimation_model.keras')
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    model = None

# Define class names (Ensure this matches training class names)
class_names = []


@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded properly'}), 500

    try:
        # Get input data from request
        data = request.get_json()
        if not data or 'landmarks' not in data:
            return jsonify({'error': 'Invalid input data. Missing "landmarks" key.'}), 400

        # Convert received data to a NumPy array
        landmarks = np.array(data['landmarks']).reshape(1, -1)

        # Check the shape of the landmarks to ensure consistency
        logging.info(f"Landmarks shape: {landmarks.shape}")

        # Make prediction
        predictions = model.predict(landmarks)
        predicted_class = np.argmax(predictions)
        confidence = float(np.max(predictions))

        # Return the predicted class
        return jsonify({'predicted_class': class_names[predicted_class], 'confidence': confidence})

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/')
def home():
    return jsonify({'message': 'Pose Estimation API is running'}), 200


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)