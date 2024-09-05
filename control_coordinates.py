import cv2
import numpy as np
import math

def main():
    # Burada büyük kod parçanız çalışacak
    pass

def get_ship_center_coordinates(ret, frame):
    # The ship is the biggest purple object in the frame
    # Returns the center (cx, cy) of the ship
    if not ret:
        print("Error: Frame not valid.")
        return 0, 0

    lower_purple = np.array([120, 50, 50])
    upper_purple = np.array([150, 255, 255])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) > 0:
        ship = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(ship)
        cx = x + w // 2  # Gemi merkezinin x koordinatı
        cy = y + h // 2  # Gemi merkezinin y koordinatı
        return cx, cy

    return 0, 0  # If no ship is found


def guide_ship_to_port(ship_cx, ship_cy, port_cx, port_cy):
    commands = []

    # Yatay eksende hareket (x koordinatı)
    if ship_cx < port_cx:
        commands.append("right")
    elif ship_cx > port_cx:
        commands.append("left")

    # Dikey eksende hareket (y koordinatı)
    if ship_cy < port_cy:
        commands.append("down")
    elif ship_cy > port_cy:
        commands.append("up")

    return commands

## Gemi hareketi için fonksiyon
def move_ship(ship_cx, ship_cy, command):
    if command == "right":
        ship_cx += 1
    elif command == "left":
        ship_cx -= 1
    elif command == "down":
        ship_cy += 1
    elif command == "up":
        ship_cy -= 1
    
    return ship_cx, ship_cy


def control_loop(ship_cx, ship_cy, port_cx, port_cy):
    while True:
        commands = guide_ship_to_port(ship_cx, ship_cy, port_cx, port_cy)
        
        for command in commands:
            # Gemiyi komuta göre hareket ettir
            new_ship_cx, new_ship_cy = move_ship(ship_cx, ship_cy, command)

            # Eğer yeni konum limana daha yakınsa, devam et
            if abs(new_ship_cx - port_cx) < abs(ship_cx - port_cx) and abs(new_ship_cy - port_cy) < abs(ship_cy - port_cy):
                ship_cx, ship_cy = new_ship_cx, new_ship_cy
            else:
                # Eğer limana yaklaşmıyorsa, yön değiştirilir
                continue
        
        # Eğer gemi limana ulaştıysa döngüden çık
        if ship_cx == port_cx and ship_cy == port_cy:
            print("Gemi limana ulaştı!")
            break

        # Simülasyon için basit bir durdurma koşulu
        if len(commands) == 0:
            print("Gemi yönünü bulamıyor!")
            break

    return ship_cx, ship_cy


    
if __name__ == "__main__":
    main()
