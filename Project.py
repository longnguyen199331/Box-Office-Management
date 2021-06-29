import sqlite3

# Create the database and schema tables
db = sqlite3.connect("BoxOffice.sqlite")
db.execute("PRAGMA foreign_keys = ON")
# db.execute("""DROP TABLE Office""")
db.execute("""CREATE TABLE IF NOT EXISTS Movie             (Movie_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, 
           Rating TEXT NOT NULL, Year INTEGER NOT NULL, Genre TEXT NOT NULL, Team_ID INTEGER,
           Rank INTEGER NOT NULL, FOREIGN KEY (Team_ID) REFERENCES Production(Team_ID)
           ON UPDATE CASCADE
            ON DELETE CASCADE,
           FOREIGN KEY (Rank) REFERENCES Office (Movie_rank)
            ON UPDATE CASCADE
            ON DELETE CASCADE)""")

db.execute("""CREATE TABLE IF NOT EXISTS Production(Team_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           Company TEXT NOT NULL)""")

db.execute("CREATE TABLE IF NOT EXISTS Office (Movie_rank INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
           "Movie_name TEXT NOT NULL, Number_ratings INTEGER NOT NULL, Gross INTEGER NOT NULL, "
           "Weeks_in_top INTEGER)")

db.execute("""CREATE TABLE IF NOT EXISTS Producer (Producer_name TEXT PRIMARY KEY NOT NULL, Team_ID INTEGER,
                FOREIGN KEY (Team_ID) REFERENCES Production(Team_ID)
                ON UPDATE CASCADE
                ON DELETE CASCADE)""")

db.execute("""CREATE TABLE IF NOT EXISTS Director (Director_name TEXT PRIMARY KEY NOT NULL, Team_ID INTEGER,
                FOREIGN KEY (Team_ID) REFERENCES Production(Team_ID)
                ON UPDATE CASCADE
                ON DELETE CASCADE)""")


class Movie(object):
    # initializing a Movie object will insert that object attributes into the Movie table
    def __init__(self, id: int, name: str, rating: str, year: int, genre: str, team_id: int, rank: int):
        cursor = db.execute("SELECT * FROM movie WHERE (Movie_ID = ?)", (id,))
        row = cursor.fetchone()

        if row:
            self.id, self.name, self.rating, self.year, self.genre, self.team_id, self.rank = row
        else:
            self.id = id
            self.name = name
            self.rating = rating
            self.year = year
            self.genre = genre
            self.team_id = team_id
            self.rank = rank
            cursor.execute("INSERT INTO Movie VALUES(?,?,?,?,?,?,?)", (id, name, rating, year, genre, team_id, rank))
            cursor.connection.commit()
            print("Movie added: {}".format(self.name))

    def update(self, **kwargs):
        if 'name' in kwargs:
            db.execute("UPDATE Movie SET name = ? WHERE (Movie_ID = ?)", (kwargs['name'], self.id))
        if 'rating' in kwargs:
            db.execute("UPDATE Movie SET rating = ? WHERE (Movie_ID = ?)", (kwargs['rating'], self.id))
        if 'year' in kwargs:
            db.execute("UPDATE Movie SET year = ? WHERE (Movie_ID = ?)", (kwargs['year'], self.id))
        if 'genre' in kwargs:
            db.execute("UPDATE Movie SET genre = ? WHERE (Movie_ID = ?)", (kwargs['genre'], self.id))
        db.commit()

    def delete(self):
        db.execute("DELETE FROM Movie WHERE id = ?", (self.id,))
        db.commit()


class Production(object):
    # initializing a Production object will insert that object attributes into the Production table
    def __init__(self, id: int, company: str):
        cursor = db.execute("SELECT * FROM Production WHERE (Team_ID = ?)", (id,))
        row = cursor.fetchone()

        if row:
            self.id, self.company = row
        else:
            self.id = id
            self.company = company
            cursor.execute("INSERT INTO Production VALUES(?,?)", (id, company))
            cursor.connection.commit()
            print("Production team added: {}".format(self.company))

    def update(self, comp: str):
        db.execute("UPDATE Production SET Company = ? WHERE (Team_ID = ?)", (comp, self.id))
        db.commit()

    def delete(self):
        db.execute("DELETE FROM Production WHERE Team_ID = ?", (self.id,))
        db.commit()


