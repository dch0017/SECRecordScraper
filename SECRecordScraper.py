""""
Python Semester Project

Web-Scraping Program
This program is designed to scrape a specific website and deliver details about 
an SEC teams football/basketball record from a given year.

Damon Hebb, Jacob Bourland, Alyssa Krienke, Katherine Rothbart

"""""
# Import the necessary modules needed for the program
## Requests will handle pulling the HTML code from the website
## BeautifulSoup will handle compiling and searching through the HTML code
## Pandas will be used to import the data collected into a dataframe
## tKinter is used to graphically display data in a pop-up window
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *

# This will allow all the columns to be displayed, without this the columns or rows may get cut off
# This line also left-aligns the headers of the columns as to not cause confusion
pd.set_option('display.max_columns', None, 'display.max_rows', None, 'display.max_colwidth', -1,
              'display.width', 1000, 'colheader_justify', 'left')


# CONSTANTS: these are the only choices that a user can select
# The current choices are years from 1950-2018, SEC Schools, and football/basketball
YEARS = [x for x in range(1950,2019)]
SCHOOLS = ["auburn","mississippi","alabama","arkansas", "georgia", "florida", "kentucky", "missouri",
           "south-carolina", "vanderbilt", "tennessee", "louisiana-state", "texas-am", "mississippi-state"]
SPORTS = ["football","basketball"]


# This main function goes through and collects input from the user and runs through the 
# functions to create and display a window showcasing the given teams record.
def main():
    # These variables are the user's choices for school, sport, and year
    school = schoolChoice()
    sport = sportChoice()
    year = yearChoice()

    # We create all the variables that are returned from the webScrape() method
    pageURL, date_game, opp_name, school_points, opp_points, game_results, game_notes = webScrape(school, year, sport)

    
    # getWinLosses() returns two variables so we save those variables into the wins, losses variables
    wins, losses = getWinLosses(game_results)

    
    # This is the pandas dataframe that we will put into the tKinter window
    schedData = getSchedule(sport, date_game, opp_name, school_points, opp_points, game_results, game_notes)

    # Here we turn our result strings into variables so they are easier to print onto a window
    teamChoice = f'{school.upper()} {sport.upper()} --- {year}\n\n'
    teamRecord = f'\n\n{school.upper()}\'s {sport} record in {year} was {wins}-{losses}'
    dataSource = f'\n\nData Source:\n{pageURL}'
    
    
    # We user the tKinterWindow function to put together all our data and print it out on a pop-up display
    tKinterWindow(teamChoice, schedData, teamRecord, dataSource)

        

# This function runs through the school choice that the user selects and makes sure
# that it is a valid SEC school
def schoolChoice():
    while True:
        school = input("What SEC school would you like to view('help' for list of schools):")
        school = school.lower()
        if school in SCHOOLS:
            return school
        elif school == "help":
            print("A list of available shcools is: ")
            for i in SCHOOLS:
                print(i)
            continue
        # Here we offer some easier spellings for users to type such as 'lsu' instead of 'louisiana-state'
        elif school == "bama":
            school = "alabama"
            
        elif school == "texasam":
            school = "texas-am"
        
        elif school == "texas am":
            school = "texas-am"
            
        elif school == "texas a&m":
            school = "texas-am"
            
        elif school == "south carolina":
            school = "south-carolina"

        elif school == "lsu":
            school = "louisiana-state"

        elif school == "miss st":
            school = "mississippi-state"

        elif school == "ole miss":
            school = "mississippi"
        
        else:
            print("That is not a valid school. Please only use SEC schools.")
            continue
        
        return school


# This function verifies that the user's choice is only basketball or football
def sportChoice():
    while True:
        sport = input("What sport would you like to see([f]ootball or [b]asketball):")
        sport = sport.lower()
        if sport == "b":
            sport = "basketball"
        elif sport == "f":
            sport = "football"
        
        # This IF statement is ran after the initial IF statement to check to see if football or basketball has been selected
        if sport in SPORTS:
            return sport
        else:
            print("That is not a valid sport. Please only type 'football' or 'basketball'")
            continue

# This function makes sure that the user selects a valid year and makes it an int so it can check to see if it
# is in the YEARS list we created at the beginning. Then turns the year back into a string to easily be printed
def yearChoice():
    while True:
        try:
            year = int(input("What year would you like to see the record for(1950-2018):"))
        except ValueError:
            print("That is not a valid year.")
            continue
        if year in YEARS:
            yearURL = str(year)
            return yearURL
        else:
            print("That is not a valid year.")
            continue

# This function uses the proper layout and formatting to scrape the data from a basketball schedule
def webScrape(school, year, sport):
    
    # Resetting all the variables
    date_game = []
    opp_name = []
    school_points = []
    opp_points = []
    game_results = []
    game_notes = []
    
