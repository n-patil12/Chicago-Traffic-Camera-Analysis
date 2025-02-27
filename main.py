import sqlite3
import matplotlib.pyplot as plt 
import datetime
import numpy as np

dbConn = sqlite3.connect("chicago-traffic-cameras.db")
dbCursor = dbConn.cursor()

#---------------------------------------------------------------------------------------
# this is the beginning part of the program:

#counts the number of red cameras
red_cameras = """ SELECT COUNT(Camera_ID) FROM RedCameras;"""
dbCursor.execute(red_cameras)
redCam_Count = dbCursor.fetchall()

#counts the number of speed cameras
speed_cameras = """SELECT COUNT(Camera_ID) FROM SpeedCameras"""
dbCursor.execute(speed_cameras)
speedCam_Count = dbCursor.fetchall()

#counts the number of violations from red cameras
red_violations = """SELECT COUNT(Num_Violations) FROM RedViolations"""
dbCursor.execute(red_violations)
redVi_Count = dbCursor.fetchall()

#counts the number of violations from speed cameras
speed_violations = """SELECT COUNT(Num_Violations) FROM SpeedViolations"""
dbCursor.execute(speed_violations)
speedVi_Count = dbCursor.fetchall()

#gets the range of dates in the database
begin_date = """SELECT Violation_Date FROM RedViolations LIMIT 1;"""
dbCursor.execute(begin_date)
first_date = dbCursor.fetchall()
last_date = """SELECT Violation_Date FROM RedViolations ORDER BY Violation_Date DESC LIMIT 1;"""
dbCursor.execute(last_date)
end_date = dbCursor.fetchall()

#counts the total number of violations from red cameras
red_violations_sum = """SELECT SUM(Num_Violations) FROM RedViolations"""
dbCursor.execute(red_violations_sum)
redVi_Sum = dbCursor.fetchall()

#counts the total number of violations from speed cameras
speed_violations_sum = """SELECT SUM(Num_Violations) FROM SpeedViolations"""
dbCursor.execute(speed_violations_sum)
speedVi_Sum = dbCursor.fetchall()

#--------------------------------------------------------------------------------------
# this is for command 1

#grabs all of the intersections
def command_1(intersection_name):
    intersection_sql = """SELECT Intersection_ID, Intersection FROM Intersections WHERE Intersection like ? ORDER BY Intersection ASC;"""
    dbCursor.execute(intersection_sql, (intersection_name,))
    intersection_output = dbCursor.fetchall()
    return intersection_output

#--------------------------------------------------------------------------------------
#this is for command 2

# capture all the red light cameras on the intersection
def command_2_red(intersection_name2):
    redcameras_sql = """SELECT RedCameras.Camera_ID, RedCameras.Address
FROM RedCameras
JOIN Intersections on Intersections.Intersection_ID = RedCameras.Intersection_ID
WHERE Intersections.Intersection = ?;"""
    dbCursor.execute(redcameras_sql, (intersection_name2,))
    intersection_red = dbCursor.fetchall()
    return intersection_red

#grabs all the speed cameras from a specific intersection
def command_2_speed(intersection_name2):
    speedcameras_sql = """SELECT SpeedCameras.Camera_ID, SpeedCameras.Address
FROM SpeedCameras
JOIN Intersections on Intersections.Intersection_ID = SpeedCameras.Intersection_ID
WHERE Intersections.Intersection = ?;"""
    dbCursor.execute(speedcameras_sql, (intersection_name2,))
    intersection_speed = dbCursor.fetchall()
    return intersection_speed

#--------------------------------------------------------------------------------------
#this is for command 3

#gets all the total red light violations from a specific date
def command_3_red(input_date):
    redcameras_sql = """SELECT SUM(Num_Violations)
FROM RedViolations
WHERE Violation_Date = ?;"""
    dbCursor.execute(redcameras_sql, (input_date,))
    total_red = dbCursor.fetchall()
    return total_red

#gets all the total speed violations from a specific date
def command_3_speed(input_date):
    speedcameras_sql = """SELECT SUM(Num_Violations)
FROM SpeedViolations
WHERE Violation_Date = ?;"""
    dbCursor.execute(speedcameras_sql, (input_date,))
    total_speed = dbCursor.fetchall()
    return total_speed

