from google.colab import files

# Upload the video file on colab
uploaded = files.upload()


from ultralytics import YOLO
import cv2
import math

# Video path
video_path = 'People_walking.mp4'
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
else:
    # Get video frame dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Load YOLO model (verbose mode off to reduce the amount of output printed)
    model = YOLO("yolo-Weights/yolov8n.pt", verbose=False)

    # Class ID for "person" in YOLO model
    person_class_id = 0  

    # Video writer to save the result
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output_people_detection.mp4', fourcc, 20.0, (width, height))

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break

        # Run YOLO model on the current frame
        results = model(img, stream=True)

        for r in results:
            boxes = r.boxes

            for box in boxes:
                # Check if the detected object is a person
                cls = int(box.cls[0])
                if cls == person_class_id:
                    # Bounding box coordinates
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Draw bounding box on people
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    # Display confidence and class_name
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    label = f'Person: {confidence}'

                    # Display label on the video
                    org = (x1, y1 - 10)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    fontScale = 0.5
                    color = (255, 0, 0)
                    thickness = 2
                    cv2.putText(img, label, org, font, fontScale, color, thickness)

        # Write the frame to the output video
        out.write(img)

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Download the output from colab
    from google.colab import files
    files.download('output_people_detection.mp4')