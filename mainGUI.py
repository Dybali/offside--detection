import time
import tkinter as tk
from tkinter import PhotoImage, filedialog
from PIL import ImageTk, Image, ImageEnhance
from tkinter import Canvas, Label
import os
from PIL import Image, ImageTk, ImageEnhance
from tkinter import font
from offside import drawOffside
from model.sportsfield_release.calculateHomography import calculateOptimHomography
from model.teamClassification.team_classification import team_classification
import time

# Function to reduce the brightness of an image by a given factor
def reduce_brightness(image, factor=0.7):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

# Function to open a file dialog for selecting an image
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        preprocessing_settings(file_path)

# Function to display the processed image with offside information
def display_image(file_path, team, dictPlayers, colors):
    # Set the background image for the canvas
    background = Image.open("GUI/src/images/result.jpg")
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)
    
    # Calculate the homography for the selected image
    homography = calculateOptimHomography(file_path)
    
    # Draw offside lines based on the homography and team information
    if 'goalkeeper' in dictPlayers.keys():
        if team != "A":
            offside = drawOffside(file_path, team, colors, homography, dictPlayers['Team A'], dictPlayers['Team B'], dictPlayers['goalkeeper'])
        else:
            offside = drawOffside(file_path, team, colors, homography, dictPlayers['Team B'], dictPlayers['Team A'], dictPlayers['goalkeeper'])
    else:
        if team != "A":
            offside = drawOffside(file_path, team, colors, homography, dictPlayers['Team A'], dictPlayers['Team B'])
        else:
            offside = drawOffside(file_path, team, colors, homography, dictPlayers['Team B'], dictPlayers['Team A'])

    # Display the 3D result image
    img = Image.open('result/result3D.jpg')
    img = img.resize((753, 424))
    img = ImageTk.PhotoImage(img)
    canvas.img = img
    canvas.create_image(0, 159, anchor=tk.NW, image=img)
    
    # Display the 2D result image
    img2 = Image.open("result/result2D.png")
    x = 1050
    y = 680
    res = 2.4
    img2 = img2.resize((int(x/res), int(y/res)))
    img2 = ImageTk.PhotoImage(img2)
    canvas.img2 = img2
    canvas.create_image(810, 168, anchor=tk.NW, image=img2)

    # Load and display the restart button image
    restart_button_img = Image.open("GUI/src/elements/restart_button.png")
    restart_button_img_resized = restart_button_img.resize((200, 50))
    restart_button_photo = ImageTk.PhotoImage(restart_button_img_resized)
    canvas.restart_button = restart_button_photo
    canvas.restart_button_img = restart_button_img_resized
    
    restart_button = canvas.create_image(640, 650, image=restart_button_photo)

    # Bind the restart button click event to the start_view function
    canvas.tag_bind(restart_button, '<Button-1>', lambda event: start_view())
    
    # Function to handle mouse enter event on the restart button
    def on_enter_restart(event):
        brightened_image = reduce_brightness(canvas.restart_button_img)
        brightened_photo = ImageTk.PhotoImage(brightened_image)
        canvas.itemconfig(restart_button, image=brightened_photo)
        canvas.current_button_image = brightened_photo

    # Function to handle mouse leave event on the restart button
    def on_leave_restart(event):
        canvas.itemconfig(restart_button, image=canvas.restart_button)

    # Bind the mouse enter and leave events to the respective handlers
    canvas.tag_bind(restart_button, '<Enter>', on_enter_restart)
    canvas.tag_bind(restart_button, '<Leave>', on_leave_restart)

    # Display the offside result based on the returned offside value
    if offside == 0:
        players_button_img = Image.open(f"GUI/src/images/no_offside.png")
    else:
        players_button_img = Image.open(f"GUI/src/images/{offside}.png")

    players_button_photo = ImageTk.PhotoImage(players_button_img)
    canvas.players_button = players_button_photo
    canvas.players_button_img = players_button_img   
    canvas.create_image(1140, 530, image=players_button_photo)

    # Display the team button image
    team_button_img = Image.open(f"GUI/src/images/{team}.png")
    team_button_photo = ImageTk.PhotoImage(team_button_img)
    canvas.team_button = team_button_photo
    canvas.team_button_img = team_button_img
    
    canvas.create_image(900, 530, image=team_button_photo)

# Function to display the loading screen
def loading_screen(file_path, team, dictPlayers, colors):
    canvas.delete("all")
    background = Image.open('GUI/src/images/waiting.jpg')
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)

    # Schedule the display_image function to run after a short delay
    root.after(10, display_image, file_path, team, dictPlayers, colors)

# Function to display the start view with the start button
def start_view():
    # Remove existing labels if any
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            if widget["text"].startswith("Team ") or widget["text"].startswith("Giocatori "):
                widget.destroy()

    # Set the background image for the start view
    background = Image.open('GUI/src/images/start.jpg')
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)

    # Load and display the start button image
    start_button_image = Image.open('GUI/src/elements/start_button.png')
    start_button_image_resized = start_button_image.resize((200, 50))
    start_button_photo = ImageTk.PhotoImage(start_button_image_resized)
    canvas.start_button = start_button_photo
    canvas.start_button_image = start_button_image_resized
    
    start_button = canvas.create_image(640, 360, image=start_button_photo)

    # Function to handle mouse enter event on the start button
    def on_enter(event):
        brightened_image = reduce_brightness(canvas.start_button_image)
        brightened_photo = ImageTk.PhotoImage(brightened_image)
        canvas.itemconfig(start_button, image=brightened_photo)
        canvas.current_button_image = brightened_photo

    # Function to handle mouse leave event on the start button
    def on_leave(event):
        canvas.itemconfig(start_button, image=canvas.start_button)

    # Bind the start button click event to the start_process function
    canvas.tag_bind(start_button, '<Button-1>', lambda event: start_process())
    # Bind the mouse enter and leave events to the respective handlers
    canvas.tag_bind(start_button, '<Enter>', on_enter)
    canvas.tag_bind(start_button, '<Leave>', on_leave)

