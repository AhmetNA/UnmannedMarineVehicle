import cv2
import numpy as np

# Kamera nesnesini başlat
cap = cv2.VideoCapture(0)

while True:
    # Kameradan bir kare al
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Görüntüyü HSV renk alanına çevir
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Renk aralıklarını belirle
    # Kırmızı renk için
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = mask_red1 + mask_red2

    # Yeşil renk için
    lower_green = np.array([36, 100, 100])
    upper_green = np.array([86, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Sarı renk için
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Maskeleri uygula
    red_output = cv2.bitwise_and(frame, frame, mask=mask_red)
    green_output = cv2.bitwise_and(frame, frame, mask=mask_green)
    yellow_output = cv2.bitwise_and(frame, frame, mask=mask_yellow)
    
    # Renk yoğunluklarını hesapla
    red_intensity = cv2.countNonZero(mask_red)
    green_intensity = cv2.countNonZero(mask_green)
    yellow_intensity = cv2.countNonZero(mask_yellow)
    
    # En büyük alanların piksel sayısını bul
    def max_contour_area(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            return max(cv2.contourArea(contour) for contour in contours)
        return 0
    
    max_red_area = max_contour_area(mask_red)
    max_green_area = max_contour_area(mask_green)
    max_yellow_area = max_contour_area(mask_yellow)
    
    # Yoğunlukları yazdır
    if max_red_area > 1000:
        print('Kırmızı')
    elif max_green_area > 1000:
        print('Yeşil')
    elif max_yellow_area > 1000:
        print('Sarı')
    else:
        print('Renk Yok')    
    # Sonuçları göster
    cv2.imshow('Frame', frame)
    cv2.imshow('Red Mask', red_output)
    cv2.imshow('Green Mask', green_output)
    cv2.imshow('Yellow Mask', yellow_output)
    
    # Çıkmak için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
