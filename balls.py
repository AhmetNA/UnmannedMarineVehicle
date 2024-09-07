import cv2
import pytesseract

# Tesseract'a giden yolu belirt
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def balls():
    ...

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Görüntüdeki 1, 2 ve 3 rakamlarını ve konumlarını oku
        birler, ikiler, ucler = balls(frame)
        
        # Tespit edilen rakamların etrafına dikdörtgen çiz ve rakamı ekrana yazdır
        for (x, y, w, h) in birler:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, '1', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            print(f"Rakam: 1, Konum: ({x}, {y})")
        
        for (x, y, w, h) in ikiler:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, '2', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            print(f"Rakam: 2, Konum: ({x}, {y})")
        
        for (x, y, w, h) in ucler:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, '3', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            print(f"Rakam: 3, Konum: ({x}, {y})")

        # Görüntüyü ekranda göster
        cv2.imshow('Kamera', frame)

        # Çıkmak için 'q' tuşuna basın
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kaynakları serbest bırak
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
