# .------------------------------------------- [INSTALL COMMAND LINE] -----------------------------------------. #
# | pyinstaller --noconfirm --noconsole --onefile --hide-console="hide-early" --hidden-import=tkinter main.pyw | #          
# '------------------------------------------------------------------------------------------------------------' #




# .------------------------------------- [ PROGRAM CONSTANTS ] -------------------------------------------. #

TEST_MODE = False
actualTime = 4.0  # Entering the time in general for the splash screen    (in min)  [Default: 4.5 minutes]

# '-------------------------------------------------------------------------------------------------------' #




import psutil
import subprocess
import pynput
import ctypes
import darkdetect
import tkinter
import customtkinter as tk
from PIL import Image, ImageTk, ImageFilter, ImageDraw, ImageFont

image = Image.open("image.jpg")
pilImage1 = image.filter(ImageFilter.GaussianBlur(radius = 50))
pilImage2 = image.filter(ImageFilter.GaussianBlur(radius = 50))

draw = ImageDraw.Draw(pilImage1)
font1 = ImageFont.truetype("Segoe.woff", 64)
font2 = ImageFont.truetype("Segoe.woff", 28)

draw.text((1850, 990), "Please wait . . .", font = font1, fill = "white")
draw.text((1650, 1090), "Getting your desktop ready", font = font1, fill = "white")
draw.text((1860, 1250), "Estimated time: " + str(actualTime) + " minutes", font = font2, fill = "white")

drawDone = ImageDraw.Draw(pilImage2)
drawDone.text((1820, 1100), "Almost done . . .", font = font1, fill = "white")

timeScreen = int(actualTime * 60000)           # Time after which loading Screen will destroy itself   (in ms)   [Default: 270000 (4 minutes and 30 seconds)]
timeInSec = int(actualTime * 60)               # Displays Timer on loading Screen                      (in s)    [Default: 270 (4 minutes and 30 seconds)]
timeDestroyLoad = int(timeScreen - 15000)      # Time after which Image Screen will destroy itself     (in ms)   [Default: 255000 (4 minutes and 15 seconds)]

root = tkinter.Tk()
win = tkinter.Toplevel(root)
done = tkinter.Toplevel(root)
loadBar = tkinter.Toplevel(root)

w, h = root.winfo_screenwidth(), root.winfo_screenheight()




keyboard_listener = pynput.keyboard.Listener(suppress = True)

# Disable all keyboard keys.
def block(check):
    if (check == False):
        keyboard_listener.start()
    else:
        return 0




# Enbale all keyboard keys.
def unblock(check):
    if (check == False):
        keyboard_listener.stop()
    else:
        return 0




# Progress bar on the screen.
def progress():
    progressbar_height = 10

    if darkdetect.isDark():
        color = "#56556D"
    else:
        color = "#FFFFFF"

    result = "#56556E" if darkdetect.isDark() else "#FDFDFD"

    loadBar.geometry(f"400x{progressbar_height}+754+566")
    loadBar.overrideredirect(1)
    loadBar.focus_force()
    loadBar.focus_set()
    loadBar.grab_set_global()

    loadBar.config(background = result)
    loadBar.attributes("-transparentcolor", result)
    
    progressbar = tk.CTkProgressBar(
        master = loadBar,
        mode = "indeterminate",
        width = 408.5,
        height = progressbar_height,
        corner_radius = 15,
        border_width = 1,
        progress_color = "#1E95E5",
        border_color = color,
        fg_color = color,
        orientation = "horizontal",
        indeterminate_speed = 0.5,
    )

    progressbar.set(0)
    progressbar.start()
    progressbar.pack()
    loadBar.after(timeScreen + 500, lambda: progressbar.destroy())

    loadBar.mainloop()




# Image resizer to fix size issue of the background.
def fix_Image(fix_img):
    imgWidth, imgHeight = fix_img.size

    if imgWidth > w or imgHeight > h:
        ratio = min(w / imgWidth, h / imgHeight)
        imgWidth = int(imgWidth * ratio)
        imgHeight = int(imgHeight * ratio)
        fix_img = fix_img.resize((imgWidth, imgHeight))

    return fix_img




