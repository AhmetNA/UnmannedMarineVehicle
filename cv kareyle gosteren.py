import cv2
import numpy as np
import tkinter as tk
from tkinter import LabelFrame, messagebox
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime

# Tkinter ana penceresi
master = tk.Tk()

# Başlangıç penceresi boyutları
canvas_genislik = 1000
canvas_yukseklik = 450
panel_genislik = 150
panel_yukseklik = 250
panel_margin = 10
top_margin = 20

# Tkinter ana penceresi
master.title("Kamera ve Veri Okuma Uygulamasi")

# Kanvas oluşturma
canvas = tk.Canvas(master, width=canvas_genislik, height=canvas_yukseklik)
canvas.pack()

def label_frame_olusturma(master, text, relx, rely, relwidth, relheight):
    label_frame = LabelFrame(master, text=text)
    label_frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return label_frame

# Veri Paneli (Kamera görüntüsü burada olacak)
label_frame_veri = label_frame_olusturma(master, "Veri", 0.04, top_margin / canvas_yukseklik, 0.5, 0.65)

# Araç Paneli (başka bir örnek için)
label_frame_arac = label_frame_olusturma(master, "Araç", 0.6, 0.04, 0.34, 0.1)
label_arac = tk.Label(label_frame_arac, text="arac ismi icin simdilik bos birakilmistir")
label_arac.pack(padx=15, pady=5, anchor=tk.NW)

# Sonuç Paneli (veriler burada gösterilecek)
label_frame_sonuc = label_frame_olusturma(master, "Sonuç", 0.6, 0.2, 0.35, 0.5)

# Fonksiyon Paneli
label_frame_fonksiyon = label_frame_olusturma(master, "Fonksiyon", 0.6, 0.6, 0.35, 0.3)

# Kamera açma butonu
def btnCamera():
    start_video_capture()

# Diğer buton fonksiyonları    
def btnBatma():
    messagebox.showinfo("Bilgi", "Batma butonuna tikandi")    
def btnCikma():
    messagebox.showinfo("Bilgi", "Çıkma butonuna tıklandı")

def btnSag():
    messagebox.showinfo("Bilgi", "Sağ butonuna tıklandı")

def btnSol():
    messagebox.showinfo("Bilgi", "Sol butonuna tıklandı")

def btnIleri():
    messagebox.showinfo("Bilgi", "İleri butonuna tıklandı")

def btnGeri():
    messagebox.showinfo("Bilgi", "Geri butonuna tıklandı")

def btnReset():
    messagebox.showinfo("Bilgi", "Reset butonuna tıklandı")

def btnArm():
    messagebox.showinfo("Bilgi", "Arm butonuna tıklandı")

def btnDisarm():
    messagebox.showinfo("Bilgi", "Disarm butonuna tıklandı")

def btnStabilize():
    messagebox.showinfo("Bilgi", "Stabilize butonuna tıklandı")

def btnAuto():
    messagebox.showinfo("Bilgi", "Auto butonuna tıklandı")

# Butonları yerleştirme
buton_metinleri = ["Batma", "Çıkma", "Sağ", "Sol", "İleri", "Geri", "Kamera", "Reset", "Arm", "Disarm", "Stabilize", "Auto"]
buton_fonksiyonlari = [btnBatma, btnCikma, btnSag, btnSol, btnIleri, btnGeri, btnCamera, btnReset, btnArm, btnDisarm, btnStabilize, btnAuto]


for i, metin in enumerate(buton_metinleri):
    row, column = divmod(i, 2)
    buton = tk.Button(label_frame_fonksiyon, text=metin, width=10, height=1, background='White', command=buton_fonksiyonlari[i])
    buton.grid(row=row, column=column, padx=40, pady=3)

# Sonuç paneline veri yazdırmak için fonksiyon
def update_sonuc_panel(text):
    for widget in label_frame_sonuc.winfo_children():
        widget.destroy()
    label = tk.Label(label_frame_sonuc, text=text)
    label.pack()

def max_contour_center(mask, color, frame):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centers.append((cx, cy))

    centers_sorted = sorted(centers, key=lambda c: c[0])[:2]  # En büyük iki merkezi bul

    # En büyük iki merkez arasında çizgi çiz
    if len(centers_sorted) == 2:
        cv2.line(frame, centers_sorted[0], centers_sorted[1], color, 2)

        # İki merkez arasında siyah çizgi çiz
        cv2.line(frame, centers_sorted[0], centers_sorted[1], (0, 0, 0), 5)

    # Merkezlerin etrafına yuvarlak çiz
    for center in centers:
        cv2.circle(frame, center, 5, color, -1)

    return centers_sorted


def start_video_capture():
    label_veri = tk.Label(label_frame_veri)
    label_veri.pack()

    def video_thread():
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messagebox.showerror("Hata", "Kamera bulunamadi veya acilamadi!")
            return

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        video_filename = f"Akriha_Control_{now}.avi"
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                # Kırmızı renk için maske
                lower_red1 = np.array([0, 120, 70])
                upper_red1 = np.array([10, 255, 255])
                mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
                lower_red2 = np.array([170, 120, 70])
                upper_red2 = np.array([180, 255, 255])
                mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
                mask_red = mask_red1 + mask_red2

                # Yeşil renk için maske
                lower_green = np.array([36, 100, 100])
                upper_green = np.array([86, 255, 255])
                mask_green = cv2.inRange(hsv, lower_green, upper_green)

                # Kırmızı merkezleri bul ve çizgi çiz
                red_centers = max_contour_center(mask_red, (0, 0, 255), frame)

                # Yeşil merkezleri bul ve çizgi çiz
                green_centers = max_contour_center(mask_green, (0, 255, 0), frame)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(img)

                def update_gui():
                    label_veri.imgtk = imgtk
                    label_veri.config(image=imgtk)

                master.after(0, update_gui)
                out.write(frame)

            else:
                break

            time.sleep(0.05)  # Görüntü güncellemeleri arasında küçük bir bekleme süresi

        cap.release()
        out.release()

    threading.Thread(target=video_thread, daemon=True).start()

# Tkinter ana döngüsü
master.mainloop()