# Here we get the URL for the webpage that we will scrape
    year = str(year)
    if sport == "basketball":
        sportURL = "cbb"
    elif sport == "football":
        sportURL = "cfb"
    # We plug in our variables to get the approprite webpage with the record
    pageURL = f'https://www.sports-reference.com/{sportURL}/schools/{school}/{year}-schedule.html'

# This uses the request package to get the web page and the
# BeautifulSoup package to parse the html that comes from it
    pageResponse = requests.get(pageURL, timeout=5)
    pageContent = BeautifulSoup(pageResponse.content, "html.parser")
    
# Adds all the dates of the games to a list
    dates = pageContent.find_all(attrs={"data-stat": "date_game"})
    for date in dates:
        date_game.append(date.get_text())
# Adds each opponent to a list
    opponents = pageContent.find_all(attrs={"data-stat": "opp_name"})
    for opponent in opponents:
        opp_name.append(opponent.get_text())
# Adds points from each game to a list that the user's team scored to a list
    # We need an If statement to determine whether the sport is football or basketball
    # as the HTML pages vary slightly for each sport
    if sport == "basketball":
        points = pageContent.find_all(attrs={"data-stat": "pts"})
    elif sport == "football":
        points = pageContent.find_all(attrs={"data-stat": "points"})
    for point in points:
        school_points.append(point.get_text())      
# Adds the opponents points scored for each game to a list
    # We need an If statement to determine whether the sport is football or basketball
    # as the HTML pages vary slightly for each sport
    if sport == "basketball":
        oppPoints = pageContent.find_all(attrs={"data-stat": "opp_pts"})
    elif sport == "football":
        oppPoints = pageContent.find_all(attrs={"data-stat": "opp_points"})
    for oppPoint in oppPoints:
        opp_points.append(oppPoint.get_text())
# This adds the result either W/L of each game to a list
    results = pageContent.find_all(attrs={"data-stat": "game_result"})
    for result in results:
        game_results.append(result.get_text())
# This IF/ELSE allows us to see special notes about each type of game. The HTML 
# Identifiers for each sport are different.
    if sport == "football":       
        notes = pageContent.find_all(attrs={"data-stat": "notes"})
    elif sport == "basketball":  
        notes = pageContent.find_all(attrs={"data-stat": "game_type"})
    # Since these are only SEC Schools CTourn correlates to SEC Tourney,and NCAA tourney is for
    # the NCAA tournament, however if the program were to expand outside SEC this code would need to be
    # significantly changed
    for note in notes:
        if note.get_text() == "CTOURN":
            game_notes.append("SEC Tourney")
        elif note.get_text() == "NCAA":
                game_notes.append("NCAA Tourney")
        else:
            game_notes.append("")

    
# Here we return each variable that we will need to properly use the getSchedule() function
    return pageURL, date_game, opp_name, school_points, opp_points, game_results, game_notes
        

# This function iterates through the game_results to count up Wins and Losses
def getWinLosses(game_results):
    wins = 0
    losses = 0
    for j in game_results:
        if j == "W":
            wins +=1
        elif j == "L":
            losses +=1
    return wins, losses


# This function takes all the data that was previously scraped and puts it into a pandas dataframe
def getSchedule(sport, date_game, opp_name, school_points, opp_points, game_results, game_notes):
    if sport == "football":
        schedule =pd.DataFrame({
                "Date": date_game,
                "Opponent": opp_name,
                "Points": school_points,
                "Opp-Points": opp_points,
                "Result": game_results,
                "Notes": game_notes
                })  
    elif sport == "basketball":
        schedule =pd.DataFrame({
                "Date": date_game,
                "Opponent": opp_name,
                "Points": school_points,
                "Opp-Points": opp_points,
                "Result": game_results,
                "Notes": game_notes
                })  
    # Removes the blank lines that come from the basketball HTML doc
    schedule.drop(schedule.index[schedule['Points'] == 'Tm'], inplace = True)
    # Removes the blank lines that come from the football HTML doc
    schedule.drop(schedule.index[schedule['Points'] == 'Pts'], inplace = True)
    
    # Removes the default index provided by pandas and sets "Date" as index
    schedule.set_index('Date', inplace=True)
    
    # Returns the schedule of the team from the year selected
    return schedule

# This function takes the strings and dataFrame, and places them onto a blank tKinter window.
def tKinterWindow(teamChoice, schedData, teamRecord, dataSource):

    # This code creates the Tkinter window object and places all our data on it
    root = Tk()
    # This portion of the code allows all the text to fit onto one page, width-wise
    text1 = Text(root, width=100)
    text1.pack()
    text1.insert(END, teamChoice )
    text1.insert(END, schedData)
    text1.insert(END, teamRecord)
    text1.insert(END, dataSource)

    # This makes sure that the window does not close until we exit it
    mainloop()


main()