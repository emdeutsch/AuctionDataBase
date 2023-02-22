-- Delete any existing tables with the same names
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Bid;

-- Create the Item table
CREATE TABLE Item (
    ItemID INTEGER PRIMARY KEY,
    Name TEXT,
    Category TEXT,
    Currently FLOAT,
    FirstBid FLOAT,
    NumberofBids FLOAT,
    Started DATETIME,
    Ends DATETIME,
    Country Text,
    Location Text,
    Description Text
);

-- Create the AuctionUser table
CREATE TABLE User (
    UserID TEXT PRIMARY KEY,
    Rating INTEGER,
    Country TEXT,
    Location TEXT,
    Type TEXT
);

-- Create the Bid table
CREATE TABLE Bid (
    ItemID INTEGER,
    UserID INTEGER,
    Time DATETIME,
    Amount FLOAT,
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);
