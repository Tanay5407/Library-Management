import mysql.connector
import typer
import tabulate
import inquirer
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pass",
  database = "IP_PROJECT"
)



def main():
    """This function basically is a container for the starting statements. Calls other functions as per user input."""
    que = inquirer.list_input("What do you want to do?", choices = [Library.__name__, AddBook.__name__, RemoveBook.__name__, IssueBook.__name__, ReturnBook.__name__])

    # You will see the next two lines of code multiple times in the program, what they basically do is call the function by the name(of the function to be called) given as a string. 
    # How does it work? Well...
    # The globals() function basically returns a dictionary of all the methods that are active in the program, which has names(strings) as keys and functions as values.
    # The first line retrieves the function from the dictionary and the second line calls it.
    
    func = globals()[que]
    func()

def Library():
    #Logic for Library
    choice1 = inquirer.list_input("Filters? or Nah!", choices = ["NoFilter","Search", "Year", "Author", "Tags","back"])
    if choice1 == "back":
        main()
    else:
        func1 = globals()[choice1]
        func1("Library")

def Search(parent):
    """Contains choices, and calls other functions to search."""
    ch2  = inquirer.list_input("Search By:" ,choices = ["BookName", "ISBN", "back"])
    if ch2 == "back":
        f2 = globals()[parent]
        f2()
    else:
        f2 = globals()[ch2]
        res = f2()
        return res


def BookName():
    """Fetches data on the basis of the name of the book from SQL database, prints it (tabulated) and returns a list."""
    ch4  = inquirer.list_input("Are you sure?" ,choices = ["Continue", "back"])
    if ch4 == "back":
        f5 = globals()["Search"]
        f5()
    else:
        name:str = typer.prompt("Enter the name of the Book")
        cursor.execute(f"SELECT * FROM BOOKS WHERE NAME = {name}")
        res = cursor.fetchone()
        res = list(res)
        Headers = ["NAME", "AUTHOTR", "ISBN", "YEAR OF PUBLISHING","TAGS", "STATUS", "TOTAL"]
        print(tabulate(res, headers = Headers))
        return res


def ISBN():
    """Fetches data on the basis of the ISBN of the book from SQL database, prints it (tabulated) and returns a list."""
    ch4  = inquirer.list_input("Are you sure?" ,choices = ["Continue", "back"])
    if ch4 == "back":
        f3 = globals()["Search"]
        f3()
    else:
        isbn = int(typer.prompt("Enter the ISBN ID of the Book:"))
        cursor.execute(f"SELECT * FROM BOOKS WHERE ISBN = {isbn}")
        res = cursor.fetchone()
        res = list(res)
        Headers = ["NAME", "AUTHOTR", "ISBN", "YEAR OF PUBLISHING","TAGS", "STATUS", "TOTAL"]
        print(tabulate(res, headers = Headers))
        return res

def Author():
    """Fetches data on the basis of the author of the book from SQL database, prints it (tabulated) and returns a list."""
    ch7  = inquirer.list_input("Are you sure?" ,choices = ["Continue", "back"])
    if ch7 == "back":
        f8 = globals()["Library"]
        f8()
    else:
        Au = int(typer.prompt("Enter the Author of the Book:"))
        cursor.execute(f"SELECT * FROM BOOKS WHERE AUTHOR = {Au}")
        res = cursor.fetchall()
        res = list(res)
        Headers = ["NAME", "AUTHOTR", "ISBN", "YEAR OF PUBLISHING","TAGS", "STATUS", "TOTAL"]
        print(tabulate(res, headers = Headers))
        return res
    

def Nofilter():
    cursor.execute("SELECT * FROM BOOKS")
    res = cursor.fetchall()
    res = list(res)
    Headers = ["NAME", "AUTHOTR", "ISBN", "YEAR OF PUBLISHING","TAGS", "STATUS", "TOTAL"]
    print(tabulate(res, headers = Headers))


def Date():
    ch5  = inquirer.list_input("Are you sure?" ,choices = ["Continue", "back"])
    if ch5 == "back":
        f6 = globals()["Library"]
        f6()
    else:
        date_ini = typer.prompt("Enter the starting year(YYYY) for the search:")
        date_fin = typer.prompt("Enter the ending year(YYYY) for the search:")
        cursor.execute(f"SELECT * FROM BOOKS WHERE DATEOFPUBLISHING > '{date_ini}' and DATEOFPUBLISHING < '{date_fin}'")
        res = cursor.fetchall()
        res = list(res)
        Headers = ["NAME", "AUTHOTR", "ISBN", "YEAR OF PUBLISHING","TAGS", "STATUS", "TOTAL"]
        print(tabulate(res, headers = Headers))
        return res
    
def Tags():
    ch6  = inquirer.list_input("Are you sure?" ,choices = ["Continue", "back"])
    if ch6 == "back":
        f7 = globals()["Library"]
        f7()
    else:
        t = typer.prompt("Enter the tags separated by comma.")
        ls = t.split(seperator = ",")
        for item in ls:
            item.strip()
        s = "%".join(ls)
        cursor.execute(f"SELECT * FROM BOOKS WHERE TAGS LIKE '%{s}%'")
        res = cursor.fetchall()
        res = list(res)
        Headers = ["NAME", "AUTHOTR", "ISBN", "YEAR OF PUBLISHING","TAGS", "STATUS", "TOTAL"]
        print(tabulate(res, headers = Headers))
        return res

def AddBook():
    book_name = typer.prompt("Enter the name of the book ")
    Auth_name = typer.prompt("Enter the name of the author ")
    isbn = int(typer.prompt("Enter the ISBN of the book "))
    dop = typer.prompt("Enter the year of publishing of the book(YYYY) ")
    tags = typer.prompt("Enter the tags of the book(separated by comma) ")
    stat = int(typer.prompt("Enter the status of the book "))
    total = int(typer.prompt("Enter the total number of books "))
    sql = "INSERT INTO BOOKS (NAME, AUTHOR, ISBN, YEAROFPUBLISHING, TAGS, STATUS, TOTAL) VALUES (%s, %s,%s, %s,%s, %s,%s)"
    val = (book_name, Auth_name, isbn, dop, tags, stat, total)
    cursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "record inserted.")

def RemoveBook():
    """Removes a specific book by search."""
    book = Search("RemoveBook")
    sql = f"DELETE FROM BOOKS WHERE NAME = '{book[0]}'"
    cursor.execute(sql)
    mydb.commit()
    print(cursor.rowcount, "record(s) deleted")

def IssueBook():
    id = typer.prompt("Enter the SchoolID of the borrower ")
    l = Search("IssueBook")
    sql = f"UPDATE BOOKS SET STATUS = STATUS+1 WHERE NAME = '{l[0]}'"
    cursor.execute(sql)
    # write to .csv or .txt logic for logs
    mydb.commit()
    print(cursor.rowcount, "record(s) affected")

def ReturnBook():
    id = typer.prompt("Enter the SchoolID of the person ")
    l = Search("ReturnBook")
    sql = f"UPDATE BOOKS SET STATUS = STATUS-1 WHERE NAME = '{l[0]}'"
    cursor.execute(sql)
    # write to .csv or .txt logic for logs
    mydb.commit()
    print(cursor.rowcount, "record(s) affected")




if __name__ == "__main__":
    cursor = mydb.cursor()
    typer.run(main)

