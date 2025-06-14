# Needed Lists and Databases in Program


## Temporary Tables 

These are going to be temporary tables in a MariaDB. These are going to hold infos about the game, and will be deleted at the end of a round

List of all Cards:
Card ID, Status (In Hand, In Deck, In Effect)

List of all Curses in Effect:
Curse ID, AskedOn

List of all Questions:
Question ID, Status (Not Asked, Currently Asked, Previously Asked), Answer, AskedOn (Time where Question was asked)




## Global Variables/Dictionaries in the Server

These Values will be saved as dictionaries in the flask server and will be global for easy access everywhere

HiderInfo: 
Lat, Lon, Bus Station ID

SeekerInfo: 
Lat, Lon


## Permanent Tables

These are persistent tables, not to be deleted after the game

RO_Geodata: Contains info about bus stations, bus routes, Points of interrest, and Administrative Region Boundaries
RO_Carddata: Contains info about the Cards: name, description, type (Time Bonus, Curse, Power Up)
RO_Questiondata: Conains info about the Questions: name, description, type (Comparing, Measuring, Thermometer, Radar, Photo), Time (minutes), Num Of Cards to Choose From