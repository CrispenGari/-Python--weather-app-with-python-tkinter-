''''
APP NAME:           WEATHER FINDER
DESCRIPTION:        A TKINTER APP THAT ALLOWS PEOPLE TO SEARCH FOR THE WEATHER OF CITIES
DEVELOPED BY:       CRISPEN GARI
TECHNOLOGIES USED:  TKINTER, OPENWEATHERMAP API's, PIL, REQUESTS, AST, JSON
'''
class DataException(Exception):
    pass
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from bs4 import BeautifulSoup
import requests, json, ast
root = Tk()
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
width = 660
height = 500
position_top = int((window_height-height)/2)
position_right = int((window_width-width)/2)
root.geometry(f'{width}x{height}+{position_right}+{position_top}')
root.iconbitmap('main.ico')
main_title="WEATHER FINDER"
root.title(main_title)
root.resizable(False, False)
# Functions
#initial data
data =  {"coord":{"lon":-0.13,"lat":51.51},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],
         "base":"stations","main":{"temp":291.06,"feels_like":289.58,"temp_min":289.26,"temp_max":292.15,"pressure":1017,"humidity":59},"visibility":10000,"wind":{"speed":2.1,"deg":270},"clouds":{"all":98},"dt":1598473952,"sys":{"type":1,"id":1414,"country":"GB","sunrise":1598418257,"sunset":1598468438},"timezone":3600,"id":2643743,"name":"London","cod":200}

main= data['weather'][0]
temperatures = data['main']
API_KEY ="<API_KEY from open weather map>"
def degrees(temp:int):
    return round(temp-273.15, 2)
def close():
    choice = messagebox.askyesnocancel(main_title, f"ARE YOU SURE YOU WANT TO CLOSE THE {main_title} APP?")
    if(choice):
        root.destroy()
    else:
        root.focus()
    return
def Search():
    query = query_string.get()
    if(query != ''):
        url_call = f'https://api.openweathermap.org/data/2.5/weather?q={query}&appid={API_KEY}'
        try:
            temp_data =requests.get(url=url_call).text
            data = ast.literal_eval(temp_data)
            main = data['weather'][0]
            temperatures = data['main']
            if(data == {}):
                raise DataException("An Error Occured while fetching some weather Infomation!!!")
            else:
                # clear the text on the labels and add new text
                for i in range(2):
                    if(i==0):
                        label_cloud['text'] = f""
                        label_main['text'] = f""
                        label_descrip['text'] = f""
                        label_iso['text'] = f""
                        label_city['text'] = f""
                        label_mainheader['text']=''
                    else:
                        # add new text
                        label_cloud['text'] = f"{data['clouds']['all']} %"
                        label_main['text'] = f"{main['main']}"
                        label_descrip['text'] = f"{main['description']}"
                        label_iso['text'] = f"{data['sys']['country']}"
                        label_city['text'] = f"{data['name']}"
                        label_mainheader['text'] = f"Weather Results ({data['name'].upper()})"
                        pass
                #     delete the temperatures that are in the entried and add new ones

                for i in range(2):
                    if(i==0):
                        label_temprature['state'] = 'normal'
                        label_temprature.delete(0,END)
                        label_maxtemprature['state'] = 'normal'
                        label_maxtemprature.delete(0, END)
                        label_mintemprature['state'] = 'normal'
                        label_mintemprature.delete(0, END)
                        label_pressure['state'] = 'normal'
                        label_pressure.delete(0, END)
                        label_humidity['state'] = 'normal'
                        label_humidity.delete(0, END)
                    else:
                        label_temprature.insert(0, f"{degrees(temperatures['temp'])} ℃")
                        label_temprature['state'] = DISABLED
                        label_maxtemprature.insert(0, f"{degrees(temperatures['temp_max'])} ℃")
                        label_maxtemprature['state'] = DISABLED
                        label_mintemprature.insert(0, f"{degrees(temperatures['temp_min'])} ℃", )
                        label_mintemprature['state'] = DISABLED
                        label_pressure.insert(0, f"{temperatures['pressure']} hPa")
                        label_pressure['state'] = DISABLED
                        label_humidity.insert(0, f"{temperatures['humidity']} %")
                        label_humidity['state'] = 'disabled'
                pass
        except DataException as e:
            messagebox.showerror(main_title, e)
        finally:
            query_string.delete(0, END)
            root.after(1000, root.update())
    else:
        pass
    return
weather_icon = ImageTk.PhotoImage(Image.open('weather.ico'))
Label(root, font=('arial', 15, 'bold'), text= main_title,compound=LEFT, image=weather_icon).grid(row=0, column=0, columnspan=10, pady=10)
hr =ttk.Separator(root, orient=HORIZONTAL)
hr.grid(row=1, column =0, columnspan=10, ipadx=330, pady=10,  sticky=W)
Label(root, font=('arial', 12, 'bold'), text= "City Name").grid(row=2, column=0,sticky=W)
query_string = Entry(root, font=('arial', 15), width= 26)
query_string.grid(row=2, column=2, columnspan=5, sticky=E)
btn_search = Button(root, text="Search", width=10, bg="blue", fg="white", bd=0 , font=('arial', 12), relief=SOLID, command=Search)
btn_search.grid(row=2, column=7, sticky=W)
label_mainheader = Label(root, font=('arial', 15, 'bold'), text= f"Weather Results ({data['name'].upper()})",compound=LEFT)
label_mainheader.grid(row=3, column=0, columnspan=10, pady=10)
Label(root, font=('arial', 12, 'bold'), text= "Main",compound=LEFT).grid(row=4, column=0, columnspan=2)
hr =ttk.Separator(root, orient=HORIZONTAL)
hr.grid(row=5, column =0, columnspan=10, ipadx=330, sticky=W)