#--------------------------------------------------------------------------------------
#this is for command 4

#counts instances of red light cameras at each intersection
def command_4_red():
    redcameras_sql2 = """SELECT RedCameras.Intersection_ID, Intersections.Intersection, COUNT(RedCameras.Camera_ID)
FROM RedCameras
JOIN Intersections on Intersections.Intersection_ID = RedCameras.Intersection_ID
GROUP BY RedCameras.Intersection_ID
ORDER BY COUNT(RedCameras.Camera_ID) DESC;"""
    dbCursor.execute(redcameras_sql2)
    total_red2 = dbCursor.fetchall()
    return total_red2

#counts instances of speed cameras at each intersection
def command_4_speed():
    speedcameras_sql2 = """SELECT SpeedCameras.Intersection_ID, Intersections.Intersection, COUNT(SpeedCameras.Camera_ID)
FROM SpeedCameras
JOIN Intersections on Intersections.Intersection_ID = SpeedCameras.Intersection_ID
GROUP BY SpeedCameras.Intersection_ID
ORDER BY COUNT(SpeedCameras.Camera_ID) DESC;"""
    dbCursor.execute(speedcameras_sql2)
    total_speed2 = dbCursor.fetchall()
    return total_speed2

#--------------------------------------------------------------------------------------
#this is for command 5

#get all the total red light violations at intersections from a specific date 
def command_5_red(input_date2):
    redcameras_sql3 = """SELECT RedCameras.Intersection_ID, Intersections.Intersection, SUM(RedViolations.Num_Violations)
FROM RedCameras
JOIN Intersections on Intersections.Intersection_ID = RedCameras.Intersection_ID
JOIN RedViolations on RedViolations.Camera_ID = RedCameras.Camera_ID
WHERE RedViolations.Violation_Date like ?
GROUP BY RedCameras.Intersection_ID
ORDER BY SUM(RedViolations.Num_Violations) DESC;"""
    dbCursor.execute(redcameras_sql3, (input_date2,))
    total_red3 = dbCursor.fetchall()
    return total_red3

#get all the total speed violations at intersections from a specific date 
def command_5_speed(input_date2):
    speedcameras_sql3 = """SELECT SpeedCameras.Intersection_ID, Intersections.Intersection, SUM(SpeedViolations.Num_Violations)
FROM SpeedCameras
JOIN Intersections on Intersections.Intersection_ID = SpeedCameras.Intersection_ID
JOIN SpeedViolations on SpeedViolations.Camera_ID = SpeedCameras.Camera_ID
WHERE SpeedViolations.Violation_Date like ?
GROUP BY SpeedCameras.Intersection_ID
ORDER BY SUM(SpeedViolations.Num_Violations) DESC;"""
    dbCursor.execute(speedcameras_sql3, (input_date2,))
    total_speed3 = dbCursor.fetchall()
    return total_speed3

#--------------------------------------------------------------------------------------
#this is for command 6

# get all the red light violations from a specific camera id
def command_6_red(input_date3):
    redcameras_sql4 = """SELECT strftime('%Y',Violation_Date) AS year, SUM(Num_Violations) AS violation_count
FROM RedViolations
WHERE camera_id like ?
GROUP BY year 
ORDER BY year ASC;"""
    dbCursor.execute(redcameras_sql4, (input_date3,))
    total_red4 = dbCursor.fetchall()
    return total_red4

# get all the speed violations from a specific camera id
def command_6_speed(input_date3):
    speedcameras_sql4 = """SELECT strftime('%Y',Violation_Date) AS year, SUM(Num_Violations) AS violation_count
FROM SpeedViolations
WHERE camera_id like ?
GROUP BY year 
ORDER BY year ASC;"""
    dbCursor.execute(speedcameras_sql4, (input_date3,))
    total_speed4 = dbCursor.fetchall()
    return total_speed4

#--------------------------------------------------------------------------------------
#this is for command 7

#checks if the camera ids exist for both the red and speed cameras
def command_7_check_red(camera_id):
    redcameras_check = """SELECT COUNT(Num_Violations) 
FROM RedViolations
WHERE Camera_ID like ? ;"""
    dbCursor.execute(redcameras_check, (camera_id,))
    red_check = dbCursor.fetchall()
    return red_check


