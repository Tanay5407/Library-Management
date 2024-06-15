import mysql.connector
import typer
import tabulate
import inquirer
from datetime import date
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pass",
  database = "ip_project"
)

global Headers 
Headers = ["NAME", "AUTHOR", "ISBN", "YEAR OF PUBLISHING","TAGS", "STATUS", "TOTAL"]

def main():
    """This function basically is a container for the starting statements. Calls other functions as per user input."""
    que = inquirer.list_input("What do you want to do?", choices = ["Library", "AddBook", "RemoveBook", "IssueBook", "ReturnBook"])

    # You will see the next two lines of code multiple times in the program, what they basically do is call the function by the name(of the function to be called) given as a string. 
    # How does it work? Well...
    # The globals() function basically returns a dictionary of all the methods that are active in the program, which has names(strings) as keys and functions as values.
    # The first line retrieves the function from the dictionary and the second line calls it.
    
    func = globals()[que]
    func()

def Library():
    """Allows you to look at books. Filtering/Searching included."""
    choice1 = inquirer.list_input("Filters? or Nah!", choices = ["NoFilter","Search", "Year", "Author", "Tags","back"])
    if choice1 == "back":
        main()
    else:
        func1 = globals()[choice1]
        func1("Library")

def AddBook():
    """Used to add a new book to the library."""
    book_name = typer.prompt("Enter the name of the book ").lower()
    Auth_name = typer.prompt("Enter the name of the author(s) (separated by comma) ").lower()
    isbn = typer.prompt("Enter the ISBN of the book ")
    dop = typer.prompt("Enter the year of publishing of the book(YYYY) ")
    tags = typer.prompt("Enter the tags of the book(separated by comma) ").lower()
    stat = int(typer.prompt("Enter the number of books lent "))
    total = int(typer.prompt("Enter the total number of books "))
    sql = "INSERT INTO BOOKS (NAME, AUTHOR, ISBN, YEAR_OF_PUBLISHING, TAGS, STATUS, TOTAL) VALUES (%s, %s,%s, %s,%s, %s,%s)"
    val = (book_name, Auth_name, isbn, dop, tags, stat, total)
    cursor.execute(sql, val)
    mydb.commit()
    print(book_name, "Added.")


def RemoveBook():
    """Removes a specific book by search."""
    book = Search("RemoveBook")
    sql = f"DELETE FROM BOOKS WHERE NAME = '{book[0]}'"
    cursor.execute(sql)
    mydb.commit()
    print(cursor.rowcount, "record(s) deleted")

def IssueBook():
    """Can be used to issue a book."""
    id = typer.prompt("Enter the SchoolID of the borrower ")
    l = Search("IssueBook")
    sql = f"UPDATE BOOKS SET STATUS = STATUS+1 WHERE NAME = '{l[0]}'"
    cursor.execute(sql)
    # write to .csv or .txt logic for logs
    mydb.commit()
    print(l[0], "Issued")

def ReturnBook():
    """Can be used when the book is returned."""
    id = typer.prompt("Enter the SchoolID of the person ")
    l = Search("ReturnBook")
    sql = f"UPDATE BOOKS SET STATUS = STATUS-1 WHERE NAME = '{l[0]}'"
    cursor.execute(sql)
    # write to .csv or .txt logic for logs
    mydb.commit()
    print(l[0], "Returned")

def NoFilter(parent):
    """Daughter function of Library, displays all the books without filter."""
    cursor.execute("SELECT * FROM BOOKS")
    res = cursor.fetchall()
    res = list(res)
    print(tabulate.tabulate(res, headers = Headers, tablefmt="rounded_outline"))

def Search(parent):
    """Calls other functions to search."""
    ch2  = inquirer.list_input("Search By:" ,choices = ["BookName", "ISBN", "back"])
    if ch2 == "back":
        f2 = globals()[parent]
        f2()
    else:
        f2 = globals()[ch2]
        res = f2()
        return res