# Function to display preprocessing settings and team selection
def preprocessing_settings(file_path):
    global team
    team = "A"  # Initial team value

    # Set the background image for the preprocessing view
    background = Image.open("GUI/src/images/preprocess.jpg")
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)  

    # Classify teams and get player data and colors
    dictPlayers, colors, _ = team_classification(file_path)
    img_path = 'result/teamClassification.png'

    # Display the team classification result image
    imgX = 727
    img = Image.open(img_path)
    img = img.resize((imgX, int((imgX/16) * 9)))
    img = ImageTk.PhotoImage(img)
    canvas.img = img
    canvas.create_image(640-(imgX//2), 62, anchor=tk.NW, image=img)
    
    # Load and display the team A button image
    teamA_button_img = Image.open("GUI/src/elements/teamA_button.png")
    teamA_button_img_resized = teamA_button_img.resize((160, 40))
    teamA_button_img_dark = reduce_brightness(teamA_button_img_resized, 0.5)
    teamA_button_photo = ImageTk.PhotoImage(teamA_button_img_dark)
    canvas.teamA_button_photo = teamA_button_photo
    canvas.teamA_button_img_resized = teamA_button_img_resized
    
    # Load and display the team B button image
    teamB_button_img = Image.open("GUI/src/elements/teamB_button.png")
    teamB_button_img_resized = teamB_button_img.resize((160, 40))
    teamB_button_img_dark = reduce_brightness(teamB_button_img_resized, 0.5)
    teamB_button_photo = ImageTk.PhotoImage(teamB_button_img_dark)
    canvas.teamB_button_photo = teamB_button_photo
    canvas.teamB_button_img_resized = teamB_button_img_resized
    
    # Load and display the process button image
    process_button_img = Image.open("GUI/src/elements/process_button.png")
    process_button_img_resized = process_button_img.resize((200, 50))
    process_button_photo = ImageTk.PhotoImage(process_button_img_resized)
    canvas.process_button_photo = process_button_photo
    canvas.process_button_img = process_button_img_resized
    
    button_space = 90
    button_height = 560
    
    teamA_button = canvas.create_image(640-button_space, button_height, image=teamA_button_photo)
    teamB_button = canvas.create_image(640+button_space, button_height, image=teamB_button_photo)
    process_button = canvas.create_image(640, 630, image=process_button_photo)

    # Function to handle team selection
    def select_team(this_team):
        global team
        team = this_team
        if team == "A":
            brightened_teamA = ImageTk.PhotoImage(canvas.teamA_button_img_resized)
            darkened_teamB = ImageTk.PhotoImage(reduce_brightness(canvas.teamB_button_img_resized, 0.5))
            canvas.itemconfig(teamA_button, image=brightened_teamA)
            canvas.itemconfig(teamB_button, image=darkened_teamB)
            canvas.teamA_button_photo = brightened_teamA
            canvas.teamB_button_photo = darkened_teamB
        elif team == "B":
            brightened_teamB = ImageTk.PhotoImage(canvas.teamB_button_img_resized)
            darkened_teamA = ImageTk.PhotoImage(reduce_brightness(canvas.teamA_button_img_resized, 0.5))
            canvas.itemconfig(teamB_button, image=brightened_teamB)
            canvas.itemconfig(teamA_button, image=darkened_teamA)
            canvas.teamB_button_photo = brightened_teamB
            canvas.teamA_button_photo = darkened_teamA

    # Function to handle mouse enter event on the process button
    def on_enter_process(event):
        brightened_image = reduce_brightness(canvas.process_button_img, 0.8)
        brightened_photo = ImageTk.PhotoImage(brightened_image)
        canvas.itemconfig(process_button, image=brightened_photo)
        canvas.current_button_image = brightened_photo

    # Function to handle mouse leave event on the process button
    def on_leave_process(event):
        canvas.itemconfig(process_button, image=canvas.process_button_photo)

    # Bind the team buttons and process button to their respective handlers
    canvas.tag_bind(teamA_button, '<Button-1>', lambda event: select_team("A"))
    canvas.tag_bind(teamB_button, '<Button-1>', lambda event: select_team("B"))
    canvas.tag_bind(process_button, '<Button-1>', lambda event: loading_screen(file_path, team, dictPlayers, colors))
    canvas.tag_bind(process_button, '<Enter>', on_enter_process)
    canvas.tag_bind(process_button, '<Leave>', on_leave_process)

# Function to start the image selection process
def start_process():
    select_image()

# Initialize the main application window
root = tk.Tk()
root.title("Automatic Offside Recognition")
root.geometry("1280x720")
root.resizable(False, False)

# Set the application icon
icon_path = 'GUI/src/icons/logo.ico'
im = Image.open(icon_path)
photo = ImageTk.PhotoImage(im)
root.wm_iconphoto(True, photo)

# Create and pack the main canvas
canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
canvas.pack()

# Display the start view
start_view()

# Run the main event loop
root.mainloop()