# Show final image with ending screen of the program.
def showDonePIL(doneimage):
    done.overrideredirect(1)
    done.geometry("%dx%d+-2+-2" % (w + 4, h + 4))

    canvasLoad = tkinter.Canvas(done, width = w, height = h)
    canvasLoad.pack()
    canvasLoad.configure(background = "black")

    image = ImageTk.PhotoImage(fix_Image(doneimage))
    canvasLoad.create_image(w / 2, h / 2, image = image)

    done.grab_set_global()
    win.grab_set_global()

    done.after(1000, lambda: (done.focus_force(), done.focus_set(), done.wm_attributes("-topmost", 1)))
    loadBar.after(1000, lambda: loadBar.wm_attributes("-topmost", 1))

    done.mainloop()




# Main function where all the thinks are being done on the desktop.
def showPIL(pilImage):
    root.overrideredirect(1)
    root.geometry("%dx%d+-2+-2" % (w + 4, h + 4))
    root.focus_force()
    root.focus_set()

    canvas = tkinter.Canvas(root, width = w, height = h)
    canvas.pack()
    canvas.configure(background = "black")

    image = ImageTk.PhotoImage(fix_Image(pilImage))
    canvas.create_image(w / 2, h / 2, image = image)
    
    def Count(Number):
        if Number == -1:
            win.withdraw()
        else:
            NumberLabel["text"] = Number
            win.after(1000, Count, Number - 1)

    win.geometry("+%d+%d" % (2, 2))
    win.overrideredirect(1)
    win.focus_force()
    win.focus_set()
    win.grab_set_global()
    win.wm_attributes("-transparentcolor", win["bg"])

    NumberLabel = tkinter.Label(win, font = (font1, 8), fg = win["bg"])
    NumberLabel.pack()

    win.bind_all("<Button-1>", lambda e: NumberLabel.configure(fg = "white"))
    win.bind_all("<ButtonRelease-1>", lambda e: NumberLabel.configure(fg = win["bg"]))

    win.after(0, lambda: block(TEST_MODE))
    win.after(0, lambda: (Count(timeInSec)))

    root.after(100, lambda: root.wm_attributes("-topmost", 1))
    win.after(105, lambda: win.wm_attributes("-topmost", 1))
    loadBar.after(110, lambda: loadBar.wm_attributes("-topmost", 1))

    root.after(timeDestroyLoad + 1000, lambda: showDonePIL(pilImage2))

    def changeCanvas():
        canvas.delete("all")
        canvas.img = tkinter.PhotoImage(pilImage2)

    win.after(timeScreen - 2000, lambda: changeCanvas())
    win.after(timeScreen + 2990, lambda: unblock(TEST_MODE))
    win.after(timeScreen + 3000, lambda: root.destroy())

    progress()

    root.mainloop()
    win.mainloop()




# Used for testing the prorgram.
def Exit(check):
    if (check == True): 
        done.bind_all("<Escape>", lambda e: e.widget.quit())
        win.bind_all("<Escape>", lambda e: (win.withdraw(), e.widget.quit()))
        root.bind_all("<Escape>", lambda e: e.widget.quit())
    else:
        return 0

Exit(TEST_MODE)




# .------------------------------. #
# |                              | #
# |   CALLING THE MAIN PROGRAM   | #
# |                              | #
# '------------------------------' #

# Main function to execute the program if the system has just booted else exit.
def MAIN_CHECK(check):
    lib = ctypes.windll.kernel32
    t = lib.GetTickCount64()
    t = int(str(t)[:-3])

    # Function to check if a process is running or not.
    def is_not_process_running(process_name):
        for proc in psutil.process_iter(["name"]):
            try:
                if process_name.lower() in proc.info["name"].lower():
                    return False
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return True

    # Function to call the userinit system file to start the logon process.
    def call():
        subprocess.Popen("C:\\Windows\\System32\\userinit.exe", creationflags = subprocess.CREATE_NO_WINDOW)

    if check == False:
        if t < 160 and is_not_process_running("userinit.exe") and is_not_process_running("explorer.exe"):
            call()
            showPIL(pilImage1)
        else:
            call()
    else:
        showPIL(pilImage1)
    
    return 1

MAIN_CHECK(TEST_MODE)