# SMART STUDY

Smart Study is an app to effectively manage, track and study materials.

Materials for each course are uploaded , and timetable for study is created at account creation for user.

### SETUP

- Create a virtual environment
- Install all required packages
- Run main.py

### PACKAGES

- matplotlib
- pandas
- openpyxl
- json

### **Main Features:**

1. Create Timetable

   - a Page to get User Profile and store in `UserProfile.json`
   - Timetalble creation : should consists of a list of days with a field to input courses for each day. `TimeTable.json`

2. Upload Files for Each course

   - User Should be able to upload materials for each material, which would be stored in **materials**
   - Additionally a page for Updating or Deleting materials associated with a course can be supported

3. Main Page

   - Mainpage should be provide commands in the filebar for navigating application
   - It should have a notification section, for courses the user hasn't touched yet.
   - It should have section under notification or a seperate page entirely, to list all the materials for courses, and give an option to **START STUDY**
   - it should have a CTA Button to **START STUDY** which will open the course to study for current day, based on timetable.

4. Timer and Tracking

   - on **`START STUDY`** The application should be opened, and the timer should be opened automatically
   - The tracking algorithm should detect automatically when the user closes computer, closes document then stop timer automatically
   - The user should also be able to stop the timer manually, and start as far as the material is open.

5. Analysis

   - Every successful time input(start & end timer), time should be recorded in **week.json**
   - A command in the **filemenu** should enable **view-week-analysis**
   - **`view-week-analysis`** should plot graph based on **week** result of timer(not past 7 day's e get why) and display it to the user in same/seperate window
   - Every week application should check and migrate the past **week** data to the past folder

### **TOOLS**

Data will be persisted in files in **store directory**, using json serialization, which will serve as the local Database