def command_7_check_speed(camera_id):
    speedcameras_check = """SELECT COUNT(Num_Violations) 
FROM SpeedViolations
WHERE Camera_ID like ? ;"""
    dbCursor.execute(speedcameras_check, (camera_id,))
    speed_check = dbCursor.fetchall()
    return speed_check

#will grab the total violations from both red and speed cameras from a specific camera id and year
def command_7_red(camera_id, input_year):
    redcameras_sql5 = """SELECT strftime('%m', violation_date) AS month, strftime('%Y', violation_date) as Year, SUM(Num_Violations) AS violations
FROM RedViolations
WHERE Camera_ID like ? AND strftime('%Y', violation_date) like ?
GROUP BY month
ORDER BY month;"""
    dbCursor.execute(redcameras_sql5, (camera_id, input_year,))
    total_red5 = dbCursor.fetchall()
    return total_red5

def command_7_speed(camera_id, input_year):
    speedcameras_sql5 = """SELECT strftime('%m', violation_date) AS month, strftime('%Y', violation_date) as Year, SUM(Num_Violations) AS violations
FROM SpeedViolations
WHERE Camera_ID like ? AND strftime('%Y', violation_date) like ?
GROUP BY month
ORDER BY month;"""
    dbCursor.execute(speedcameras_sql5, (camera_id, input_year))
    total_speed5 = dbCursor.fetchall()
    return total_speed5

#--------------------------------------------------------------------------------------
#this is for command 8

#gets the total red light violations for the year
def command_8_red(input_year):
    redcameras_sql6 = """SELECT Violation_Date, SUM(Num_Violations) FROM RedViolations
WHERE Violation_Date like ?
GROUP BY Violation_Date
ORDER BY Violation_Date ASC;"""
    dbCursor.execute(redcameras_sql6, (input_year,))
    total_red6 = dbCursor.fetchall()
    return total_red6

#gets the total speed violations for the year
def command_8_speed(input_year):
    redcameras_sql8 = """SELECT Violation_Date, SUM(Num_Violations) FROM SpeedViolations
WHERE Violation_Date like ?
GROUP BY Violation_Date
ORDER BY Violation_Date ASC;"""
    dbCursor.execute(redcameras_sql8, (input_year,))
    total_red8 = dbCursor.fetchall()
    return total_red8

#----------------------------------------------------------------------------------------
#this is for command 9

#gets the camera ids, latitude,  and longitude from a specific address for both red and speed cameras
def command_9_red(street_name):
    redcameras_sql9 = """SELECT Camera_ID, Address, Latitude, Longitude
FROM RedCameras
WHERE Address LIKE ?
ORDER BY Camera_ID ASC; """
    dbCursor.execute(redcameras_sql9, (street_name,))
    total_red9 = dbCursor.fetchall()
    return total_red9

def command_9_speed(street_name):
    speedcameras_sql9 = """SELECT Camera_ID, Address, Latitude, Longitude
FROM SpeedCameras
WHERE Address LIKE ?
ORDER BY Camera_ID ASC;"""
    dbCursor.execute(speedcameras_sql9, (street_name,))
    total_speed9 = dbCursor.fetchall()
    return total_speed9

#--------------------------------------------------------------------------------------

#this is just the menu option
menu_options = """Select a menu option: 
 1. Find an intersection by name
 2. Find all cameras at an intersection
 3. Percentage of violations for a specific date
 4. Number of cameras at each intersection
 5. Number of violations at each intersection, given a year
 6. Number of violations by year, given a camera ID
 7. Number of violations by month, given a camera ID and year
 8. Compare the number of red light and speed violations, given a year
 9. Find cameras located on a street
or x to exit the program.""" 

#these are all of the different commands: 

def command_1_option(): #command 1 --> user will enter intersection name, and get all intersections associated
    print()
    intersection_name = input("Enter the name of the intersection to find (wildcards _ and % allowed): ")
    output = command_1(intersection_name)

    if (output): #output of the query results
        for intersect in output:
            print(intersect[0], ":", intersect[1])
    else:
        print("No intersections matching that name were found.")

