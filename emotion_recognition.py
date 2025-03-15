import cv2
from fer import FER
import time

# Initialize FER for emotion detection
emotion_detector = FER(mtcnn=True)  # Use MTCNN for more accurate face detection

# Initialize webcam
cap = cv2.VideoCapture(0)

# Emotion tracking variables
emotion_data = []  # To store emotion probabilities for each frame
time_limit = 5  # Analysis window in seconds
start_time = time.time()

print("Press 'q' to exit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Detect emotions in the frame
    emotions = emotion_detector.detect_emotions(frame)

    # Process detected faces and their emotions
    frame_emotion_data = []  # To store data for the current frame
    for face in emotions:
        box = face["box"]  # Bounding box around the face
        emotion_probs = face["emotions"]  # Dictionary of emotion probabilities

        # Store emotion probabilities
        frame_emotion_data.append(emotion_probs)

        # Draw a rectangle around the face
        x, y, w, h = box
        dominant_emotion = max(emotion_probs, key=emotion_probs.get)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Annotate with the dominant emotion
        cv2.putText(frame, f"{dominant_emotion} ({int(emotion_probs[dominant_emotion]*100)}%)",
                    (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Add current frame emotions to tracking
    if frame_emotion_data:
        emotion_data.append(frame_emotion_data)

    # Show the video feed with annotations
    cv2.imshow('Emotion Recognition', frame)

    # Check if one minute has passed and calculate general emotional state
    if time.time() - start_time >= time_limit:
        # Calculate general emotional state
        aggregated_emotions = {emotion: 0 for emotion in emotions[0]["emotions"]}
        frame_count = len(emotion_data)

        for frame in emotion_data:
            for face_probs in frame:
                for emotion, prob in face_probs.items():
                    aggregated_emotions[emotion] += prob

        # Compute the average probabilities
        average_emotions = {emotion: prob / frame_count for emotion, prob in aggregated_emotions.items()}

        # Find the dominant emotion
        dominant_emotion = max(average_emotions, key=average_emotions.get)
        print("\nGeneral Emotional State:")
        for emotion, prob in average_emotions.items():
            print(f"{emotion}: {prob*100:.2f}%")
        print(f"Dominant Emotion: {dominant_emotion}")

        # Reset for the next one-minute analysis to make it a continuous emotional assessment
        emotion_data = []
        start_time = time.time()

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
