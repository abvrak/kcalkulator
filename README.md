**kcalkulator**  is an application designed for managing user profiles and tracking body weight, BMI values, and calorie needs. Its goal is to support users in effectively managing their diet and physical activity by providing key data such as:
- Calculating BMI and categorizing it based on weight and height.
- Tracking the history of weights, BMI, and calorie requirements.
- Calculating "caloric maintenance" (TDEE) considering activity level and age.
- Estimating calorie intake for weight gain or weight loss.
- Managing user profiles and measurement history.


**Prerequisites**
To run the kcalkulator project, ensure the following requirements are met:
- Python version 3.11.
- Installed libraries:
    - `numpy`
    - `scikit-learn`
    - `sqlite3` (built-in with Python)
    - `PyQt6`
    - `matplotlib`



**Project Structure**
The project consists of several modules responsible for different functionalities:

- **`main_classes.py`:** Contains classes for BMI and calorie demand calculations:
    - `BmiCalculator` - Calculates BMI value and determines weight category.
    - `CaloricDemandCalculator` - Computes caloric maintenance (TDEE) based on body weight, age, height, and activity level.
    - `CaloricDemandAdjuster` - Calculates caloric surplus or deficit for dietary goals.

- **`database.py`:** Manages the SQLite database:
    - Creating, saving, and deleting user profiles.
    - Storing the history of weight measurements, BMI, and calorie demand.
    - Importing/exporting user data to/from files.

- **`main_gui.py`:** Handles the user interface created using PyQt6. Includes functions for navigation between views, managing user data, and generating charts.


**Application Usage**

Importing a Profile

- Start by navigating to the "Profile Management" tab and importing one or more profiles. If a mistake occurs, you can delete the incorrectly added profile.

Selecting a Profile

- After importing the profile, go to the main menu and select the desired profile to access further functions.

Profile Summary

- Once a profile is selected, the application will display a detailed summary of all information related to that profile.

Exporting the Summary

- In the top-right corner of the screen, there is an option to export the summary. This allows you to save or share the profile data.

Updating Data

- You can update the profile with a new weight and measurement date. To do this, simply click the "+" button next to the weight label.