def command_2_option(): #command 2 --> enter name of intersection + checks if red or speed cameras exist at intersection
    print()
    intersection_name2 = input("Enter the name of the intersection (no wildcards allowed): ")
    output_red2 = command_2_red(intersection_name2)
    output_speed2 = command_2_speed(intersection_name2)

    #checks if the query results produce any output:

    #red light cameras
    if (output_red2):
        print()
        print("Red Light Cameras:")
        for intersect2 in output_red2:
            print(" ", intersect2[0], ":", intersect2[1])

    else:
        print()
        print("No red light cameras found at that intersection.\n")
    
    #speed cameras
    if (output_speed2):
        print()
        print("Speed Cameras:")
        for intersect3 in output_speed2:
            print(" ", intersect3[0], ":", intersect3[1])
    else:
        print()
        print("No speed cameras found at that intersection.\n")


def command_3_option(): #command 3 --> outputs red light and speed violations across all cameras based on specific date
    print()
    user_date = input("Enter the date that you would like to look at (format should be YYYY-MM-DD): ")
    total_redOutput = command_3_red(user_date)
    total_speedOutput = command_3_speed(user_date)

    #checks that all of the data is not empty, otherwise it sets the total to be 0
    if total_redOutput and total_redOutput[0][0] is not None: 
            total_red = total_redOutput[0][0]
    else:
        total_red = 0

    if total_speedOutput and total_speedOutput[0][0] is not None: 
        total_speed = total_speedOutput[0][0]
    else:
        total_speed = 0

    #add up all the violations from both the red light and the speed violations
    total_Violations = total_red  + total_speed

    if total_Violations > 0: #if violations is not empty, then find the percentage and display the output
        red_percentage = (total_red / total_Violations) * 100
        speed_percentage = (total_speed / total_Violations) * 100

        print("Number of Red Light Violations:", f"{total_red:,}", f"({red_percentage:.3f}%)")
        print("Number of Speed Violations:", f"{total_speed:,}", f"({speed_percentage:.3f}%)")
        print("Total Number of Violations:", f"{total_Violations:,}")
    else:
        print("No violations on record for that date.\n")

def command_4_option(): #command 4 --> outputs red light and speed cameras along each intersection
    print()
    total_redOutput2 = command_4_red()
    total_speedOutput2 = command_4_speed()
    total_red_count = 0

    #grabs the total number of red light cameras for the percentage
    for red in total_redOutput2:
        total_red_count += red[2]

    print("Number of Red Light Cameras at Each Intersection") #outputs all the red light cameras, as well as their percentages
    for r in total_redOutput2:
        individual_percentage = (r[2] / total_red_count) * 100
        print(f" {r[1]} ({r[0]}) : {r[2]} ({individual_percentage:.3f}%)")

    print()
    total_speed_count = 0

    #grabs the total number of speed cameras for the percentage
    for speed in total_speedOutput2:
        total_speed_count += speed[2]
    
    print("Number of Speed Cameras at Each Intersection") #outputs all the red light cameras, as well as their percentages
    for s in total_speedOutput2:
        individual_percentage2 = (s[2] / total_speed_count) * 100
        print(f" {s[1]} ({s[0]}) : {s[2]} ({individual_percentage2:.3f}%)")

def command_5_option(): #command 5 --> output the number of red light and speed violations recorded at each intersection for a specfic year
    print()
    user_date2 = input("Enter the year that you would like to analyze: ")

    #puts in the wildcards for the queries
    total_redOutput3 = command_5_red("%" + user_date2 + "%")
    total_speedOutput3 = command_5_speed("%" + user_date2 + "%")

    if total_redOutput3 and total_speedOutput3: #checks if results are not empty
        total_red_count2 = 0
        for red in total_redOutput3:
            total_red_count2 += red[2]

        print() #outputs the red light and speed violations, along with their percentages
        print("Number of Red Light Violations at Each Intersection for", user_date2)
        for r in total_redOutput3:
            individual_percentage3 = (r[2] / total_red_count2) * 100
            print(f"  {r[1]} ({r[0]}) : {r[2]:,} ({individual_percentage3:.3f}%)")
        print("Total Red Light Violations in", user_date2, ":", "{:,}".format(total_red_count2))
        
        total_speed_count2 = 0
        for speed in total_speedOutput3:
            total_speed_count2 += speed[2]
        
        print()
        print("Number of Speed Violations at Each Intersection for", user_date2)
        for s in total_speedOutput3:
            individual_percentage4 = (s[2] / total_speed_count2) * 100
            print(f"  {s[1]} ({s[0]}) : {s[2]:,} ({individual_percentage4:.3f}%)")
        print("Total Speed Violations in", user_date2, ":", "{:,}".format(total_speed_count2))

    else: #the queries are empty and there are no red light or speed violations for that year
        print()
        print("Number of Red Light Violations at Each Intersection for", user_date2)
        print("No red light violations on record for that year.")
        print()
        print("Number of Speed Violations at Each Intersection for", user_date2)
        print("No speed violations on record for that year.")

