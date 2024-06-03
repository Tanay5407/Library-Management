import mysql.connector
import typer
import tabulate
import inquirer
#mydb = mysql.connector.connect(
#  host="localhost",
#  user="root",
#  password="pass",
#  database = "IP_PROJECT"
#)


def BookName():
    """Fetches data on the basis of the name of the book from SQL database, prints it (tabulated) and returns a list."""
    name:str = typer.prompt("Enter the name of the Book")
    cursor.execute(f"SELECT * FROM BOOKS WHERE NAME = {name}")
    res = cursor.fetchone()
    res = list[list]
    Headers = ["NAME", "AUTHOTR", "ISBN", "DATE OF PUBLISHING","TAGS", "STATUS", "TOTAL"]
    print(tabulate(res, headers = Headers))
    return res


def ISBN():
    isbn:int = typer.prompt("Enter the ISBN ID of the Book:")
    cursor.execute(f"SELECT * FROM BOOKS WHERE ISBN = {isbn}")
    res = cursor.fetchone()
    res = list(res)
    Headers = ["NAME", "AUTHOTR", "ISBN", "DATE OF PUBLISHING","TAGS", "STATUS", "TOTAL"]
    print(tabulate(res, headers = Headers))
    return res

def Search(parent):
    ch2  = inquirer.list_input("Search By:" ,choices = ["BookName", "ISBN", "Author", "DateOfPublishing", "back"])
    if ch2 == "back":
        f2 = globals()[parent]
        f2()
    else:
        f2 = globals()[ch2]
        f2()


def Nofilter():
    cursor.execute("SELECT * FROM customers")
    res = cursor.fetchall()
    res = list(res)
    Headers = ["NAME", "AUTHOTR", "ISBN", "DATE OF PUBLISHING","TAGS", "STATUS", "TOTAL"]
    print(tabulate(res, headers = Headers))


def Library():
    #Logic for Library
    choice1 = inquirer.list_input("Filters? or Nah!", choices = ["NoFilter","Search", "Date", "Tags","back"])
    if choice1 == "back":
        main()
    else:
        func1 = globals()[choice1]
        func1("Library")
    pass
def AddBook():
    #Logic to Add book
    pass
def RemoveBook():
    #Logic to remove book
    pass
def IssueBook():
    #Logic to Issue book
    pass
def ReturnBook():
    #Logic to Return book
    pass
def main():
    que = inquirer.list_input("What do you want to do?", choices = [Library.__name__, AddBook.__name__, RemoveBook.__name__, IssueBook.__name__, ReturnBook.__name__])
    func = globals()[que]
    func()
if __name__ == "__main__":
    cursor = mydb.cursor()
    typer.run(main)
    pass

