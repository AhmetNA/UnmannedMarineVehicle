import cv2
import numpy as np
import tkinter as tk
from tkinter import LabelFrame, messagebox
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime

# Tkinter main window
master = tk.Tk()

# Initial window dimensions
canvas_width = 1000
canvas_height = 450
panel_width = 150
panel_height = 250
panel_margin = 10
top_margin = 20

# Tkinter main window
master.title("Camera and Data Reading Application")

# Create Canvas
canvas = tk.Canvas(master, width=canvas_width, height=canvas_height)
canvas.pack()

def label_frame_creation(master, text, relx, rely, relwidth, relheight):
    label_frame = LabelFrame(master, text=text)
    label_frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return label_frame

# Data Panel (camera image will be here)
label_frame_data = label_frame_creation(master, "Data", 0.04, top_margin / canvas_height, 0.5, 0.65)

# Tool Panel (for another example)
label_frame_tool = label_frame_creation(master, "Tool", 0.6, 0.04, 0.34, 0.1)
label_tool = tk.Label(label_frame_tool, text="tool name is temporarily left blank")
label_tool.pack(padx=15, pady=5, anchor=tk.NW)

# Result Panel (data will be displayed here)
label_frame_result = label_frame_creation(master, "Result", 0.6, 0.2, 0.35, 0.5)

# Function Panel
label_frame_function = label_frame_creation(master, "Function", 0.6, 0.6, 0.35, 0.3)

# Camera start button
def btnCamera():
    start_video_capture()

# Other button functions    
def btnBatma():
    messagebox.showinfo("Information", "Batma button clicked")    
def btnCikma():
    messagebox.showinfo("Information", "Cikma button clicked")

def btnSag():
    messagebox.showinfo("Information", "Sag button clicked")

def btnSol():
    messagebox.showinfo("Information", "Sol button clicked")

def btnIleri():
    messagebox.showinfo("Information", "Ileri button clicked")

def btnGeri():
    messagebox.showinfo("Information", "Geri button clicked")

def btnReset():
    messagebox.showinfo("Information", "Reset button clicked")

def btnArm():
    messagebox.showinfo("Information", "Arm button clicked")

def btnDisarm():
    messagebox.showinfo("Information", "Disarm button clicked")

def btnStabilize():
    messagebox.showinfo("Information", "Stabilize button clicked")

def btnAuto():
    messagebox.showinfo("Information", "Auto button clicked")

# Placing buttons
button_texts = ["Batma", "Cikma", "Sag", "Sol", "Ileri", "Geri", "Camera", "Reset", "Arm", "Disarm", "Stabilize", "Auto"]
button_functions = [btnBatma, btnCikma, btnSag, btnSol, btnIleri, btnGeri, btnCamera, btnReset, btnArm, btnDisarm, btnStabilize, btnAuto]

for i, text in enumerate(button_texts):
    row, column = divmod(i, 2)
    button = tk.Button(label_frame_function, text=text, width=10, height=1, background='White', command=button_functions[i])
    button.grid(row=row, column=column, padx=40, pady=3)

# Function to write data to the result panel
def update_result_panel(text):
    for widget in label_frame_result.winfo_children():
        widget.destroy()
    label = tk.Label(label_frame_result, text=text)
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

    centers_sorted = sorted(centers, key=lambda c: c[1])[:2]  # En büyük iki merkezi bul

    # En büyük iki merkez arasında çizgi çiz
    if len(centers_sorted) == 2:
        cv2.line(frame, centers_sorted[0], centers_sorted[1], color, 2)

        # İki merkez arasındaki ortalama noktayı bul
        midpoint = ((centers_sorted[0][0] + centers_sorted[0][1]) // 2,
                    (centers_sorted[1][0] + centers_sorted[1][1]) // 2)

        # Ortaya yatay siyah çizgi çiz
        cv2.line(frame, (0, midpoint[1]), (frame.shape[1], midpoint[1]), (0, 0, 0), 5)

    # Merkezlerin etrafına yuvarlak çiz
    for center in centers:
        cv2.circle(frame, center, 5, color, -1)

    return centers_sorted

def start_video_capture():
    label_data = tk.Label(label_frame_data)
    label_data.pack()

    def video_thread():
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            messagebox.showerror("Error", "Camera not found or could not be opened!")
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
                
                # Red color mask
                lower_red1 = np.array([0, 120, 70])
                upper_red1 = np.array([10, 255, 255])
                mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
                lower_red2 = np.array([170, 120, 70])
                upper_red2 = np.array([180, 255, 255])
                mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
                mask_red = mask_red1 + mask_red2

                # Green color mask
                lower_green = np.array([36, 100, 100])
                upper_green = np.array([86, 255, 255])
                mask_green = cv2.inRange(hsv, lower_green, upper_green)

                # Find red centers and draw lines
                red_centers = max_contour_center(mask_red, (0, 0, 255), frame)

                # Find green centers and draw lines
                green_centers = max_contour_center(mask_green, (0, 255, 0), frame)

                # Draw a black line between the centers if both are found
                if len(red_centers) == 2 and len(green_centers) == 2:
                    mid_point_red = ((red_centers[0][0] + red_centers[1][0]) // 2, (red_centers[0][1] + red_centers[1][1]) // 2)
                    mid_point_green = ((green_centers[0][0] + green_centers[1][0]) // 2, (green_centers[0][1] + green_centers[1][1]) // 2)
                    cv2.line(frame, mid_point_red, mid_point_green, (0, 0, 0), 5)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(img)

                def update_gui():
                    label_data.imgtk = imgtk
                    label_data.config(image=imgtk)

                master.after(0, update_gui)
                out.write(frame)

            else:
                break

            time.sleep(0.05)  # Small delay between frame updates

        cap.release()
        out.release()

    threading.Thread(target=video_thread, daemon=True).start()

# Tkinter main loop
master.mainloop()