def command_6_option(): #command 6 --> given a camera ID, outputs the number of violations recorded by that camera for each year
    print()
    camera_id = input("Enter a camera ID: ")

    total_redOutput4 = command_6_red("%" + camera_id + "%")
    total_speedOutput4 = command_6_speed("%" + camera_id + "%")

    if total_redOutput4: #outputs the yearly violations generated from the queries for just red light if no speed
        print("Yearly Violations for Camera", camera_id)
        for r in total_redOutput4:
            print(r[0], ":", "{:,}".format(r[1]))
        
        print()
        user_plot = input("Plot? (y/n) ") #ask user if they want to plot

        if user_plot == "y": #plots for the red light violations
            years = [red[0] for red in total_redOutput4]
            violations = [red[1] for red in total_redOutput4]

            plt.figure(figsize=(8, 5))
            plt.plot(years, violations, color='blue', linestyle='-')

            plt.xlabel("Year")
            plt.ylabel("Number of Violations")
            plt.title(f"Yearly Violations for Camera {camera_id}")
            plt.xticks(rotation= 0)

            plt.show()

    elif total_speedOutput4: #outputs the yearly violations generated from the queries for just speed if no red light
        print("Yearly Violations for Camera", camera_id)
        for s in total_speedOutput4:
            print(s[0], ":", "{:,}".format(s[1]))

        print()
        user_plot = input("Plot? (y/n) ")

        if user_plot == "y": #plots for the speed violations
            years = [speed[0] for speed in total_speedOutput4]
            violations = [speed[1] for speed in total_speedOutput4]

            plt.figure(figsize=(8, 5))
            plt.plot(years, violations, color='blue', marker='o', linestyle='-')

            plt.xlabel("Year")
            plt.ylabel("Number of Violations")
            plt.title(f"Yearly Violations for Camera {camera_id}")
            plt.xticks(rotation= 0)

            plt.show()

    else:
        print("No cameras matching that ID were found in the database.")

def command_7_option(): #command 7 --> given camera ID and a year, outputs the number of violations recorded by that camera for each month in the specified year,
    print()

    #checks if the camera id even exists
    camera_id = input("Enter a camera ID: ")
    red_return = command_7_check_red(camera_id)
    speed_return = command_7_check_speed(camera_id)

    if red_return[0][0] > 0: #the count for the red light camera id is not 0
        user_year = input("Enter a year: ")

        #results after camera id and user inputed year
        total_redOutput5 = command_7_red("%" + camera_id + "%", "%" + user_year + "%")
        print("Monthly Violations for Camera" , camera_id, "in", user_year)

        if total_redOutput5: #outputs the monthly red light violations
            for r in total_redOutput5:
                new_date_str = r[0] + "/" + user_year
                print(new_date_str, ":", "{:,}".format(r[2]))

        print()
        user_plot = input("Plot? (y/n) ") #asks user to plot the results

        if user_plot == "y":
            years = [red[0] for red in total_redOutput5]
            violations = [red[2] for red in total_redOutput5]

            plt.figure(figsize=(8, 5))
            plt.plot(years, violations, color='blue', linestyle='-')

            #plots for just the red light violations
            plt.xlabel("Monthly")
            plt.ylabel("Number of Violations")
            plt.title(f"Monthly Violations for Camera {camera_id} ({user_year})")
            plt.xticks(rotation= 0)

            plt.show()

    #repeats process for the speed cameras if red light does not exist
    elif speed_return[0][0] > 0:
        user_year = input("Enter a year: ")

        total_speedOutput5 = command_7_speed("%" + camera_id + "%", "%" + user_year + "%")
        print("Monthly Violations for Camera" , camera_id, "in", user_year)

        if total_speedOutput5:
            for s in total_speedOutput5:
                new_date_str = s[0] + "/" + user_year
                print(new_date_str, ":", "{:,}".format(s[2]))

        print()
        user_plot = input("Plot? (y/n) ") #asks user to plot the data

        if user_plot == "y":
            years = [speed[0] for speed in total_speedOutput5]
            violations = [speed[2] for speed in total_speedOutput5]

            plt.figure(figsize=(8, 5))
            plt.plot(years, violations, color='blue', linestyle='-')

            plt.xlabel("Monthly")
            plt.ylabel("Number of Violations")
            plt.title(f"Monthly Violations for Camera {camera_id} ({user_year})")
            plt.xticks(rotation= 0)

            plt.show()

    else: #outputs message if both do not exist
        print("No cameras matching that ID were found in the database.")