class Office(object):
    # initializing a Office object will insert that object attributes into the Office table
    def __init__(self, rank: int, m_name: str, num_ratings: int, gross: int, weeks: int):
        cursor = db.execute("SELECT * FROM Office WHERE (Movie_Rank = ?)", (rank,))
        row = cursor.fetchone()

        if row:
            self.rank, self.m_name, self.gross, self.num_ratings, self.weeks = row
        else:
            # self.rank = rank
            self.m_name = m_name
            self.gross = gross
            self.num_ratings = num_ratings
            self.weeks = weeks
            cursor.execute("INSERT INTO Office VALUES(?,?,?,?)", (m_name, num_ratings, gross, weeks))
            cursor.connection.commit()
            print("Movie added: {}".format(self.m_name))
            print("Rank: {}".format(self.rank))

    # if a movie is very popular, the rate will increase
    def rate(self, rates):
        self.num_ratings += rates
        db.execute("UPDATE Office SET Number_ratings = ? WHERE (Movie_rank = ?)", (self.num_ratings, self.rank))
        db.commit()

    def update(self, **kwargs):
        if 'name' in kwargs:
            db.execute("UPDATE Office SET Movie_name = ? WHERE (Movie_rank = ?)", (kwargs['name'], self.rank))
        if 'gross' in kwargs:
            db.execute("UPDATE Office SET Gross = ? WHERE (Movie_rank = ?)", (kwargs['gross'], self.rank))
        if 'weeks' in kwargs:
            db.execute("UPDATE Office SET Weeks_in_top = ? WHERE (Movie_rank = ?)", (kwargs['weeks'], self.rank))
        db.commit()

    def delete(self):
        db.execute("DELETE FROM Office WHERE Movie_rank = ?", (self.rank,))
        db.commit()


class Producer(object):
    # initializing a Producer object will insert that object attributes into the Producer table
    def __init__(self, prod_name: str, id: int):
        cursor = db.execute("SELECT * FROM Producer WHERE (Producer_name = ?)", (prod_name,))
        row = cursor.fetchone()

        if row:
            self.prod_name, self.id = row
        else:
            self.id = id
            self.prod_name = prod_name
            cursor.execute("INSERT INTO Producer VALUES(?,?)", (prod_name, id))
            cursor.connection.commit()
            print("Producer added: {}".format(self.prod_name))

    def update(self, prod: str):
        db.execute("UPDATE Producer SET Producer_name = ? WHERE(Producer_name = ?)", (prod, self.prod_name,))
        db.commit()

    def delete(self):
        db.execute("DELETE FROM Producer WHERE Producer_name = ?", (self.prod_name,))


class Director(object):
    # initializing a Director object will insert that object attributes into the Director table
    def __init__(self, d_name: str, id: int):
        cursor = db.execute("SELECT * FROM Director WHERE (Director_name = ?)", (d_name,))
        row = cursor.fetchone()

        if row:
            self.d_name, self.id = row
        else:
            self.id = id
            self.d_name = d_name
            cursor.execute("INSERT INTO Director VALUES(?,?)", (d_name, id))
            cursor.connection.commit()
            print("Director added: {}".format(self.d_name))

    def update(self, director: str):
        db.execute("UPDATE Director SET Director_name = ? WHERE(Director_name = ?)", (director, self.d_name,))
        db.commit()

    def delete(self):
        db.execute("DELETE FROM Director WHERE Director_name = ?", (self.d_name,))


# if a movie is very popular, the rank will change
def update():
    ratings = db.execute("""SELECT Number_ratings FROM Office ORDER BY Number_ratings DESC""").fetchall()

    for i in range(len(ratings)):
        db.execute("UPDATE Office SET Movie_rank = ?"
                   " WHERE Number_ratings = ?", (i - len(ratings), ratings[i][0],))
        db.commit()
    for j in range(len(ratings)):
        db.execute("UPDATE Office SET Movie_rank = ?"
                   " WHERE Number_ratings = ?", (j + 1, ratings[j][0],))
        db.commit()


