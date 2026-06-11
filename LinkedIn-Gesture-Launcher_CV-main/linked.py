# ===============================
# فتح لينكدإن عند عمل إشارة لايك 👋
# ===============================

import cv2
from cvzone.HandTrackingModule import HandDetector
import webbrowser
import time

# ===== إعدادات أساسية =====
LINKEDIN_URL = "https://www.linkedin.com/in/abdelkreem-frahat-160g/"  # ضع لينك لينكدإن بتاعك هنا
DETECTION_FRAMES_REQUIRED = 8   # عدد الفريمات المطلوبة لتأكيد الإشارة
COOLDOWN_SECONDS = 5             # فترة الانتظار قبل فتح لينك تاني

# ===== تفعيل الكاميرا وكاشف اليد =====
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1, detectionCon=0.7)
detected_frames = 0
last_action_time = 0

print("📸 افتح الكاميرا، وارفع إيدك بإشارة 👍 علشان يفتح لينكدإن.")

try:
    while True:
        success, img = cap.read()
        if not success:
            break

        hands, img = detector.findHands(img, flipType=True)

        gesture_like = False

        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)  # [thumb, index, middle, ring, pinky]

            print("🖐️ Fingers status:", fingers)  # دي بتطبع حالة كل صباع
            if fingers == [1, 0, 0, 0, 0]:
             print("👍 Detected Like gesture!")
             gesture_like = True
            else:
             gesture_like = False


        # التحقق من عدد الفريمات المتتالية اللي فيها لايك
        if gesture_like:
            detected_frames += 1
        else:
            detected_frames = 0

        if detected_frames >= DETECTION_FRAMES_REQUIRED:
            now = time.time()
            if now - last_action_time > COOLDOWN_SECONDS:
                print("✅ تم التعرف على الإشارة 👍 — فتح لينكدإن ...")
                webbrowser.open(LINKEDIN_URL)
                last_action_time = now
            detected_frames = 0

        # عرض الحالة على الشاشة
        cv2.putText(img, f"Like frames: {detected_frames}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("👍 Like to Open LinkedIn (press q to quit)", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