def command_8_option(): #command 8 --> given a year, outputs the number of red light violations across all red light cameras, and the number of speed violations across all speed cameras, for each day in that year.
    print()
    user_year = input("Enter a year: ")

    #grabs results based on user inputted year
    asc_red = command_8_red('%' + user_year + '%')
    asc_speed = command_8_speed('%' + user_year + '%')

    print("Red Light Violations:") #prints red light violations
    if asc_red:
        #grabs the first 5 days of the year
        for r in range(0, 5, 1):
            print(asc_red[r][0], asc_red[r][1])
        
        #grabs the last 5 days of the year
        for r in range(len(asc_red) - 5, len(asc_red), 1):
            print(asc_red[r][0], asc_red[r][1])

    #repeats above for loop for the speed cameras
    print("Speed Violations:")
    if asc_speed:
        for s in range(0, 5, 1):
            print(asc_speed[s][0], asc_speed[s][1])
        for s in range(len(asc_speed) - 5, len(asc_speed), 1):
            print(asc_red[s][0], asc_red[s][1])

    print()
    user_plot = input("Plot? (y/n) ")

    if user_plot == "y":
        # initialize lists
        red_dates = []
        speed_dates = []
        red_violations = []
        speed_violations = []

        # create a list of all days in the year
        start_date = datetime.date(int(user_year), 1, 1)
        end_date = datetime.date(int(user_year), 12, 31)
        all_dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        day_numbers = list(range(1, 366))  # x-axis values

        #y-axis values
        total_red_vi = []
        total_speed_vi = []

        # appends the dates in the list
        for date_red in asc_red:
            red_dates.append(date_red[0])
        for date_speed in asc_speed:
            speed_dates.append(date_speed[0])

        #appends the violations inside the list
        for row in asc_red:
            red_violations.append(row[1])
        for row in asc_speed:
            speed_violations.append(row[1])

        #creates counters to append results for the y-axis values
        list_count = 0
        red_count = 0
        speed_count = 0


        #loops through all the dates in the year
        for day in all_dates:
            date_time_str = day.strftime("%Y-%m-%d") #changes the format of the dates from the query
            
            if red_dates[red_count] == date_time_str: #checks if the specific date has violations
                total_red_vi.append(red_violations[red_count]) #appends violations to y-axis list for red light
                red_count += 1
                
            else:
                total_red_vi.append(0) #means no violations exist for the date
            
            #repeats process for the speed violations
            if speed_dates[speed_count] == date_time_str:
                total_speed_vi.append(speed_violations[speed_count])
                speed_count += 1
            
            else:
                total_speed_vi.append(0)
            
            list_count += 1
        
        # plotting 
        plt.figure(figsize=(10, 6))
        plt.plot(day_numbers, total_red_vi, color='red', label='Red Light', linewidth=1.5) 
        plt.plot(day_numbers, total_speed_vi, color='gold', label='Speed', linewidth=1.5) 

        plt.xlabel('Day of Year', fontsize=12) 
        plt.ylabel('Number of Violations', fontsize=12) 
        plt.title(f'Violations Each Day of {user_year}', fontsize=14)  
        plt.xticks(np.arange(0, 366, 50), fontsize=10) 
        plt.yticks(fontsize=10) # Smaller font
        
        # set y-axis limits explicitly to start at 0
        plt.ylim(bottom=0)  
        
        plt.legend(fontsize=10, loc='upper right', frameon=False) 
        
        plt.tight_layout()
        plt.show()

