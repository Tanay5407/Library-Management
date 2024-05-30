import mysql.connector
import customtkinter as tk 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="pass",
  database = "IP_PROJECT"
)


class SplashScreen:
    def __init__(self, master):
      self.master = master
      #Frame
      self.bars = tk.Frame(self.master, width = 200, height = 300)
      self.bars.pack()
       #Buttons
      
class Window:
   def __init__(self,master) :
      self.master = master
cursor = mydb.cursor()
root = tk.Tk()
window = SplashScreen(root)
root.mainloop()