def Year(parent):
    """Daughter function of Library, searches in a range if years."""
    ch5  = inquirer.list_input("Are you sure?" ,choices = ["Continue", "back"])
    if ch5 == "back":
        f6 = globals()["Library"]
        f6()
    else:
        date_ini = typer.prompt("Enter the starting year(YYYY) for the search:")
        date_fin = typer.prompt("Enter the ending year(YYYY) for the search:")
        cursor.execute(f"SELECT * FROM BOOKS WHERE YEAR_OF_PUBLISHING > '{date_ini}' and YEAR_OF_PUBLISHING < '{date_fin}'")
        res = cursor.fetchall()
        res = list(res)
        print(tabulate.tabulate(res, headers = Headers, tablefmt="rounded_outline"))
        return res

def Author(parent):
    """Daughter function of Library, fetches data on the basis of the author of the book from SQL database, prints it (tabulate.tabulated) and returns a list."""
    ch7  = inquirer.list_input("Are you sure?" ,choices = ["Continue", "back"])
    if ch7 == "back":
        f8 = globals()["Library"]
        f8()
    else:
        Au = typer.prompt("Enter the Author of the Book ").lower()
        cursor.execute(f"SELECT * FROM BOOKS WHERE AUTHOR like '%{Au}%'")
        res = cursor.fetchall()
        res = list(res)
        print(tabulate.tabulate(res, headers = Headers, tablefmt="rounded_outline"))
        return res
    
def Tags(parent):
    """Daughter function of Library, filters books on the basis of tags."""
    ch6  = inquirer.list_input("Are you sure?" ,choices = ["Continue", "back"])
    if ch6 == "back":
        f7 = globals()["Library"]
        f7()
    else:
        t = typer.prompt("Enter the tags separated by comma ").lower()
        ls = t.split(",")
        for item in ls:
            item.strip()
        s = "%".join(ls)
        cursor.execute(f"SELECT * FROM BOOKS WHERE TAGS LIKE '%{s}%'")
        res = cursor.fetchall()
        res = [list(item) for item in res]
        print(tabulate.tabulate(res, headers = Headers, tablefmt="rounded_outline"))
        return res

def BookName():
    """Daughter function of Search, fetches data on the basis of the name of the book from SQL database, prints it (tabulate.tabulated) and returns a list."""
    ch4  = inquirer.list_input("Are you sure?" ,choices = ["Continue", "back"])
    if ch4 == "back":
        f5 = globals()["Search"]
        f5()
    else:
        name:str = typer.prompt("Enter the name of the Book ").lower()
        cursor.execute(f"SELECT * FROM BOOKS WHERE NAME = '{name}'")
        res = cursor.fetchone()
        r1 = make_tab_ready(res)
        print(tabulate.tabulate(r1, headers = Headers, tablefmt="rounded_outline"))
        return res

def ISBN():
    """Daughter function of Search, fetches data on the basis of the ISBN of the book from SQL database, prints it (tabulate.tabulated) and returns a list."""
    ch4  = inquirer.list_input("Are you sure?" ,choices = ["Continue", "back"])
    if ch4 == "back":
        f3 = globals()["Search"]
        f3()
    else:
        isbn = typer.prompt("Enter the ISBN ID of the Book ")
        cursor.execute(f"SELECT * FROM BOOKS WHERE ISBN = {isbn}")
        res = cursor.fetchone()
        r1 = make_tab_ready(res)
        print(tabulate.tabulate(r1, headers = Headers, tablefmt="rounded_outline"))
        return res


def continue_or_exit():
    ch = inquirer.list_input("Do you want to Continue or Exit?", choices = ["Continue", "Exit"])
    if ch=="Continue":
        main()
    else:
        exit()


def make_tab_ready(l:tuple):
    l = list(l)
    l1 = []
    for i in l:
        if type(i)==int:
            l1.append(str(i))
        else:
            l1.append(i)
    l2 = [l1[:]]
    return l2
if __name__ == "__main__":
    cursor = mydb.cursor()
    typer.run(main)