def command_9_option(): #command 9 --> given the name of a street, finds all red light cameras and all speed cameras that are physically located on that street.
    print()
    #asks user for input
    user_input = input("Enter a street name: ")
    street_red = command_9_red('%' + user_input + '%')
    street_speed = command_9_speed('%' + user_input + '%')

    if (not street_red) and (not street_speed): #if the query results come back empty
        print("There are no cameras located on that street.")

    else:
        print()
        print("List of Cameras Located on Street:", user_input)
        print(" Red Light Cameras:")

        #prints out the results for red and speed violations
        if street_red:
            for row in street_red:
                print(f"     {row[0]} : {row[1]} ({row[2]}, {row[3]})")
            
        print(" Speed Cameras:")
        if street_speed:
            for speed in street_speed:
                print(f"     {speed[0]} : {speed[1]} ({speed[2]}, {speed[3]})")

        print()
        user_plot = input("Plot? (y/n) ")

        if user_plot == "y":

            # populate x and y lists with (x, y) coordinates
            x_red = [row[3] for row in street_red] 
            y_red = [row[2] for row in street_red] 
            x_speed = [row[3] for row in street_speed] 
            y_speed = [row[2] for row in street_speed]  
            
            image = plt.imread("chicago.png")
            xydims = [-87.9277, -87.5569, 41.7012, 42.0868] 
            plt.imshow(image, extent=xydims)
            plt.title(f"Cameras on {user_input} Street")

            # plot the red light cameras as red dots
            plt.plot(x_red, y_red, color='red', label='Red Light Cameras', marker='o', linestyle= '-', linewidth=1)

            # plot the speed cameras as orange dots
            plt.plot(x_speed, y_speed, color='orange', label='Speed Cameras', marker='o', linestyle= '-', linewidth=1)

            # annotate the camera ids
            for row in street_red:
                plt.annotate(f"{row[0]}", (row[3], row[2]), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)
            for row in street_speed:
                plt.annotate(f"{row[0]}", (row[3], row[2]), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)

            # sets the x and y the map area
            plt.xlim([-87.9277, -87.5569])
            plt.ylim([41.7012, 42.0868])

            plt.legend()

            plt.show()


#-----------------------------------------------------------------------------------------

def menu_func(): #for the menu function, for user to type in choices
    condition = True #keeps while loop going
    while (condition):
        print()
        print(menu_options)
        user_command = input("Your Choice --> ")

        if (user_command == 'x'): #user will leave the program
            print("Exiting program.")
            condition = False

        elif (user_command == '1'): #does the first command
            command_1_option()

        elif (user_command == '2'): #does the second command
            command_2_option()
    
        elif (user_command == '3'): #does the third command
            command_3_option()

        elif (user_command == '4'): #does the third command
            command_4_option()

        elif (user_command == '5'): #does the fifth command
            command_5_option()

        elif (user_command == '6'): #does the sixth command
            command_6_option()

        elif (user_command == '7'): #does the seventh command
            command_7_option()

        elif (user_command == '8'): #does the eighth command
            command_8_option()

        elif (user_command == '9'): #does the ninth command
           command_9_option()

        else: #user will try again until the right input is entered
            print("Error, unknown command, try again...")
            condition = True
    



#--------------------------------------------------------------------------------------
if __name__ == "__main__": #main program outputting stats, what user will first see
    print("Project 1: Chicago Traffic Camera Analysis")
    print("CS 341, Spring 2025\n")
    print("This application allows you to analyze various\naspects of the Chicago traffic camera database.\n")
    print("General Statistics:")
    print(" Number of Red Light Cameras:", redCam_Count[0][0])
    print(" Number of Speed Cameras:", speedCam_Count[0][0])
    print(" Number of Red Light Camera Violation Entries:", "{:,}".format(redVi_Count[0][0]))
    print(" Number of Speed Camera Violation Entries:", "{:,}".format(speedVi_Count[0][0]))
    print(" Range of Dates in the Database:", first_date[0][0], "-", end_date[0][0])
    print(" Total Number of Red Light Camera Violations:", "{:,}".format(redVi_Sum[0][0]))
    print(" Total Number of Speed Camera Violations:", "{:,}".format(speedVi_Sum[0][0]), "\n")

    menu_func() #goes to the menu function above

    
    