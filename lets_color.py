import tkinter as tk
from tkinter import colorchooser

class DrawingPad(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Interactive Drawing Pad")
        self.geometry("500x500")
        
        # Canvas for drawing
        self.canvas = tk.Canvas(self, width=500, height=400, bg="white")
        self.canvas.pack(pady=20)

        # Initial color and brush size
        self.color = "black"
        self.brush_size = 5
        
        # Create a frame for buttons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack()

        # Buttons for drawing, erasing, and clearing
        self.color_button = tk.Button(self.button_frame, text="Pick Color", command=self.pick_color)
        self.color_button.grid(row=0, column=0, padx=5)
        
        self.erase_button = tk.Button(self.button_frame, text="Erase", command=self.erase)
        self.erase_button.grid(row=0, column=1, padx=5)
        
        self.clear_button = tk.Button(self.button_frame, text="Clear All", command=self.clear_all)
        self.clear_button.grid(row=0, column=2, padx=5)
        
        # Set up drawing with the mouse
        self.previous_x = None
        self.previous_y = None
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    # Pick a color for the brush
    def pick_color(self):
        color_code = colorchooser.askcolor(title="Choose Brush Color")[1]
        if color_code:
            self.color = color_code

    # Start drawing when mouse is pressed
    def paint(self, event):
        if self.previous_x and self.previous_y:
            self.canvas.create_line(self.previous_x, self.previous_y, event.x, event.y, 
                                    width=self.brush_size, fill=self.color, capstyle=tk.ROUND, smooth=tk.TRUE)
        self.previous_x = event.x
        self.previous_y = event.y

    # Reset the previous position when mouse is released
    def reset(self, event):
        self.previous_x = None
        self.previous_y = None

    # Enable eraser tool
    def erase(self):
        self.color = "white"  # Eraser will be white
        self.brush_size = 20  # Bigger brush size for erasing

    # Clear the entire canvas
    def clear_all(self):
        self.canvas.delete("all")

# Create and run the drawing pad application
app = DrawingPad()
app.mainloop()