label_texts = ["CURRENT TEMPERATURE", "MAXIMUM TEMPERATURE","MINIMUM TEMPERATURE", "PREASURE",  "HUMIDITY" ]
for i in range(6, 6+len(label_texts)):
    Label(root, font=('arial', 10), text= label_texts[i-6],compound=LEFT).grid(row=i+1, column=0, sticky=W, padx=2)

# temprerauters
label_temprature = Entry(root, font=('arial', 12, 'bold'), width=10, fg="blue", state=DISABLED)
label_temprature['state'] = 'normal'
label_temprature.insert(0,  f"{degrees(temperatures['temp'])} ℃")
label_temprature['state'] = DISABLED
label_temprature.grid(row=7, column=1, sticky=W, padx=2)

label_maxtemprature = Entry(root, font=('arial', 12, 'bold'), width=10, fg="blue", state=DISABLED)
label_maxtemprature['state'] = 'normal'
label_maxtemprature.insert(0,  f"{degrees(temperatures['temp_max'])} ℃")
label_maxtemprature['state'] = DISABLED
label_maxtemprature.grid(row=8, column=1, sticky=W, padx=2)

label_mintemprature = Entry(root, font=('arial', 12, 'bold'), width=10, fg="blue", state=DISABLED)
label_mintemprature['state'] = 'normal'
label_mintemprature.insert(0,  f"{degrees(temperatures['temp_min'])} ℃",)
label_mintemprature['state'] = DISABLED
label_mintemprature.grid(row=9, column=1, sticky=W, padx=2)

label_pressure = Entry(root, font=('arial', 12, 'bold'), width=10, fg="blue", state=DISABLED)
label_pressure['state'] = 'normal'
label_pressure.insert(0,  f"{temperatures['pressure']} hPa")
label_pressure['state'] = DISABLED
label_pressure.grid(row=10, column=1, sticky=W, padx=2)

label_humidity = Entry(root, font=('arial', 12, 'bold'), width=10, fg="blue", state=DISABLED)
label_humidity['state'] = 'normal'
label_humidity.insert(0,  f"{temperatures['humidity']} %")
label_humidity['state'] = 'disabled'
label_humidity.grid(row=11, column=1, sticky=W, padx=2)

hr =ttk.Separator(root, orient=VERTICAL)
hr.grid(row=7, column =2, rowspan=5, ipady=90, sticky=N)
Label(root, font=('arial', 12, 'bold'), text= "Others",compound=LEFT).grid(row=4, column=3, columnspan=2)

label_texts1 = ["Cloud Cover","Main", "Description","Country Iso2", "City Name"  ]
for i in range(6, 6 + len(label_texts1)):
    Label(root, font=('arial', 10), text=label_texts1[i - 6], compound=LEFT).grid(row=i + 1, column=3, sticky=W, padx=2)
#others
label_cloud = Label(root, font=('arial', 10, 'bold'), text= f"{data['clouds']['all']} %", fg="blue",compound=LEFT)
label_cloud.grid(row=7, column=4, sticky=W, padx=2)
label_main= Label(root, font=('arial',  10, 'bold'), text= f"{main['main']}", fg="blue",compound=LEFT)
label_main.grid(row=8, column=4, sticky=W, padx=2)
label_descrip = Label(root, font=('arial',  10, 'bold'), text= f"{main['description']}", fg="blue",compound=LEFT)
label_descrip.grid(row=9, column=4, sticky=W, padx=2)
label_iso =Label(root, font=('arial',  10, 'bold'), text= f"{data['sys']['country']}", fg="blue",compound=LEFT)
label_iso.grid(row= 10, column=4, sticky=W, padx=2)
label_city=Label(root, font=('arial', 10, 'bold'), text= f"{data['name']}", fg="blue",compound=LEFT)
label_city.grid(row=11, column=4, sticky=W, padx=2)
Button(root, text="Close App", width=10, bg="blue", fg="white", bd=0 , font=('arial', 12),
       relief=SOLID, command=close).grid(row=12, column=7, stick=E)
label_city=Label(root, font=('arial', 10, 'bold'), text= f"{data['name']}", fg="blue",compound=LEFT)
label_city.grid(row=13, column=0, sticky=W, padx=2, columnspan=10)
# root.update()
n_rows =13
n_columns =10
for i in range(n_rows):
    root.grid_rowconfigure(i,  weight =1)
for i in range(n_columns):
    root.grid_columnconfigure(i,  weight =1)
root.mainloop()

# search ="weather in mumbai"
# url = f'https://www.google.com/search?q={search}'
#
# results = requests.get(url)
# print(results)
#
# response = BeautifulSoup(results.text, "html.parser")
# update = response.find('div', class_="BNeawe")
# print(update.text)
# print("hello world")
