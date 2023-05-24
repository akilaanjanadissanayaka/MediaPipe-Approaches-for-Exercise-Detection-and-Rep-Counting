import cv2
import mediapipe as md
md_drawing=md.solutions.drawing_utils
md_drawing_styles=md.solutions.drawing_styles
md_pose=md.solutions.pose

count = 0
position=None
# cap =cv2.VideoCapture (0)
cap = cv2.VideoCapture("sample\push-up_10.mp4")  # For Video
cap.set(3, 500)
cap.set(4, 500)

# Create a named window
cv2.namedWindow("Video", cv2.WINDOW_NORMAL)

# Resize the window size
cv2.resizeWindow("Video", 400, 400)  # Set the desired window size

with md_pose.Pose(min_detection_confidence=0.7,min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        success, image=cap.read()
        if not success:
            print("end with ",count," reps")
            break
        image=cv2.cvtColor (cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        result=pose.process (image)

        imlist=[]

        if result.pose_landmarks:
            md_drawing.draw_landmarks(image, result.pose_landmarks, md_pose. POSE_CONNECTIONS)
            for id,im in enumerate (result.pose_landmarks.landmark):
                h,w,_=image.shape
                X,Y=int (im.x*w), int(im.y*h)
                imlist.append([id,X,Y])

        if len(imlist)!=0:
            if (imlist[12][2] and imlist[11][2] >= imlist[14][2] and imlist[13][2]):
                position = "down"
            if (imlist[12][2] and imlist[11][2] <= imlist[14][2] and imlist[13][2] and position == "down"):
                position = "up"
                count += 1
                print(count)
        cv2.putText(image, "Reps: " + str(count), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Push-up counter",image)
        # flipped_frame = cv2.flip(frame, 1)  # Flip the frame horizontally
        # cv2.imshow("Video", flipped_frame)

        key=cv2.waitKey(1)
        if key==ord('q'):
            break
cap.release()

