# Required End Points for Rest API:

Post Coordinates of Seeker (lat, lon) => (Success)

Post Coordinates of Hider (lat, lon) => (Success)

Get Coordinates of Seeker () => (lat, lon)

Get Coordinates of Hider () => (lat, lon)




Ask Question (Question ID) => (Success)

Answer Current Question () => (Success)

Veto Current Question () => (Success)

Get Current Curses Info () => (For every Curse: Curse ID, Name, Description)

Get Currently Asked Question Info () => (Question ID, Name, Description, Time Left)

Get Previously Asked Questions Info () => (For Every Question: Question ID, Name, Description, Answer)

Get all Questions () => (For Every Question: ID, Name, Description, Already Asked)

Complete Curse (Curse ID) => (Success)

Get Card Hand Info () => (For every Card in Hand: Card ID, Name, Description, Type (string))

Discard Card (Card ID) => (Success)

Use Card (Card ID) => (Success)

Swap Hider and Seeker() => (Success)

Start Game ()  => (Success)

End Game () => (Success)

Get Game Info () => (Current Game Timer, Hider Name, Seeker Name)

Get Hider Info () => (Lat, Lon, Bus Station Name, Bus Station Lat, Bus Station Lon, Bus Station Altitude, Bus Station Bezirk, Bus Station Gemeinde, Distance to nearest Train Station, Distance to nearest Mountain, Distance to nearest Minigold, Distance to nearest Museum)

Get Seeker Info () => (Lat, Lon, Altitude, Bezirk, Gemeinde, Distance to nearest Train Station, Distance to nearest Mountain, Distance to nearest Minigold, Distance to nearest Museum)

Get All Bus Routes () => (For Every Routes: Route Id, Route Name)

Set_Hiding_Bus_Stop (Bus_Stop_ID) => (Success)

Get_Bus_Stops () => (For every Bus Stop that has not been marked of: Bus_Stop_ID, Bus_Stop_Name, Bus_Stop_Lat, Bus_Stop_Lon)

Get_Bus_Stops_In_Range () => (For every Bus Stop that is within 400 meters: Bus_Stop_ID, Bus_Stop_Name, Bus_Stop_Lat, Bus_Stop_Lon)

Exists () => (Success) (Explanation: This should be a test method for the client to see if the server exists. Should alwayss send 200 Success)