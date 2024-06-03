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
def Library():
    #Logic for Library
    
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
    #cursor = mydb.cursor()
    typer.run(main)
    pass
