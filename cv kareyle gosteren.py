import cv2
import numpy as np

# Kamerayı başlat
cap = cv2.VideoCapture(0)

while True:
    # Kameradan bir kare oku
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Görüntüyü HSV renk alanına çevir
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Kırmızı renk için maske oluştur
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = mask_red1 + mask_red2

    # Yeşil renk için maske oluştur
    lower_green = np.array([36, 100, 100])
    upper_green = np.array([86, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Sarı renk için maske oluştur
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Kırmızı nesneleri tespit et ve işaretle
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_red:
        area = cv2.contourArea(contour)
        if area > 500:  # Minimum alan filtresi
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # Yeşil nesneleri tespit et ve işaretle
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_green:
        area = cv2.contourArea(contour)
        if area > 500:  # Minimum alan filtresi
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Sarı nesneleri tespit et ve işaretle
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours_yellow:
        area = cv2.contourArea(contour)
        if area > 500:  # Minimum alan filtresi
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
    
    # Sonuçları göster
    cv2.imshow('Frame', frame)
    
    # Çıkmak için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
