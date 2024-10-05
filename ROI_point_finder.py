import pyautogui
from tkinter import Tk, Canvas
from PIL import Image, ImageTk

def get_screen_rect():
    screen = pyautogui.screenshot()
    return screen

def on_click(event):
    global roi_start_x, roi_start_y, drawing
    roi_start_x, roi_start_y = event.x, event.y
    drawing = True

def on_drag(event):
    if drawing:
        canvas.delete("rect")
        canvas.create_rectangle(roi_start_x, roi_start_y, event.x, event.y, outline="green", width=2, tags="rect")

def on_release(event):
    global roi_end_x, roi_end_y, drawing
    roi_end_x, roi_end_y = event.x, event.y
    drawing = False
    print(f"ROI_START_POINT: {roi_start_x}, {roi_start_y}")
    print(f"ROI_END_POINT: {roi_end_x}, {roi_end_y}")
    root.destroy()

# Setup tkinter window
root = Tk()
root.title("Select ROI")
screen_img = get_screen_rect()
screen_img = ImageTk.PhotoImage(screen_img)
canvas = Canvas(root, width=screen_img.width(), height=screen_img.height())
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=screen_img)
canvas.bind("<Button-1>", on_click)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)

drawing = False
roi_start_x = roi_start_y = roi_end_x = roi_end_y = 0

root.mainloop()