# Print menu

def menu():
    print("1. Show the database")
    print("2. Add new item")
    print("3. Delete an item")
    print("4. Update the database")
    print("5. Watch a movie")
    print("Q. Quit")


def update_menu():
    print("1. Movie")
    print("2. Box Office")
    print("3. Production Team")
    print("4. Producer")
    print("5. Director")
    print("Q. Quit")


def add_menu():
    print("1. Movie and Box Office")
    print("2. Production Team")
    print("3. Producer")
    print("4. Director")
    print("Q. Quit")


def show_movie_menu():
    print("1. Show movies based on year released")
    print("2. Show movies based on rank")
    print("Q. Quit")


def show_office_menu():
    print("1. Order movies based on gross income")
    print("2. Show movies based on weeks spent in the top of the box office")
    print("Q. Quit")


def m_table():
    print("(ID, name, rating, year, genre, production team ID, rank)")


def o_table():
    print("(rank, name, number of ratings, gross, weeks in top)")


def t_table():
    print("(ID, company)")


def p_table():
    print("(name, team ID)")


def d_table():
    print("(name, team ID)")


if __name__ == '__main__':

    # Add some sample data to Production table
    disNey = Production(1, "Disney")
    marVel = Production(2, "Marvel")
    dC = Production(3, "DC")

    # Add some sample data to Office table
    PH = Office(1, "Pearl Harbor", 100000000, 100000, 5)
    SW = Office(2, "Star Wars", 20000300, 310000, 5)
    SM = Office(3, "Spider Man: Far from home", 4800000, 10000, 4)
    ITT = Office(4, "IT", 4000000, 2100000, 4)
    AEG = Office(5, "Avengers: End Game", 1000000, 10000, 2)
    FRO = Office(6, "Frozen", 15000000, 20000, 2)
    CCO = Office(7, "Coco", 2500000, 15000, 4)
    AQM = Office(8, "Aquaman", 20000, 45000, 3)

    # Add some sample data to Movie table
    starWars = Movie(1, "Star Wars", "G", 1998, "animation, action fiction", 1, 2)
    spiderMan = Movie(2, "Spider Man: Far from home", "PG-13", 2003, "superhero, fantasy, comedy, sci-fi, teen", 2, 3)
    pearlHarbor = Movie(3, "Pearl Harbor", "PG-13", 2001, "war, romance, drama, action, historical drama, epic", 3, 1)
    IT = Movie(4, "IT", "R", 2019, "horror, mystery, thriller, supernatural", 3, 4)
    avengerEnd = Movie(5, "Avengers: Endgame", "PG-13", 2019, "action, superhero, fantasy, adventure, sci-fi", 2, 5)
    frozen = Movie(6, "Frozen", "PG-13", 2013, "Family Features, Cartoon, teen", 1, 6)
    coco = Movie(7, "Coco", "PG-13", 2017, "Family Features, Cartoon, teen", 1, 7)
    aquaman = Movie(8, "Aquaman", "PG-13", 2018, "superhero, fantasy, comedy, sci-fi", 3, 8)

    # Add some sample data to Producer table
    disney_prod = Producer("Rick McCallum", 1)
    disney_prod1 = Producer("Peter Del Vecho", 1)
    disney_prod2 = Producer("Darla K. Anderson", 1)
    marvel_prod1 = Producer("Amy Pascal", 2)
    marvel_prod2 = Producer("Kevin Fiege", 2)
    dC_prod1 = Producer("Michael Bay", 3)
    dC_prod2 = Producer("Roy Lee", 3)
    dC_prod3 = Producer("Peter Safran", 2)

    # Add some sample data to Director table
    disney_director = Director("Andy Muschietti", 1)
    disney_director1 = Director("Chris Buck", 1)
    disney_director2 = Director("Lee Unkrick ", 1)
    marvel_director1 = Director("Jon Watts", 2)
    marvel_director2 = Director("Anthony Russo", 2)
    marvel_director3 = Director("Joe Russo", 2)
    dC_director = Director("Andy Law", 3)
    dC_director1 = Director("James Wan", 3)

    movieName = []  # List containing movie name
    for row in db.execute("SELECT name FROM Movie").fetchall():
        movieName.append(row[0])

    teamName = []  # List containing production company name
    for row in db.execute("SELECT Company FROM Production").fetchall():
        teamName.append(row[0])

    producerName = []  # List containing producer name
    for row in db.execute("SELECT Producer_name FROM Producer").fetchall():
        producerName.append(row[0])

    directorName = []  # List containing director name
    for row in db.execute("SELECT Director_name FROM Director").fetchall():
        directorName.append(row[0])

    update()
    # User Interface
    while True:
        menu()
        selection = input("Welcome to the box office! Please enter one of the choices above: ")
        print("*" * 100)

        if selection == '1':
            while True:
                update_menu()
                choice1 = input("Which database would you like to see: ")
                if choice1 == '1':
                    m_table()
                    print("-" * 50)
                    for row in db.execute("SELECT * FROM Movie"):
                        print(row)
                    print("*" * 100)
                    while True:
                        show_movie_menu()
                        option = input("Please enter one of the choices above: ")
                        if option == '1':
                            select = input("Select the year you want the movies to be from: ")
                            print("*" * 100)
                            movie_list = []
                            for row in db.execute("SELECT name, Year FROM Movie WHERE Year >= ? ORDER BY Year",
                                                  (select,)):
                                movie_list.append(row)
                            if len(movie_list) != 0:
                                for movie in movie_list:
                                    print(movie)
                            else:
                                print("None")
                            print("*" * 100)
                        elif option == '2':
                            select = input("Show the movies in top: ")
                            print("*" * 100)
                            movie_list = []
                            for row in db.execute("SELECT Rank, name FROM Movie WHERE Rank <= ? ORDER BY Rank",
                                                  (select,)):
                                movie_list.append(row)
                            if len(movie_list) != 0:
                                for movie in movie_list:
                                    print(movie)
                            else:
                                print("None")
                            print("*" * 100)
                        elif option == 'Q' or option == 'q':
                            print("*" * 100)
                            break
                elif choice1 == '2':
                    o_table()
                    print("-" * 50)
                    for row in db.execute("SELECT * FROM Office"):
                        print(row)
                    print("*" * 100)
                    while True:
                        show_office_menu()
                        option = input("Please enter one of the choices above: ")
                        if option == '1':
                            select = input("Show Movies grossing at a minimum of: ")
                            print("*" * 100)
                            movie_list = []
                            for row in db.execute(
                                    "SELECT Movie_name, Gross FROM Office WHERE Gross >= ? ORDER BY Gross", (select,)):
                                movie_list.append(row)
                            if len(movie_list) != 0:
                                for movie in movie_list:
                                    print(movie)
                            else:
                                print("None")
                            print("*" * 100)
                        elif option == '2':
                            select = input("Show Movies charting the box office at a minimum of how many weeks? ")
                            print("*" * 100)
                            movie_list = []
                            for row in db.execute(
                                    "SELECT Movie_name, Weeks_in_top FROM Office WHERE Weeks_in_top >= ? ORDER BY Weeks_in_top",
                                    (select,)):
                                movie_list.append(row)
                            if len(movie_list) != 0:
                                for movie in movie_list:
                                    print(movie)
                            else:
                                print("None")
                            print("*" * 100)
                        elif option == 'Q' or option == 'q':
                            print("*" * 100)
                            break
                elif choice1 == '3':
                    t_table()
                    print("-" * 50)
                    for row in db.execute("SELECT * FROM Production"):
                        print(row)
                    print("*" * 100)
                    show_movie = input("Show all movies that have the same production company(type Q to quit): ")
                    if show_movie == 'Q' or show_movie == 'q':
                        break
                    while show_movie not in teamName:
                        print("Company does not exist. Please try again")
                        show_movie = input("Show all movies that have the same production company: ")
                    t_ID = db.execute("SELECT Team_ID FROM Production WHERE Company = ?", (show_movie,)).fetchone()
                    movie_list = []
                    for row in db.execute("SELECT name FROM Movie WHERE Team_ID = ?", (t_ID[0],)):
                        movie_list.append(row[0])
                    if len(movie_list) != 0:
                        print(movie_list)
                    else:
                        print("None")
                    print("*" * 100)
                elif choice1 == '4':
                    p_table()
                    print("-" * 50)
                    for row in db.execute("SELECT * FROM Producer"):
                        print(row)
                    show_producer = input("Show all movies that have the same producer: ")
                    while show_producer not in producerName:
                        print("Producer does not exist. Please try again")
                        show_producer = input("Show all movies that have the same producer: ")
                    t_ID = db.execute("SELECT Team_ID FROM Producer WHERE Producer_name = ?",
                                      (show_producer,)).fetchone()
                    movie_list = []
                    for row in db.execute("SELECT name FROM Movie WHERE Team_ID = ?", (t_ID[0],)):
                        movie_list.append(row[0])
                    if len(movie_list) != 0:
                        print(movie_list)
                    else:
                        print("None")
                    print("*" * 100)
                elif choice1 == '5':
                    d_table()
                    print("-" * 50)
                    for row in db.execute("SELECT * FROM Director"):
                        print(row)
                    show_director = input("Show all movies that have the same director: ")
                    while show_director not in directorName:
                        print("Director does not exist. Please try again")
                        show_director = input("Show all movies that have the same director: ")
                    t_ID = db.execute("SELECT Team_ID FROM Director WHERE Director_name = ?",
                                      (show_director,)).fetchone()
                    movie_list = []
                    for row in db.execute("SELECT name FROM Movie WHERE Team_ID = ?", (t_ID[0],)):
                        movie_list.append(row[0])
                    if len(movie_list) != 0:
                        print(movie_list)
                    else:
                        print("None")
                    print("*" * 100)
                elif choice1 == 'Q' or choice1 == 'q':
                    break
                else:
                    print("Invalid choice. Please try again")
                    print("*" * 100)
                    continue

        elif selection == '2':
            while True:
                add_menu()
                choice2 = input("Which table do you want to add data in: ")
                if choice2 == '1':
                    # val = max(movieID)
                    # m_ID = val + 1
                    # movieID.append(m_ID)
                    m_name = input("Enter the movie name: ")
                    m_rating = input("Enter the movie rating: ")
                    m_year = input("Enter the movie year: ")
                    m_genre = input("Enter the movie genre: ")
                    m_teamID = input("Enter the team ID: ")

                    m_gross = input("Enter the movie gross: ")
                    m_num_ratings = input("Enter the number of ratings: ")
                    m_weeks = input("Enter the number of weeks: ")
                    db.execute("INSERT INTO Office (Movie_name, Number_ratings, Gross, Weeks_in_top) VALUES(?,?,?,?)",
                               (m_name, m_num_ratings, m_gross, m_weeks))
                    m_rank = db.execute("SELECT Movie_rank FROM Office WHERE Movie_name = ?", (m_name,)).fetchone()
                    db.execute("INSERT INTO Movie (name, Rating, Year, Genre, Team_ID, Rank) VALUES(?,?,?,?,?,?)",
                               (m_name, m_rating, m_year, m_genre, m_teamID, m_rank[0],))
                    movieName.append(m_name)
                    update()
                    db.commit()

                    print("Movie: {} was added".format(m_name))
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Movie"):
                        print(row)
                    print("*" * 100)
                elif choice2 == '2':
                    t_company = input("Enter the company name: ")
                    teamName.append(t_company)
                    db.execute("INSERT INTO Production (Company) VALUES(?)", (t_company,))
                    teamName.append(t_company)
                    db.commit()
                    print("Team {} was added".format(t_company))
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Production"):
                        print(row)
                    print("*" * 100)
                elif choice2 == '3':
                    p_name = input("Enter producer name: ")
                    p_ID = input("Enter the team ID: ")
                    producerName.append(p_name)
                    db.execute("INSERT INTO Producer VALUES(?,?)", (p_name, p_ID))
                    db.commit()
                    print("{} was added".format(p_name))
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Producer"):
                        print(row)
                    print("*" * 100)
                elif choice2 == '4':
                    d_ID = input("Enter team ID: ")
                    d_name = input("Enter the director name: ")
                    directorName.append(d_name)
                    db.execute("INSERT INTO Director VALUES(?,?)", (d_name, d_ID))
                    db.commit()
                    print("{} was added".format(d_name))
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Director"):
                        print(row)
                    print("*" * 100)
                elif choice2 == 'Q' or choice2 == 'q':
                    break
                else:
                    print("Invalid choice. Please try again")
                    print("*" * 100)
                    continue

        elif selection == '3':
            while True:
                add_menu()
                choice3 = input("Which table do you want to delete data on: ")
                if choice3 == '1':
                    for row in db.execute("SELECT * FROM Movie"):
                        print(row)
                    print("*" * 100)
                    m_name = input("Enter movie name (or type Q to quit): ")
                    if m_name == 'Q' or m_name == 'q':
                        break
                    while m_name not in movieName:
                        print("Movie does not exist. Please try again")
                        m_name = input("Enter movie name: ")
                    m_rank = db.execute("SELECT Rank FROM Movie WHERE name = ?", (m_name,)).fetchone()
                    db.execute("DELETE FROM Movie WHERE name = ?", (m_name,))
                    db.execute("DELETE FROM Office WHERE Movie_rank = ?", (m_rank[0],))
                    movieName.remove(m_name)
                    update()
                    db.commit()
                    print("Movie {} was deleted".format(m_name))
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Movie"):
                        print(row)
                    print("*" * 100)
                elif choice3 == '2':  # Deleting a production team will also delete every data associated with it
                    for row in db.execute("SELECT * FROM Production"):
                        print(row)
                    print("*" * 100)
                    t_name = input("Enter team name (or type Q to quit): ")
                    if t_name == 'Q' or t_name == 'q':
                        break
                    while t_name not in teamName:
                        print("Production team does not exist. Please try again")
                        t_name = input("Enter team name: ")
                    t_ID = db.execute("SELECT Team_ID FROM Production WHERE Company = ?", (t_name,)).fetchone()
                    m_name = []
                    for row in db.execute("SELECT name FROM Movie WHERE Team_ID =?", (t_ID[0],)):
                        m_name.append(row[0])
                    db.execute("DELETE FROM Production WHERE Company = ?", (t_name,))
                    for movie in m_name:
                        db.execute("DELETE FROM Office WHERE Movie_name = ?", (movie,))
                        movieName.remove(m_name)
                    teamName.remove(t_name)
                    update()  # update the rank
                    db.commit()
                    print("Team {} was deleted".format(t_name))
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Production"):
                        print(row)
                    print("*" * 100)
                elif choice3 == '3':
                    for row in db.execute("SELECT * FROM Producer"):
                        print(row)
                    print("*" * 100)
                    p_name = input("Enter the producer name (or type Q to quit): ")
                    if p_name == 'Q' or p_name == 'q':
                        break
                    while p_name not in producerName:
                        print("Producer does not exist. Please try again")
                        p_name = input("Enter the producer name: ")
                    db.execute("DELETE FROM Producer WHERE Producer_name = ?", (p_name,))
                    producerName.remove(p_name)
                    db.commit()
                    print("Producer {} was deleted".format(p_name))
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Producer"):
                        print(row)
                    print("*" * 100)
                elif choice3 == '4':
                    for row in db.execute("SELECT * FROM Director"):
                        print(row)
                    print("*" * 100)
                    d_name = input("Enter the director name (or type Q to quit): ")
                    if d_name == 'Q' or d_name == 'q':
                        break
                    while d_name not in directorName:
                        print("Director does not exist. Please try again")
                        d_name = input("Enter the director name: ")
                    db.execute("DELETE FROM Director WHERE Director_name = ?", (d_name,))
                    directorName.remove((d_name))
                    db.commit()
                    print("Director {} was deleted".format(d_name))
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Director"):
                        print(row)
                    print("*" * 100)
                elif choice3 == 'Q' or choice3 == 'q':
                    break
                else:
                    print("Invalid choice. Please try again")
                    print("*" * 100)
                    continue

        elif selection == '4':
            while True:
                update_menu()
                choice4 = input("Which table do you want to update: ")
                if choice4 == '1':
                    for row in db.execute("SELECT * FROM Movie"):
                        print(row)
                    print("*" * 100)
                    m_name = input("Enter name of the movie that you want to update (or type Q to quit): ")
                    if m_name == 'Q' or m_name == 'q':
                        break
                    while m_name not in movieName:
                        print("Movie does not exist. Please try again")
                        m_name = input("Enter name of the movie that you want to update: ")
                    m_rank = db.execute("SELECT Rank FROM Movie WHERE name = ?", (m_name,)).fetchone()
                    m_newName = input("Enter the new name (Skip if unchanged): ")
                    if m_newName == '':
                        m_newName = db.execute("SELECT name FROM Movie WHERE name =?", (m_name,)).fetchone()
                        m_newName = m_newName[0]
                    else:
                        movieName.remove(m_name)
                        movieName.append(m_newName)
                    m_rating = input("Enter the new rating (Skip if unchanged): ")
                    if m_rating == '':
                        m_rating = db.execute("SELECT Rating FROM Movie WHERE name =?", (m_name,)).fetchone()
                        m_rating = m_rating[0]
                    m_year = input("Enter the new year (Skip if unchanged): ")
                    if m_year == '':
                        m_year = db.execute("SELECT Year FROM Movie WHERE name =?", (m_name,)).fetchone()
                        m_year = m_year[0]
                    m_genre = input("Enter the new genre (Skip if unchanged): ")
                    if m_genre == '':
                        m_genre = db.execute("SELECT genre FROM Movie WHERE name =?", (m_name,)).fetchone()
                        m_genre = m_genre[0]
                    db.execute("""UPDATE Movie SET name = ?, rating = ?, year = ?, genre = ? WHERE (name = ?)""",
                               (m_newName, m_rating, m_year, m_genre, m_name))
                    db.execute("""UPDATE Office SET Movie_name = ? WHERE (Movie_rank = ?)""",
                               (m_newName, m_rank[0]))
                    db.commit()
                    print("Movie updated!")
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Movie"):
                        print(row)
                    print("*" * 100)
                elif choice4 == '2':
                    for row in db.execute("SELECT * FROM Office"):
                        print(row)
                    print("*" * 100)
                    m_name = input("Enter the name of the movie that you want to update (or type Q to quit): ")
                    if m_name == 'Q' or m_name == 'q':
                        break
                    while m_name not in movieName:
                        print("Movie does not exist. Please try again")
                        m_name = input("Enter the name of the movie that you want to update: ")
                    m_newName = input("Enter the new name (Skip if unchanged): ")
                    if m_newName == '':
                        m_newName = db.execute("SELECT Movie_name FROM Office WHERE Movie_name =?",
                                               (m_name,)).fetchone()
                        m_newName = m_newName[0]
                    else:
                        movieName.remove(m_name)
                        movieName.append(m_newName)
                    m_num_ratings = input("Enter the new number of ratings (Skip if unchanged): ")
                    if m_num_ratings == '':
                        m_num_ratings = db.execute("SELECT Number_ratings FROM Office WHERE Movie_name =?",
                                                   (m_name,)).fetchone()
                        m_num_ratings = m_num_ratings[0]
                    m_gross = input("Enter the new gross (Skip if unchanged): ")
                    if m_gross == '':
                        m_gross = db.execute("SELECT Gross FROM Office WHERE Movie_name =?", (m_name,)).fetchone()
                        m_gross = m_gross[0]
                    m_weeks = input("Enter the weeks in top (Skip if unchanged): ")
                    if m_weeks == '':
                        m_weeks = db.execute("SELECT Weeks_in_top FROM Office WHERE Movie_name =?",
                                             (m_name,)).fetchone()
                        m_weeks = m_weeks[0]
                    db.execute("""UPDATE Office SET Movie_name = ?, Number_ratings = ?, Gross = ?, Weeks_in_top = ? 
                                WHERE (Movie_name = ?)""", (m_newName, m_num_ratings, m_gross, m_weeks, m_name,))
                    db.execute("""UPDATE Movie SET name = ? 
                                WHERE name = ?""", (m_newName, m_name,))
                    update()  # Update the rank
                    db.commit()
                    print("Office updated!")
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Office"):
                        print(row)
                    print("*" * 100)
                elif choice4 == '3':
                    for row in db.execute("SELECT * FROM Production"):
                        print(row)
                    print("*" * 100)
                    t_name = input("Enter the team company (or type Q to quit): ")
                    if t_name == 'Q' or t_name == 'q':
                        break
                    while t_name not in teamName:
                        print("Team does not exist. Please try again")
                        t_name = input("Enter the team company: ")
                    t_company = input("Enter the new company (Skip if unchanged): ")
                    if t_company == '':
                        t_company = db.execute("SELECT Company FROM Production WHERE Company =?", (t_name,)).fetchone()
                        t_company = t_company[0]
                    else:
                        teamName.remove(t_name)
                        teamName.append(t_company)
                    db.execute("UPDATE Production SET Company = ? WHERE Company = ?", (t_company, t_name))
                    db.commit()
                    print("Production team updated!")
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Production"):
                        print(row)
                    print("*" * 100)
                elif choice4 == '4':
                    for row in db.execute("SELECT * FROM Producer"):
                        print(row)
                    print("*" * 100)
                    p_name = input("Enter the producer name (or type Q to quit): ")
                    if p_name == 'Q' or p_name == 'q':
                        break
                    while p_name not in producerName:
                        print("Producer does not exist. Please try again")
                        p_name = input("Enter the producer name: ")
                    p_ID = input("Enter the new team ID (Skip if unchanged): ")
                    if p_ID == '':
                        p_ID = db.execute("SELECT Team_ID FROM Producer WHERE Producer_name =?", (p_name,)).fetchone()
                        p_ID = p_ID[0]
                    db.execute("UPDATE Producer SET Team_ID = ? WHERE Producer_name = ?", (p_ID, p_name))
                    db.commit()
                    print("Producer updated!")
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Producer"):
                        print(row)
                    print("*" * 100)
                elif choice4 == '5':
                    for row in db.execute("SELECT * FROM Director"):
                        print(row)
                    print("*" * 100)
                    d_name = input("Enter the director name (or type Q to quit): ")
                    if d_name == 'Q' or d_name == 'q':
                        break
                    while d_name not in directorName:
                        print("Producer does not exist. Please try again")
                        d_name = input("Enter the producer name: ")
                    d_ID = input("Enter the new team ID (Skip if unchanged): ")
                    if d_ID == '':
                        d_ID = db.execute("SELECT Team_ID FROM Director WHERE Director_name =?", (d_name,)).fetchone()
                        d_ID = d_ID[0]
                    db.execute("UPDATE Director SET Team_ID = ? WHERE Director_name = ?", (d_ID, d_name))
                    db.commit()
                    print("Director updated!")
                    print("*" * 100)
                    for row in db.execute("SELECT * FROM Director"):
                        print(row)
                    print("*" * 100)
                elif choice4 == 'Q' or choice4 == 'q':
                    break
                else:
                    print("Invalid choice. Please try again")
                    continue

        elif selection == '5':
            m_table()
            print("-" * 50)
            for row in db.execute("SELECT * FROM Movie"):
                print(row)
            print("*" * 100)
            choice5 = input("Select a movie to watch: ")
            while choice5 not in movieName:
                print("Movie does not exist. Please try again: ")
                choice5 = input("Select a movie to watch: ")
            num_ratings = db.execute("SELECT Number_ratings FROM Office WHERE Movie_name =?", (choice5,)).fetchone()
            m_gross = db.execute("SELECT Gross FROM Office WHERE Movie_name =?", (choice5,)).fetchone()
            db.execute("UPDATE Office SET Number_ratings = ?, Gross = ? WHERE Movie_name =?",
                       (num_ratings[0] + 1, m_gross[0] + 20, choice5))
            update()
            db.commit()
            print("Thanks for watching {}".format(choice5))
            print("*" * 100)

        elif selection == 'Q' or selection == 'q':
            print("Thanks for visiting, see you later!")
            break

        else:
            print("Invalid choice. Please try again")
            print("*" * 100)
            continue

    db.close()
