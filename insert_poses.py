import mysql.connector

# Database connection
con = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Swix@7466',
    database='yoga_project'
)

cursor = con.cursor()

# Yoga pose data from app for chatbot.py
pose_info = {
    "Adho Mukha Svanasana": "Adho Mukha Svanasana, or Downward Dog Pose, strengthens the arms, shoulders, and back...",
    "Anjaneyasana": "Anjaneyasana, or Low Lunge Pose, opens the hips, stretches the thighs, and strengthens the legs...",
    "Phalakasana": "Phalakasana, or Plank Pose, is a full-body strength pose that focuses on core strength...",
    "Setu Bandha Sarvangasana": "Setu Bandha Sarvangasana, or Bridge Pose, strengthens the back, glutes, and legs...",
    "Trikonasana": "Trikonasana, or Triangle Pose, stretches the legs, hips, and spine while strengthening the core...",
    "Utkatasana": "Utkatasana, or Chair Pose, strengthens the legs and core while improving endurance...",
    "Virabhadrasana 2": "Virabhadrasana 2, or Warrior II Pose, strengthens the legs, opens the hips, and improves focus...",
    "Vrikshasana": "Vrikshasana, or Tree Pose, improves balance, strengthens the legs, and helps with focus..."
}

# Insert yoga poses into the table
for pose, description in pose_info.items():
    cursor.execute("INSERT INTO pose (poseName, poseDescription) VALUES (%s, %s) ON DUPLICATE KEY UPDATE poseDescription = VALUES(poseDescription)", 
                   (pose, description))

con.commit()
cursor.close()
con.close()

print("Yoga pose data inserted successfully!")
