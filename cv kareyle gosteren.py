import cv2
import numpy as np

# Kamera başlatma
cap = cv2.VideoCapture(0)

def renk_tespiti(frame, lower_color, upper_color):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    return mask

def kontur_bul(mask, min_area):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    second_max_area = 0
    max_center = None
    second_max_center = None

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            M = cv2.moments(contour)
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                if area > max_area:
                    second_max_area = max_area
                    second_max_center = max_center
                    max_area = area
                    max_center = (cX, cY)
                elif area > second_max_area:
                    second_max_area = area
                    second_max_center = (cX, cY)

    return max_center, second_max_center

lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])
lower_green = np.array([40, 40, 40])
upper_green = np.array([70, 255, 255])

min_red_area = 300  # Kontur alanı için minimum değer
min_green_area = 300  # Kontur alanı için minimum değer

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Kamera görüntüsü alınamadı!")
        break

    # Kırmızı ve yeşil topları tespit et
    red_mask = renk_tespiti(frame, lower_red, upper_red)
    green_mask = renk_tespiti(frame, lower_green, upper_green)

    # Topların merkez noktalarını bul (belirli bir alan sınırıyla)
    max_center_red, second_max_center_red = kontur_bul(red_mask, min_red_area)
    max_center_green, second_max_center_green = kontur_bul(green_mask, min_green_area)  

    # Eğer kırmızı ve yeşil toplar bulunamazsa devam et
    if not max_center_red or not max_center_green:
        continue

    # En büyük kırmızı ve yeşil konturlar arasındaki orta noktayı bul
    mid_way_max = ((max_center_red[0] + max_center_green[0]) // 2, (max_center_red[1] + max_center_green[1]) // 2)
    # İkinci en büyük kırmızı ve yeşil konturlar arasındaki orta noktayı bul
    if second_max_center_red and second_max_center_green:
        mid_way_second_max = ((second_max_center_red[0] + second_max_center_green[0]) // 2, (second_max_center_red[1] + second_max_center_green[1]) // 2)
    else:
        mid_way_second_max = None

    # Rota çizimi için noktaları birleştir
    if mid_way_second_max:
        route_points = [mid_way_max, mid_way_second_max]
        cv2.line(frame, route_points[0], route_points[1], (0, 255, 0), 2)
    else:
        route_points = [mid_way_max]

    # Tüm merkez noktalarını ve rotayı çiz
    for center in [max_center_red, second_max_center_red, max_center_green, second_max_center_green]:
        if center:
            cv2.circle(frame, center, 5, (255, 0, 0), -1)
    
    if mid_way_second_max:
        cv2.circle(frame, mid_way_second_max, 5, (0, 255, 255), -1)
    cv2.circle(frame, mid_way_max, 5, (0, 255, 0), -1)

    # Sonuçları göster
    cv2.imshow("Frame", frame)

    # Çıkış için 'q' tuşuna bas
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()
