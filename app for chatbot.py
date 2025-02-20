from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # Allow frontend to communicate with backend

feedback_list = []  # Store user feedback
pose_info = {
    "Adho Mukha Svanasana": (
        "<p>Adho Mukha Svanasana, or Downward Dog Pose, is an inverted V-shape pose that strengthens the arms, "
        "shoulders, and back while stretching the hamstrings and calves. It also helps to improve circulation and "
        "relieve stress. This pose engages the entire body, providing both strength and flexibility benefits.</p>"
        "<p><strong>Benefits:</strong></p>"
        "<ul>"
        "<li>Strengthens the arms, shoulders, and back.</li>"
        "<li>Stretches the hamstrings and calves.</li>"
        "<li>Improves circulation.</li>"
        "<li>Relieves stress and calms the mind.</li>"
        "</ul>"
    ),
    "Anjaneyasana": (
        "<p>Anjaneyasana, or Low Lunge Pose, opens the hips, stretches the thighs, and strengthens the legs. "
        "It also lengthens the spine and improves flexibility in the groin and hips. This pose is great for preparing "
        "the body for deeper stretches and more intense postures.</p>"
        "<p><strong>Benefits:</strong></p>"
        "<ul>"
        "<li>Opens the hips and stretches the thighs.</li>"
        "<li>Improves flexibility in the groin.</li>"
        "<li>Strengthens the legs and core.</li>"
        "<li>Lengthens the spine and improves posture.</li>"
        "</ul>"
    ),
    "Phalakasana": (
        "<p>Phalakasana, or Plank Pose, is a full-body strength pose that focuses on core strength, stability, and endurance. "
        "It works the entire body, especially the core, arms, and shoulders, and helps to improve posture by engaging the "
        "muscles of the back. It is often used as a foundational pose for building core strength.</p>"
        "<p><strong>Benefits:</strong></p>"
        "<ul>"
        "<li>Strengthens the core, arms, and shoulders.</li>"
        "<li>Improves posture and balance.</li>"
        "<li>Builds endurance and stability.</li>"
        "<li>Tones the entire body.</li>"
        "</ul>"
    ),
    "Setu Bandha Sarvangasana": (
        "<p>Setu Bandha Sarvangasana, or Bridge Pose, strengthens the back, glutes, and legs while opening the chest. "
        "It is a great pose to release tension in the back and stretch the spine, and it also helps in improving blood circulation."
        " It can be used to prepare for deeper backbends.</p>"
        "<p><strong>Benefits:</strong></p>"
        "<ul>"
        "<li>Strengthens the back, glutes, and legs.</li>"
        "<li>Opens the chest and shoulders.</li>"
        "<li>Improves blood circulation.</li>"
        "<li>Relieves stress and anxiety.</li>"
        "</ul>"
    ),
    "Trikonasana": (
        "<p>Trikonasana, or Triangle Pose, stretches the legs, hips, and spine while strengthening the core. It also enhances "
        "balance and stability, making it a great pose for overall body strength and flexibility. This pose is particularly "
        "effective for opening the chest and improving digestion.</p>"
        "<p><strong>Benefits:</strong></p>"
        "<ul>"
        "<li>Stretches the legs, hips, and spine.</li>"
        "<li>Strengthens the core and legs.</li>"
        "<li>Improves balance and stability.</li>"
        "<li>Stimulates digestion and improves posture.</li>"
        "</ul>"
    ),
    "Utkatasana": (
        "<p>Utkatasana, or Chair Pose, strengthens the legs and core while improving endurance. This intense pose also improves "
        "balance and flexibility in the hips, and is often used in sequences to build heat in the body. It requires deep engagement "
        "of the lower body and core muscles.</p>"
        "<p><strong>Benefits:</strong></p>"
        "<ul>"
        "<li>Strengthens the legs, glutes, and core.</li>"
        "<li>Improves balance and stability.</li>"
        "<li>Builds endurance and flexibility in the hips.</li>"
        "<li>Stimulates the abdominal organs.</li>"
        "</ul>"
    ),
    "Virabhadrasana 2": (
        "<p>Virabhadrasana 2, or Warrior II Pose, strengthens the legs, opens the hips, and improves focus and stability. "
        "It is a powerful standing pose that builds endurance and helps to improve overall body alignment and posture. "
        "It also increases stamina and mental focus.</p>"
        "<p><strong>Benefits:</strong></p>"
        "<ul>"
        "<li>Strengthens the legs, hips, and core.</li>"
        "<li>Improves focus and mental clarity.</li>"
        "<li>Enhances stability and balance.</li>"
        "<li>Opens the chest and hips.</li>"
        "</ul>"
    ),
    "Vrikshasana": (
        "<p>Vrikshasana, or Tree Pose, improves balance, strengthens the legs, and helps with focus. This standing pose mimics the "
        "steadiness of a tree and helps to calm the mind while improving concentration. It also helps stretch the inner thighs.</p>"
        "<p><strong>Benefits:</strong></p>"
        "<ul>"
        "<li>Improves balance and coordination.</li>"
        "<li>Strengthens the legs and core.</li>"
        "<li>Enhances focus and concentration.</li>"
        "<li>Stretches the inner thighs and hips.</li>"
        "</ul>"
    )
}




@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()  # Convert input to lowercase
    response = "I didn't understand that. Please ask about a yoga pose or give feedback."
    
    for pose in pose_info:
        if user_message in pose.lower():  # Allow matching of poses in any case
            response = pose_info[pose]
            break
        elif "feedback" in user_message:
            response = "You can provide feedback by clicking the 'Submit Feedback' button."
    
    return jsonify({"response": response})

@app.route("/feedback", methods=["POST"])
def feedback():
    user_feedback = request.json.get("feedback", "")
    if user_feedback:
        feedback_list.append(user_feedback)
        return jsonify({"message": "Thank you for your feedback!"})
    return jsonify({"message": "Feedback cannot be empty."}), 400

@app.route("/get_feedback", methods=["GET"])
def get_feedback():
    return jsonify({"feedback": feedback_list})

if __name__ == "__main__":
    app.run(debug=True)
