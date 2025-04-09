# CarShowroom

# APP NAME     Car Showroom

# GitHub Repository
The source code for this project is available on GitHub: https://github.com/AlexBlanford/CarShowroom/tree/main

## Identification
- **Name:** Alex Blanford	
- **P-number:** P476502
- **Course code:** IY499

## Declaration of Own Work
I confirm that this assignment is my own work.
Where I have referred to academic sources, I have provided in-text citations and included the sources in the final reference list.

## Introduction 
This code represents a simple car showroom. It consists of the basics features such as adding a car, viewing the cars, and seeing the selected car in more detail. Once run, the application opens a very simple interface in fullscreen (can be toggled on and off by using the ‘esc’ key or the ‘f11’ key) which consists of a dark blue shade header displaying “Premium Car Showroom”. Below the header are the navigation buttons. 3 simple and straight to the point buttons that includes the View Cars button, which is the main page, the Add Car button which allows users to add a new car to the showroom, and an exit button that shuts down the application. Below are 3 sample cars. Displayed in each square is a picture of the car, the brand and model name of the car, the price, and the year. If you the user would like to see more information about the car, they could select the car and another window would pop up which consists of an enlarged image of the car, the year, price, mileage, and a description by the publisher. At the top of the pop up is a header displaying the brand and model name in a gradient blue background as well as a close button on the bottom of the page. Once back in the main page, the cars can be sorted in multiple ways including the default order (in order of date the cars were added), price (both increasing and decreasing), year (both increasing and decreasing), year (both oldest and newest), and alphabetically (A-Z and Z-A). The Add Car layout is also simple. 7 input fields are shows as well as a header at the top displaying “Add New Car” in a gradient blue background. The 7 input fields include the make, model, year, price, mileage, description, and image path. Some fields are required in order to add the car to the showroom. Those required fields are marked with a * next to the name and is shown in red. If a required field is missing, an error popup will be shown informing the user that they have missed a required field. For use simplicity, a browse button is also featured, allowing the user to choose the picture they would like to upload by navigating and pressing on their desktop. A placeholder is also provided in the input fields giving examples of what should be inputted into the fields. Once the fields are filled in, the user can select the Add Car button, which adds the inputted data to the cars.txt file (file handling) and shows the updated showroom display. If the user changes their mind about adding a new car, they could select the cancel button which will return to the main showroom page. In the case there are many cars displayed in the showroom, a scroll wheel is given to move up and down and see all the cars in the showroom.  

## Installation
To run the game, ensure you have Python installed, and then install the required dependencies from the `requirements.txt` file using the following command:
```bash
pip install -r requirements.txt
```

## How to  use
Simply navigate around the window using your mouse, a use the left mouse button to select a button. In the Add Car page, easily navigate from one input field to another by manually left clicking on each field or using the ‘tab’ button. 

### Running the Game
```python
python CarShowroom.py
```

## Application Elements
1.	Core UI Elements
-	Main Window
-	Header Section
-	Navigation Bar
-	Scrollable display area
2.	Data Management
-	File handling (stores car data inputted in the input fields)
-	Sample data (three sample cars)
3.	Functions
-	Sorting system
-	Car display grid
4.	Technical features
-	Image Handling 
-	Error Handling
-	UI effects
5.	Visual styling
-	Colors
-	Fonts
-	Visual feedback 
6.	User interaction
-	Keyboard controls 
-	Mouse interactions 


## Libraries Used
The following libraries are used in this project:
- Tkinter
- Pillow

## Project Structure
1.	Data Layer : defaultCars list, car file, loading and saving cars
2.	Presentation layer: Showing the cars in the main page, showing the car details, adding a car
3.	User Interface : Widgets with hover effects, gradient headers, scrollable areas, popups for informing user of error or success 
4.	Sorting Logic 
5.	Utility featues:  fullscreen toggling capabilities, responsive layout
6.	Error handling: Image loading errors, file errors, inputs errors 

