from tkinter import (Tk, Frame, Button, messagebox, Label, Toplevel, Radiobutton, Entry,Canvas, Text,  OptionMenu, PhotoImage, StringVar, N, S, E, W, filedialog)
from tkinter.ttk import Combobox, Treeview, Scrollbar
import simple_moving_average as sma
import ar_model as ar
import single_exponential_smoothing as ses
import weighted_moving_average as wma
import dataprep as dp
import matplotlib 
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# =============================================================================
# Die Klasse Gui wird in der Main Methode aufgerufen und baut das Benutzerinteface sowie die grundsätliche Navigation
# durch das Programm auf.
# =============================================================================

class Gui(Tk):
    
    #Baut das zugrundeliegende Fenster auf und ermöglicht somit, diesem weitere Elemente hinzuzufügen
      
    def __init__(self):
        
        Tk.__init__(self)
        
        global SCREEN_WIDTH
        global SCREEN_HEIGHT
                
        # Es wurde für das Programm eine Auflösung von 1600x900 Pixeln gewählt. Das Fenster kann nicht verändert werden.
        self.window_root = self
        self.window_width = 1600
        self.window_height = 900
        self.window_root.resizable(False, False)
        
        self.frame_root = Frame(self.window_root)
        self.frame_root.grid_rowconfigure(0, weight = 1)
        self.frame_root.grid_columnconfigure(0, weight = 1)
        
        # Liest Informationen über die verwendetet Bildschirmauflösung des Benutzers ein
        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()
        
        window_start_x = SCREEN_WIDTH/2 - self.window_width/2
        window_start_y = SCREEN_HEIGHT/2 - self.window_height/2
        
        # Positioniert das Fenster durch die eingelesenen Informationen in der Mitte des Bildschirms
        self.geometry("%dx%d+%d+%d" %(self.window_width, self.window_height, window_start_x, window_start_y - 35))
        
        # Dictionary, in dem im Folgenden die erstellten Seiten der Prognosemethoden gespeichert werden.
        self.frames = {}

        self.create_start_page()
        
        
# =============================================================================
#     Erstellt die Startseite des Programms und speichert diese in self.frames
# =============================================================================
    
    def create_start_page(self):
        
        frame = PageStart(self.window_root)
        self.frames["PageStart"] = frame
        frame.grid(row = 0, column = 0, sticky = "nsew")
        
# =============================================================================
#     Erstellt die Seiten der Einfachen Exponentiellen Glättung und speichert diese in self.frames
# =============================================================================
    
    def create_ses_page(self):
        
        for F in (SinExpSmthPageOverview,
                  SinExpSmthPageRemoveTrendAndSeasonality, 
                  SinExpSmthPageResultForecast, 
                  SinExpSmthPageAddTrendAndSeasonality):
            
            frame = F(self.window_root)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
            
# =============================================================================
#     Erstellt die Seiten des Gewichteten Gleitenden Durchschnitts und speichert diese in self.frames
# =============================================================================
    
    def create_wma_page(self):
        
        for F in (WeightMovAvgPageOverview,
                  WeightMovAvgPageRemoveTrendAndSeasonality, 
                  WeightMovAvgPageResultForecast,
                  WeightMovAvgPageAddTrendAndSeasonality):
            
            frame = F(self.window_root)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
    
# =============================================================================
#     Erstellt die Seiten des Einfachen Gleitenden Durchschnitts und speichert diese in self.frames
# =============================================================================
    
    def create_sma_page(self):

        for F in (SimMovAvgPageOverview,
                  SimMovAvgPageRemoveTrendAndSeasonality,
                  SimMovAvgPageResultForecast,
                  SimMovAvgPageAddTrendAndSeasonality):
            
            frame = F(self.window_root)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

# =============================================================================
#     Erstellt die Seiten des Einfachen Gleitenden Durchschnitts und speichert diese in self.frames
# =============================================================================
     
    def create_ar_page(self):
            
        for F in (ArModelPageOverview,
                  ArModelPageRemoveTrendAndSeasonality,
                  ArModelPageResultForecast, 
                  ArModelPageAddTrendAndSeasonality):
            
            frame = F(self.window_root)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        
# =============================================================================
#     Erhält als Parameter ein Key für die ausgewählte Seite, findet die dazugehörigen Daten in self.frames und 
#     schiebt diese Seite anschließend in den Vordergrund
# =============================================================================
    
    def show_frame(self, cont):
    
        frame = self.frames[cont]
        frame.tkraise()
        self.window_root.title(cont)
    
# =============================================================================
# Erstellt die Startseite des Programms. Das Fenster wird in 5 Bereiche anufgeteilt. In dem mittleren Bereich können       
# die Prognosemethoden ausgewählt werden. Der obere Bereich ist für die Datenauswahl konzipiert.
# =============================================================================
    
class PageStart(Frame):
    
   def __init__(self, window_root):
        
       Frame.__init__(self, window_root)
       
       self.grid_rowconfigure(0, weight = 1)
       self.grid_columnconfigure(0, weight = 1)
       
       self.create_frame_north(window_root)
       self.create_frame_south(window_root)
       self.create_frame_east(window_root)
       self.create_frame_west(window_root)
       self.create_frame_middle(window_root)
      
        
# =============================================================================
#    Erstellt den nördlichen Bereich des Fensters. Enthalten sind Buttons zur Datenauswahl.
# =============================================================================
    
   def create_frame_north(self, window_root):
       
       self.frame_north = Frame(self, width = window_root.window_width, height = 100, background = "LightSteelBlue3")
       self.frame_north.pack(side="top")
       self.frame_north.propagate(False)
       
       self.button_load_data = Button(self.frame_north, font = ('Helvetica', '10'), text = "Daten auswählen", command = lambda: create_load_data_window())
       self.button_load_data.pack(side = "left", padx = 3)
       
       self.button_rossmann_data = Button(self.frame_north, font = ('Helvetica', '10'), text = "Rossmann Verkaufszahlen", command = lambda: self.load_data("Daten/rossmann_verkaufszahlen_ausreißer_entfernt.csv", "rossmann"))
       self.button_rossmann_data.pack(side = "left", padx = 3)
       
       self.button_google_data = Button(self.frame_north, font = ('Helvetica', '10'), text = "Google Aktienkurs", command = lambda: self.load_data("Daten/google_aktienkurs.csv", "google"))
       self.button_google_data.pack(side = "left", padx = 3)
       
       self.button_google_data = Button(self.frame_north, font = ('Helvetica', '10'), text = "Bundesliga Bayern Punkte", command = lambda: self.load_data("Daten/BayernMaster_Merge_Interpol_Only_Points.csv", "bayern"))
       self.button_google_data.pack(side = "left", padx = 3)
       
       self.button_google_data = Button(self.frame_north, font = ('Helvetica', '10'), text = "Reset", command = lambda: self.reset_objects())
       self.button_google_data.pack(side = "left", padx = 3)
       

# =============================================================================
#    Löscht alle erstellten Prognosemethode Objekte, falls keine vorhanden sind, wird eine fehlermeldung ausgegeben.
# =============================================================================
   
   def reset_objects(self):
       
       resetted = 0
       
       try:
           del ar.AR_MODEL 
           resetted = 1
       except: 
           print()
           
       try:
           del wma.WEIGHT_MOV_AVG
           resetted = 1
       except: 
           print()
           
       try:
           del sma.SIM_MOV_AVG 
           resetted = 1
       except: 
           print()
        
       try:
           del ses.SIN_EXP_SMTH 
           resetted = 1
       except: 
           print()
       
       if(resetted == 0):
           messagebox.showerror("Error", "Keine Objekte zu löschen!")
       else:
           messagebox.showinfo("Information", "Objekte wurden zurückgesetzt")
       
   def load_data(self, data, dataname):
       
       if(dp.import_dataset(data)):
            
            messagebox.showinfo("Information", "Die Daten wurden erfolgreich gespeichert")
            
       dp.DATAFRAME_NAME = dataname
    
# =============================================================================
#    Erstellt den mittleren Bereich des Fensters. Enthalten sind Buttons für alle implementierten Prognosemethoden
# =============================================================================
    
   def create_frame_middle(self, window_root):  
              
       pad_grid_x = 10
       pad_grid_y = 10
       
       self.frame_middle = Frame(self, width = window_root.window_width - 200, height = 700, background = "white")
       self.frame_middle.pack(side = "left")
       self.frame_middle.grid_propagate(False)
       
       self.frame_middle.grid_columnconfigure(0, weight = 1)
       self.frame_middle.grid_columnconfigure(1, weight = 1)
       
       self.frame_middle.grid_rowconfigure(0, weight = 1)
       self.frame_middle.grid_rowconfigure(1, weight = 1)
       
       button_sim_mov_avg = Button(self.frame_middle, font = ('Helvetica', '15'), text= "Einfacher gleitender Durchschnitt", command = lambda: try_to_forecast("sim_mov_avg", window_root))
       button_sim_mov_avg.grid(row = 0, column = 0, padx = pad_grid_x, pady = pad_grid_y, sticky = "nsew")
        
       button_sin_exp_smth = Button(self.frame_middle, font = ('Helvetica', '15'), text= "Einfache exponentielle Glättung", command = lambda: try_to_forecast("sin_exp_smth", window_root))
       button_sin_exp_smth.grid(row = 1, column = 1, padx = pad_grid_x, pady = pad_grid_y, sticky = "nsew")
        
       button_ar_model = Button(self.frame_middle, font = ('Helvetica', '15'), text= "Autoregressives Modell", command = lambda: try_to_forecast("ar_model", window_root))
       button_ar_model.grid(row = 1, column = 0,padx = pad_grid_x, pady = pad_grid_y, sticky = "nsew")
        
       button_ma_model = Button(self.frame_middle,font = ('Helvetica', '15'),  text= "Gewichteter gleitender Durchschnitt", command = lambda: try_to_forecast("weight_mov_avg", window_root))
       button_ma_model.grid(row = 0, column = 1, padx = pad_grid_x, pady = pad_grid_y, sticky = "nsew")
       
       
# =============================================================================
#    Erstellt den südlichen Bereich des Fensters. Dient als visueller Rand des Programms.
# =============================================================================
       
   def create_frame_south(self, window_root):
       
       self.frame_south = Frame(self, width = window_root.window_width, height = 100, background = "LightSteelBlue3")
       self.frame_south.pack(side = "bottom")
       
# =============================================================================
#    Erstellt den östlichen Bereich des Fensters. Dient als visueller Rand des Programms.
# =============================================================================
       
   def create_frame_east(self, window_root):
       
       self.frame_east = Frame(self, width = 100, height = window_root.window_height - 200, background = "LightSteelBlue3")
       self.frame_east.pack(side = "right")

# =============================================================================
#    Erstellt den westlichen Bereich des Fensters. Dient als visueller Rand des Programms.
# =============================================================================
   
   def create_frame_west(self, window_root):
       
       self.frame_west = Frame(self,width = 100, height = window_root.window_height - 200, background = "LightSteelBlue3")
       self.frame_west.pack(side = "left")
    
# =============================================================================
# Die Klasse PageNsew erbt von der Klasse Frame von TkInter und implementiert somit ihre Funktionen. Das Fenster wird durch diese
# Klasse grundsätlich in die 5 Bereiche Nord, Süd, Ost, West und Mitte eingeteilt. Weitere Fenster können von dieser Klasse erben
# und haben somit bereits diese Einteilung implementiert.          
# =============================================================================
       
class PageNsew(Frame):

    def __init__(self, window_root):
        
       Frame.__init__(self, window_root) 
       
       self.propagate(False)
       
       self.create_frame_north(window_root)
       self.create_frame_south(window_root)
       self.create_frame_east(window_root)
       self.create_frame_west(window_root)
       self.create_frame_middle(window_root)
     
# =============================================================================
#     Erstellt den nördlichen Bereich des Fensters.
# =============================================================================
       
    def create_frame_north(self, window_root):
        
       self.frame_north = Frame(self, width = window_root.window_width, height = 100, background = "white", relief="sunken", borderwidth = 1)
       self.frame_north.pack(side="top")
       self.frame_north.propagate(False)
       
# =============================================================================
#     Erstellt den östlichen Bereich des Fensters. 
# =============================================================================
       
    def create_frame_east(self, window_root):
       
       self.frame_east = Frame(self, width = 250, height = window_root.window_height - 150, background = "white", relief="sunken", borderwidth = 1)
       self.frame_east.pack(side = "right")
       self.frame_east.propagate(False)
       
# =============================================================================
#     Erstellt den westlichen Bereich des Fensters.
# =============================================================================
       
    def create_frame_west(self, window_root):
       
       self.frame_west = Frame(self,width = 200, height = window_root.window_height - 150, background = "white", relief="sunken", borderwidth = 1)
       self.frame_west.pack(side = "left")
       self.frame_west.propagate(False)
    
# =============================================================================
#     Erstellt den südlichen Bereich des Fensters.
# =============================================================================
    
    def create_frame_south(self, window_root):
       
       self.frame_south = Frame(self, width = window_root.window_width, height = 50, background = "white", relief="sunken", borderwidth = 1)
       self.frame_south.pack(side = "bottom")
       self.frame_south.propagate(False)
    
# =============================================================================
#     Erstellt den mittleren Bereich des Fensters.
# =============================================================================
    
    def create_frame_middle(self, window_root):
       
       self.frame_middle = Frame(self, width = window_root.window_width - 450, height = 750, background = "white", relief="sunken", borderwidth = 1)
       self.frame_middle.pack(side = "left") 
       self.frame_middle.propagate(False)
      
# =============================================================================
# Diese Klasse erbt von PageNsew und implementiert weiterhin die wichtigen Grundlegenden Funktionen für den Aufbau eines Fenster.
#       
# create_plot_middle            : Erstellt den Canvas, auf dem der Graph gezeichnet werden kann.
# set_lim_x                     : Setzt Min und Max Limits für die X-Achse.
# set_lim_y                     : Setzt Min und Max Limits für die Y-Achse.
# switch_dataframe              : Setzt die angezeigten Datensätze und die dazugehöroge Legende des Graphen.
# create_frame_right            : Erstellt den Bereich für die Eingabefelder für X- und Y-Werte.
# create_limx_frame_right       : Erstellt den Bereich für das Eingabefeld der X-Werte.
# create_limx_frame_right       : Erstellt den Bereich für das Eingabefeld der Y-Werte. 
# create_explanation_middle     : Erstellt den Erklärungsbereich des Fensters.
# create_picture_remove_trend   : Lädt das Erklärungsbild für die Seite Trend entfernen.
# create_picture_method         : Lädt das Erklärungsbild für die Seite Prognoseergebnis.
# create_picture_add_trend      : Lädt das Erklärungsbild für die Seite Trend hinzufügen.
# create_picture_overview       : Lädt das Erklärungsbild für die Seite Überblick.
# display_dataframe             : Lädt den originalen Datensatz in den Graphen.
# display_forecasting_dataframe : Lädt den differenzierten Datensatz für die Prognose in den Graphen.
# display_forecast              : Lädt das Prognoseergebnis in den Graphen
# display_forecast_undiff       : Lädt das undifferenzierte Prognoseergebnis in den Graphen
# create_buttons                : Erstellt die Buttons für die Seite Trend entfernen, um die einzelnen Differenzierungen anzuzeigen.
# switch_to_original            : (Seite Trend entfernen) Zeigt wieder den originalen Datensatz
# switch_to_diff1               : (Seite Trend entfernen) Zeigt den Datensatz nach der ersten durchgeführten Differenz
# switch_to_diff2               : (Seite Trend entfernen) Zeigt den Datensatz nach der zweiten durchgeführten Differenz
# create_datalist_left          : Erstellt die linke Datenliste, in der die aktuell betrachteten Daten angezeigt werden.
# create_predictionlist_right   : Erstellt die reichte Datenliste, in der das aktuell betrachtete Prognoseergebnis angezeigt wird.
# =============================================================================

    
class PageNsewBasicControl(PageNsew):
    
    def __init__(self, window_root, model):
        
        PageNsew.__init__(self, window_root)
        
        self.x_min_lim = model.default_x_min_lim
        self.x_max_lim = model.default_x_max_lim
        self.y_min_lim = model.default_y_min_lim
        self.y_max_lim = model.default_y_max_lim
        
        self.frame_treeview = Frame(self.frame_west, width = 200, height = 750, background = "white")
        self.frame_treeview.pack()
        self.frame_treeview.grid_propagate(False)
        
        self.plots = {}
        
        self.model = model
        
        self.create_frame_right()
        self.create_explanation_middle(window_root)
        self.create_plot_middle(model)

        self.create_limx_frame_right(model)
        self.create_limy_frame_right(model)
        
        self.frame_treeview_right = Frame(self.frame_east, width = 200, height = 200, background = "white")
        self.frame_treeview_right.pack(side = "bottom")
        self.frame_treeview_right.grid_propagate(False)
          
        
    def create_plot_middle(self, model):
        
        self.figure1 = Figure(figsize=(5,5), dpi=100)        
        
        self.canvas = FigureCanvasTkAgg(self.figure1, self.frame_middle)
        self.canvas.get_tk_widget().pack(side="bottom", fill = "both")
        
    
# =============================================================================
#     Erhält als Parameter die min und max Werte der X-Achse und teilt diese den Plots in self.plots mit.
# =============================================================================
    
    def set_lim_x(self, min_x, max_x, model):

        for key in self.plots:
            heap, sep, tail = key.partition("_")
            if(tail == "index"):
                self.plots[key][0].set_xlim(min_x, max_x)
        
        self.x_min_lim = min_x
        self.x_max_lim = max_x
        
        self.canvas.draw()
        
# =============================================================================
#     Erhält als Parameter die min und max Werte der Y-Achse und teilt diese den Plots in self.plots mit.
# =============================================================================
        
    def set_lim_y(self, min_y, max_y, model):
            
        for key in self.plots:
            heap, sep, tail = key.partition("_")
            self.plots[key][0].set_ylim(min_y, max_y)
        
        self.y_min_lim = min_y
        self.y_max_lim = max_y
        
        self.canvas.draw()
        
# =============================================================================
#     Erhält als Parameter die Legendenbezeichnung und teilt diese dem Plot mit. Ebenfalls wird der Y-Achsenabschnitt
#     nach der Zielvariable genannt und der X-Achsenabschnitt standardmäßig "Days". Der Key für das Dictionary self.plots
#     wird ebenfalls als Parameter als Liste übergeben, wodurch mehrere Plots angezeigt werden können. Die Plots müssen 
#     jedesmal neu erstellt werden.
# =============================================================================
        
    def switch_dataframe(self, model, key, legend1, legend2):
        
        self.figure1.clf()
        
        self.subplot1 = self.figure1.add_subplot(111)

        for k in key:
            
            xvalue = self.plots[k][1]
            yvalue = self.plots[k][2]
            self.subplot1.plot(xvalue, yvalue)
            self.plots[k] = (self.subplot1, self.plots[k][1], self.plots[k][2])
                
        self.subplot1.set_ylabel(self.model.target_value)
        self.subplot1.set_xlabel("Days")
        
        if(legend2 == ""):
            self.subplot1.legend([legend1])
        else:
            self.subplot1.legend([legend1, legend2])
                
        self.set_lim_x(self.x_min_lim, self.x_max_lim, model)
        self.set_lim_y(self.y_min_lim, self.y_max_lim, model)
        
        self.canvas.draw()
        
    def create_frame_right(self):
        
        
        self.frame_limit_x = Frame(self.frame_east, width = 200, height = 100, relief="sunken", borderwidth = 1, background = "white")
        self.frame_limit_x.pack()
        
        self.frame_limit_y = Frame(self.frame_east, width = 200, height = 100, relief="sunken", borderwidth = 1, background = "white")
        self.frame_limit_y.pack()
            
    def create_limx_frame_right(self, model):
        
        self.label_explanation_limx = Label(self.frame_limit_x, text = "Werte der X-Achse", bg = "white")
        self.label_explanation_limx.place(x = 100, y = 20, anchor = "c")
        
        self.entry_index_minx = Entry(self.frame_limit_x, width = 5)
        self.entry_index_minx.place(x = 40, y = 75, anchor = "c")
        
        self.label_to1x = Label(self.frame_limit_x, text = "bis", bg = "white")
        self.label_to1x.place(x = 80, y = 75, anchor = "c")
        
        self.entry_index_maxx = Entry(self.frame_limit_x, width = 5)
        self.entry_index_maxx.place(x = 120, y = 75, anchor = "c")
        
        self.button_change_limx = Button(self.frame_limit_x, text = "Ok", width = 3, height = 1,
                                        command = lambda: self.set_lim_x(int(self.entry_index_minx.get()), int(self.entry_index_maxx.get()), model))
        self.button_change_limx.place(x = 160, y = 75, anchor = "c")

            
    def create_limy_frame_right(self, model):
        
        self.label_explanation_limy = Label(self.frame_limit_y, text = "Werte der Y-Achse", bg = "white")
        self.label_explanation_limy.place(x = 100, y = 20, anchor = "c")
        
        self.entry_index_miny = Entry(self.frame_limit_y, width = 5)
        self.entry_index_miny.place(x = 40, y = 75, anchor = "c")
        
        self.label_to1y = Label(self.frame_limit_y, text = "bis", bg = "white")
        self.label_to1y.place(x = 80, y = 75, anchor = "c")
        
        self.entry_index_maxy = Entry(self.frame_limit_y, width = 5)
        self.entry_index_maxy.place(x = 120, y = 75, anchor = "c")
        
        self.button_change_limy = Button(self.frame_limit_y, text = "Ok", width = 3, height = 1,
                                        command = lambda: self.set_lim_y(int(self.entry_index_miny.get()), int(self.entry_index_maxy.get()), model))
        self.button_change_limy.place(x = 160, y = 75, anchor = "c")
        
        
    def create_explanation_middle(self, window_root):
        
        self.frame_explanation = Frame(self.frame_middle, width = window_root.window_width - 450, height = 250, background = "white", borderwidth = 1, relief = "sunken")
        self.frame_explanation.pack(side = "bottom")
        self.frame_explanation.propagate(False)
        
    def create_picture_remove_trend(self):
        background_image=PhotoImage(file="Daten/trendentfernen.gif")
        self.background_label = Label(self.frame_explanation, image=background_image)
        self.background_label.place(x=0, y=0, relwidth = 1, relheight = 1)
        self.background_label.image = background_image
        
    def create_picture_add_trend(self):
        background_image=PhotoImage(file="Daten/trendhinzufügen.gif")
        self.background_label = Label(self.frame_explanation, image=background_image)
        self.background_label.place(x=0, y=0, relwidth = 1, relheight = 1)
        self.background_label.image = background_image
        
# =============================================================================
#     Lädt das Bild für die Seite überblick, je nachdem welche Daten von dem Nutzer ausgewählt wurden.
# =============================================================================
    
    def create_picture_overview(self):
        
        if(dp.DATAFRAME_NAME == "rossmann"):
            background_image=PhotoImage(file="Daten/rossmannüberblick.gif")
            self.background_label = Label(self.frame_explanation, image=background_image)
            self.background_label.place(x=0, y=0, relwidth = 1, relheight = 1)
            self.background_label.image = background_image
            
        if(dp.DATAFRAME_NAME == "google"):
            background_image=PhotoImage(file="Daten/googleüberblick.gif")
            self.background_label = Label(self.frame_explanation, image=background_image)
            self.background_label.place(x=0, y=0, relwidth = 1, relheight = 1)
            self.background_label.image = background_image
            
        if(dp.DATAFRAME_NAME == "bayern"):
            background_image=PhotoImage(file="Daten/bayernmünchenüberblick.gif")
            self.background_label = Label(self.frame_explanation, image=background_image)
            self.background_label.place(x=0, y=0, relwidth = 1, relheight = 1)
            self.background_label.image = background_image
            
# =============================================================================
#     Erstellt einen Plot für den originalen Datensatz, wobei als X-Achse der Index und als 
#     Y-Achse die Werte der Zielvariable ausgewählt werden. Diese Werte werden anschließend
#     in self.plots gespeichert.     
# =============================================================================
    
    def display_dataframe(self):
        
        _index = self.model.original_df.index.values
        _target_value = self.model.original_df[self.model.target_value]
        
        self.subplot1 = self.figure1.add_subplot(111)
        self.subplot1.plot(_index, _target_value)
        
        self.plots["dataframe_index"] = (self.subplot1, _index, _target_value)
        
        
# =============================================================================
#     Erstellt einen Plot für den für die Prognose verwendeten differenzierten Datensatz, wobei als X-Achse der Index und als 
#     Y-Achse die Werte der Zielvariable ausgewählt werden. Diese Werte werden anschließend in self.plots gespeichert. 
# =============================================================================
    
    def display_forecasting_dataframe(self):
        
        _index = self.model.df.index.values
        _target_value = self.model.df[self.model.target_value]
            
        self.subplot1 = self.figure1.add_subplot(111)
        self.subplot1.plot(_index, _target_value)
        
        self.plots["dataframe_index"] = (self.subplot1, _index, _target_value)
        
    def display_forecast(self):
        
        _index = self.model.prediction.index.values
        _target_value = self.model.prediction[self.model.target_value]
            
        self.subplot1 = self.figure1.add_subplot(111)
        self.subplot1.plot(_index, _target_value)
        
        self.plots["prediction_index"] = (self.subplot1, _index, _target_value)
        
    def display_forecast_undiff(self):
        
        _index = self.model.prediction_undiff.index.values
        _target_value = self.model.prediction_undiff[self.model.target_value]
        
        self.subplot1 = self.figure1.add_subplot(111)
        self.subplot1.plot(_index, _target_value)
        
        self.subplot1.legend()
        
        self.plots["prediction undiff_index"] = (self.subplot1, _index, _target_value)
        
        self.canvas.draw()    
    
    def create_buttons(self):
        
        button = Button(self.frame_explanation, width = 6, height = 2, text = "Reset", command = lambda: self.switch_to_original())
        button.place(x = 1100, y = 0)
          
        if(len(self.model.differences) >= 1):
            button1 = Button(self.frame_explanation, width = 6, height = 2, text = "Diff 1", command = lambda: self.switch_to_diff1())
            button1.place(x = 1100, y = 50)
        
        if(len(self.model.differences) >= 2):
            button1 = Button(self.frame_explanation, width = 6, height = 2, text = "Diff 2", command = lambda: self.switch_to_diff2())
            button1.place(x = 1100, y = 100)
        
    def switch_to_original(self):
        
        self.switch_dataframe(self.model, ["dataframe_index"], "Ausgangs Datensatz", "")
        
    
    def switch_to_diff1(self):
        
        model = self.model
        
        self.figure1.clf()
        
        _index = self.model.differenced_data[1].index.values
        _target_value = model.differenced_data[1][model.target_value]
        
        self.subplot1 = self.figure1.add_subplot(111)
        self.subplot1.plot(_index, _target_value)
        
        self.subplot1.set_ylabel(self.model.target_value)
        self.subplot1.set_xlabel("Days")
        
        self.plots["difference_index"] = (self.subplot1, _index, _target_value)
        self.subplot1.legend(["1. durchgeführte Differenz"])
        
        self.canvas.draw()
        
    def switch_to_diff2(self):
        
        model = self.model
        
        self.figure1.clf()
        
        _index = self.model.differenced_data[2].index.values
        _target_value = model.differenced_data[2][model.target_value]
        
        self.subplot1 = self.figure1.add_subplot(111)
        self.subplot1.plot(_index, _target_value)
        
        self.subplot1.set_ylabel(self.model.target_value)
        self.subplot1.set_xlabel("Days")
        
        self.plots["difference2_index"] = (self.subplot1, _index, _target_value)
        self.subplot1.legend(["2. durchgeführte Differenz"])
        
        self.canvas.draw()
            
# =============================================================================
#     Lädt das Bild für die Seite Prognoseergebnis, je nachdem welche Prognosemethode von dem Nutzer ausgewählt wurden. 
# =============================================================================
    
    def create_picture_method(self, method):
        
        if(method == "sim_mov_avg"):
            background_image=PhotoImage(file="Daten/einfachergleitenderdurchschnitt.gif")
            
        if(method == "weight_mov_avg"):
            background_image=PhotoImage(file="Daten/gewichtetergleitenderdurchschnitt.gif")
            
        if(method == "sin_exp_smth"):
            background_image=PhotoImage(file="Daten/einfacheexponentielleglättung.gif")
    
        if(method == "ar_model"):
            background_image=PhotoImage(file="Daten/autoregressivesmodell.gif")
            
        self.background_label = Label(self.frame_explanation, image=background_image)
        self.background_label.place(x=0, y=0, relwidth = 1, relheight = 1)
        self.background_label.image = background_image
        
        
# =============================================================================
#     Erstellt die linke Datenliste für die Daten des aktuell betrachteten Datensatzes. Es wird hierbei immer der Index und
#     die Zielvariable angezeigt. Falls ein Datum ausgewählt wurde, wird dieses ebenfalls angezeigt.
# =============================================================================

    def create_datalist_left(self, df):
        
        tree = Treeview(self.frame_treeview ,selectmode='browse')
        tree.grid(row = 0, column = 0, sticky = "nswe")

        vsb = Scrollbar(self.frame_treeview, orient="vertical", command=tree.yview)
        vsb.grid(row = 0, column = 1, sticky = "ns")

        
        self.frame_treeview.rowconfigure(0, weight = 1)

        tree.configure(yscrollcommand=vsb.set)

        
        target_value = self.model.target_value
        date = self.model.date
        
        # Erzeugen der Spalten Index und der Name der Zielvariable
        columns = []
        columns.append("Index")
        if date != "Kein Datum":
            columns.append(date)
        columns.append(target_value)
        
        tree["columns"] = columns
        tree['show'] = 'headings'
        
        # Bestimmen der Größe von den jeweiligen Spalten
        width = int(140/(len(columns)-1))
        for c in columns:
            if c == "Index":
                tree.column(c, width=40, anchor='c')
            else:
                tree.column(c, width=width, anchor='c')
    
        for c in columns:
             tree.heading(c, text = c)
        
        index = df.index.values[0]
        
        # Für jeden Wert in dem Datensatz wird einer neue Zeile durch tree.insert erstellt, welche den Wert beeinhaltet.
        for i in range(0, df.shape[0]):

            rows = df.iloc[i]
            values = []
            for c in columns:

                if(c == "Index"):
                    values.append(index)
                else:
                    if(c == date):
                        values.append(rows[c])
                    if(c == target_value):
                        values.append(round((rows[c]), 2))

            tree.insert("",'end',text="L" + "Index",values = values)
            index += 1
            
            
# =============================================================================
#     Erstellt die rechte Datenliste für die Daten des aktuell betrachteten Prognoseergebnisses. Es wird hierbei immer der Index und
#     die Zielvariable angezeigt. Falls ein Datum ausgewählt wurde, wird dieses ebenfalls angezeigt.
# =============================================================================
    
    def create_predictionlist_right(self, df):
        
        tree = Treeview(self.frame_treeview_right ,selectmode='browse')
        tree.grid(row = 0, column = 0, sticky = "nswe")

        vsb = Scrollbar(self.frame_treeview_right, orient="vertical", command=tree.yview)
        vsb.grid(row = 0, column = 1, sticky = "ns")

        
        self.frame_treeview_right.rowconfigure(0, weight = 1)

        tree.configure(yscrollcommand=vsb.set)

        
        target_value = self.model.target_value
        date = self.model.date
        
        # Erzeugen der Spalten Index und der Name der Zielvariable
        columns = []
        columns.append("Index")
        if date != "Kein Datum":
            columns.append(date)
        columns.append(target_value)
        tree["columns"] = columns
        tree['show'] = 'headings'
        
        # Bestimmen der Größe von den jeweiligen Spalten
        width = int(140/(len(columns)-1))
        for c in columns:
            if c == "Index":
                tree.column(c, width=40, anchor='c')
            else:
                tree.column(c, width=width, anchor='c')
    
        for c in columns:
             tree.heading(c, text = c)
        
        index = df.index.values[0]
        
        # Für jeden Wert in dem Datensatz wird einer neue Zeile durch tree.insert erstellt, welche den Wert beeinhaltet.
        for i in range(0, df.shape[0]):

            rows = df.iloc[i]
            values = []
            for c in columns:

                if(c == "Index"):
                    values.append(index)
                else:
                    if(c == date):
                        values.append(rows[c])
                    if(c == target_value):
                        values.append(round((rows[c]), 2))

            tree.insert("",'end',text="L" + "Index",values = values)
            index += 1
    

# =============================================================================
# Die Klasse erbt von PageNsewBasicControl und implementiert die Navigationsleiste für die jeweilie Prognosemethode. Für jede
# Methode muss eine eigene Klasse dieser Art erstellt werden, falls die Navigationsleiste sich unterscheidet.
# Diese Klasse ist für das Ar-Modell angepasst und beeinhaltet die folgenden Punkte:
#          
# - Home
# - Überblick
# - Entfernen von Trend und Saisonalität
# - Prognoseergebnis
# - Hinzufügen von Trend und Saisonalität
# =============================================================================

        
class PageNsewBasicControlAr(PageNsewBasicControl):
    
    def __init__(self, window_root, model):
        
        PageNsewBasicControl.__init__(self, window_root, model)
        
        self.create_navigationbar(window_root)
        
    def create_navigationbar(self, window_root):
        
        self.frame_navigation = Frame(self.frame_north, width = 1500, height = 40, background = "white")
        self.frame_navigation.place(x = window_root.window_width/2, y = 50, anchor = "c")
        
        width_buttons = 30
        height_buttons = 2
        padx_buttons = 5
        
        self.navigation_buttons = []
        
        self.button_home = Button(self.frame_north, width = width_buttons,  height = height_buttons, text = "Home",
                                 command = lambda: window_root.show_frame("PageStart"))
        self.button_home.pack(side = "left", padx = padx_buttons)
        
        self.button_overview = Button(self.frame_navigation, width = width_buttons,  height = height_buttons, text = "Überblick",
                                 command = lambda: window_root.show_frame(ArModelPageOverview))
        self.button_overview.pack(side = "left", padx = padx_buttons)
        self.navigation_buttons.append(self.button_overview)
        
        self.button_remove_saisonality = Button(self.frame_navigation, width = width_buttons,  height = height_buttons, text = "Entfernen von Trend und Saisonalität",
                                 command = lambda: window_root.show_frame(ArModelPageRemoveTrendAndSeasonality))
        self.button_remove_saisonality.pack(side = "left", padx = padx_buttons)
        self.navigation_buttons.append(self.button_remove_saisonality)
        
        self.button_forecast_result = Button(self.frame_navigation, width = width_buttons,  height = height_buttons, text = "Prognoseergebnis",
                                 command = lambda: window_root.show_frame(ArModelPageResultForecast))
        self.button_forecast_result.pack(side = "left", padx = padx_buttons)
        self.navigation_buttons.append(self.button_forecast_result)
        
        self.button_add_seasonality = Button(self.frame_navigation, width = width_buttons,  height = height_buttons, text = "Hinzufügen von Trend und Saisonalität",
                                 command = lambda: window_root.show_frame(ArModelPageAddTrendAndSeasonality))
        self.button_add_seasonality.pack(side = "left", padx = padx_buttons)
        self.navigation_buttons.append(self.button_add_seasonality)
        
        
    def change_previous_next(self, state, command):
        
        if(command == "next"):
            if(state < len(self.navigation_buttons)):
                self.navigation_buttons[state+1].invoke()
                
        if(command == "previous"):
            if(state > 0):
                self.navigation_buttons[state-1].invoke()
                
    def create_button_next(self, state):
        
        button_next = Button(self.frame_middle, width = 8, height = 2, text = "Vor", command = lambda: self.change_previous_next(state, "next"))
        button_next.place(x = 1070, y = 450)
        
    def create_button_previous(self, state):
        
        button_previous = Button(self.frame_middle, width = 8, height = 2, text = "Zurück", command = lambda: self.change_previous_next(state, "previous"))
        button_previous.place(x = 10, y = 450)
  

    
# =============================================================================
# Seiten des Autoregressiven Modells    
# =============================================================================
        
class ArModelPageOverview(PageNsewBasicControlAr):
    
    def __init__(self, window_root):
        
        model = ar.AR_MODEL
        PageNsewBasicControlAr.__init__(self, window_root, model) 

        self.create_picture_overview()
        self.display_dataframe()
        self.switch_dataframe(model, ["dataframe_index"], "Ausgangs Datensatz", "")
        self.create_datalist_left(model.original_df)
        self.button_overview.configure(relief = "solid", borderwidth = 3)
        self.create_button_next(0)        
    
        
class ArModelPageRemoveTrendAndSeasonality(PageNsewBasicControlAr):
    
    def __init__(self, window_root):
        
        model = ar.AR_MODEL
        PageNsewBasicControlAr.__init__(self, window_root, model) 
        
        self.create_picture_remove_trend()
        self.display_dataframe()
        self.create_datalist_left(model.original_df)
        self.create_buttons()
        self.switch_dataframe(model, ["dataframe_index"], "Ausgangs Datensatz", "")
        self.button_remove_saisonality.configure(relief = "solid", borderwidth = 3)
        self.create_button_next(1)
        self.create_button_previous(1)
              
        
class ArModelPageResultForecast(PageNsewBasicControlAr):
    
    def __init__(self, window_root):
        
        model = ar.AR_MODEL
        PageNsewBasicControlAr.__init__(self, window_root, model)
        
        self.create_picture_method("ar_model")
        self.display_forecasting_dataframe()
        self.display_forecast()
        self.create_datalist_left(model.df)
        self.create_predictionlist_right(model.prediction)
        self.create_frame_prediction_information()

        self.x_min_lim = model.forecast_start - 10
        self.x_max_lim = model.df.shape[0] - 1
        
        if(model.df[model.target_value].min() < 0):
            self.y_min_lim = -(model.df[model.target_value].max() + model.df[model.target_value].max()/3)
        else:
            self.y_min_lim = 0
        self.y_max_lim = model.df[model.target_value].max() + model.df[model.target_value].max()/3
        
        self.switch_dataframe(model, ["dataframe_index", "prediction_index"], "Ausgangs Datensatz", "Prognose")
        self.button_forecast_result.configure(relief = "solid", borderwidth = 3)
        
        self.create_button_next(2)
        self.create_button_previous(2)
        
   
    def create_frame_prediction_information(self):
        
        self.frame_prediction_information = Frame(self.frame_east, width = 200, height = 100, relief="sunken", borderwidth = 1, background = "white")
        self.frame_prediction_information.pack(side = "bottom")
        
        error_text = "MAE Prognosefehler: \n" + str(self.model.error)
        
        self.label_forecasterror= Label(self.frame_prediction_information, text = error_text, bg = "white")
        self.label_forecasterror.place(x = 100, y = 20, anchor = "c")
        
        lags_text = "Anzahl an Lags: \n" + str(self.model.lags)
        
        self.label_lags= Label(self.frame_prediction_information, text = lags_text, bg = "white")
        self.label_lags.place(x = 100, y = 60, anchor = "c")
        
class ArModelPageAddTrendAndSeasonality(PageNsewBasicControlAr):
    
    def __init__(self, window_root):
        
        model = ar.AR_MODEL
        PageNsewBasicControlAr.__init__(self, window_root, model) 
        
        self.create_picture_add_trend()
        self.display_dataframe()
        self.display_forecast_undiff()
        
        self.x_min_lim = model.original_df.shape[0] - 10 - 7
        self.x_max_lim = model.original_df.shape[0] - 1
        
        self.y_min_lim = 0
        self.y_max_lim = model.original_df[model.target_value].max() + model.original_df[model.target_value].max()/3
        
        self.switch_dataframe(model,["dataframe_index", "prediction undiff_index"], "Ausgangs Datensatz", "Prognose")
        self.create_datalist_left(model.original_df)
        self.create_predictionlist_right(model.prediction_undiff)
        self.create_frame_prediction_information()
        
        self.button_add_seasonality.configure(relief = "solid", borderwidth = 3)
        
        self.create_button_previous(3)
        
    def create_frame_prediction_information(self):
        
        self.frame_prediction_information = Frame(self.frame_east, width = 200, height = 100, relief="sunken", borderwidth = 1, background = "white")
        self.frame_prediction_information.pack(side = "bottom")
        
        error_text = "MAE Prognosefehler: \n" + str(self.model.error_undiff)
        
        self.label_forecasterror= Label(self.frame_prediction_information, text = error_text, bg = "white")
        self.label_forecasterror.place(x = 100, y = 20, anchor = "c")
        
        lags_text = "Anzahl an Lags: \n" + str(self.model.lags)
        
        self.label_lags= Label(self.frame_prediction_information, text = lags_text, bg = "white")
        self.label_lags.place(x = 100, y = 60, anchor = "c")
             
   
# =============================================================================
# Erstellt ein Fenster, dass dem Nutzer die Möglichkeit zur Auswahl eines eigenen Datensatzes mittels 
# eines Explorer-Fensters bietet. 
# =============================================================================

       
def create_load_data_window():
    
    width_window = 400
    height_window = 300
    offset_height_label_explanation = 70
    
    window_start_x = SCREEN_WIDTH/2 - width_window/2
    window_start_y = SCREEN_HEIGHT/2 - height_window/2
    
    load_data_window = Toplevel()
    load_data_window.geometry("%dx%d+%d+%d" %(width_window, height_window, window_start_x, window_start_y - 35))
    load_data_window.grab_set()
    
    frame_root = Frame(load_data_window, width = width_window, height = height_window)
    frame_root.propagate(False)
    frame_root.pack()
    
    frame_data_entry = Frame(frame_root, width = 265, height = 21)
    frame_data_entry.place(x = width_window/2, y = height_window/2, anchor = "center")
    frame_data_entry.propagate(False)
    
    frame_submit = Frame(frame_root, width = 150, height = 25)
    frame_submit.place(x = width_window/2, y = height_window/2 + 70, anchor = "center" )
    frame_submit.propagate(False)
       
    label_explanation = Label(frame_root, text = "Bitte wählen Sie eine Datei aus")
    label_explanation.place(x = width_window/2, y = height_window/2 - offset_height_label_explanation, anchor = "center")
    
    text_data = Text(frame_data_entry, width = 30, height = 1)
    text_data.insert("end", "Dateipfad")
    text_data.pack(side = "left")
    
    button_explorer = Button(frame_data_entry, width = 2, height = 1, text = "H", command = lambda: create_explorer_window(load_data_window, text_data))
    button_explorer.pack(side = "left")
    
    button_save_data = Button(frame_submit, text = "Speichern", command = lambda: save_data_from_textbox(load_data_window, text_data))
    button_save_data.pack(side = "left")
    
    button_cancel = Button(frame_submit, text = "Abbrechen", command = lambda: load_data_window.destroy())
    button_cancel.pack(side = "right")
    
# =============================================================================
# Erstellt ein Explorer-Fenster, dass dem Nutzer die Möglichkeit bietet, eigene Daten in das Programm zu laden.
# =============================================================================

def create_explorer_window(load_data_window, text_data):
    
    explorer_window = Toplevel()
    explorer_window.withdraw()
    
    explorer_window.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    load_data_window.lift()
    
    if(explorer_window.filename != ""):
        text_data.delete("1.0", "end")
        text_data.insert("end", explorer_window.filename)
    
    explorer_window.destroy()
    
# =============================================================================
# Liest den Ausgewählten Dateipfad aus und versucht die Daten in das Programm zu laden.
# =============================================================================

def save_data_from_textbox(load_data_window, text_data):
    
    text_data_row_one = text_data.get("1.0", "end").splitlines()
    text_data_row_one = text_data_row_one[0]
    
    if(text_data_row_one != "Dateipfad"):
        
        if(dp.import_dataset(text_data_row_one)):
            
            dp.DATAFRAME_NAME = ""
            load_data_window.destroy()
            messagebox.showinfo("Information", "Die Daten wurden erfolgreich gespeichert")
       
        
# =============================================================================
# Wird aufgerufen, wenn der Nutzer auf eine Prognosemethode klickt und überprüft, ob schon Daten ausgewählt wurden.
# Wenn Nein, dann gibt es eine Fehlermeldung. Ebenfalls überprüft diese Funktion, ob bereits ein Objekt der gewählten 
# Methode vorhanden ist. Sollte eins vorhanden sein, so werden die Bereits erstellten Seiten geöffnet, andernfalls
# werden weitere Informationen zu dem Datensatz durch die methode define_input verlangt.
# =============================================================================
      
def try_to_forecast(model, window_root):
        
    try: 
        dp.DATAFRAME
    
    except:
        messagebox.showerror("Error", "Bitte erst die benötigten Daten auswählen")
        return False
        
    if (model == "sin_exp_smth"):
        try:
            ses.SIN_EXP_SMTH
            window_root.show_frame(SinExpSmthPageOverview)
        except:
            define_input(window_root, model)
            
    if (model == "weight_mov_avg"):
        try:
            wma.WEIGHT_MOV_AVG
            window_root.show_frame(WeightMovAvgPageOverview)
        except:
            define_input(window_root, model)
            
    if (model == "sim_mov_avg"):
        try:
            sma.SIM_MOV_AVG
            window_root.show_frame(SimMovAvgPageOverview)
        except:
            define_input(window_root, model)
            
    if (model == "ar_model"):
        try:
            ar.AR_MODEL
            window_root.show_frame(ArModelPageOverview)
        except:
            define_input(window_root, model)

# =============================================================================
# Öffnet ein Fenster, in dem der Benutzer wichtige Informationen bzgl. des Datensatzes oder der Prognosemethode
# eingeben kann. Die möglichen Auswahlfaktoren unterscheiden sich je nach gewählter Prognosemethode. Durch die Auswahl
# und einem anschließenden Klick auf "Prognose starten" wird mittels der Methode create_forecast versucht, eine Prognose
# für die gewählte Methode zu starten. Als Parameter werden die Ausgewählten Faktoren übergeben.         
# =============================================================================
    
def define_input(window_root, model):
    
    width_window = 600
    height_window = 300
    offset_height_label_explanation = 90
    
    width_frame_input = 500
    height_frame_input = 60
    
    window_start_x = SCREEN_WIDTH/2 - width_window/2
    window_start_y = SCREEN_HEIGHT/2 - height_window/2
    
    window_define_input = Toplevel()
    window_define_input.geometry("%dx%d+%d+%d" %(width_window, height_window, window_start_x, window_start_y - 35))
    window_define_input.grab_set()
    
    frame_root = Frame(window_define_input, width = width_window, height = height_window)
    frame_root.propagate(False)
    frame_root.pack()
    
    frame_options = Frame(frame_root, width = width_frame_input, height = height_frame_input)
    frame_options.place(x = width_window/2 - 2, y = height_window/2, anchor = "center")
    frame_options.grid_propagate(False)
    
    frame_submit = Frame(frame_root, width = 200, height = 25)
    frame_submit.place(x = width_window/2, y = height_window/2 + 70, anchor = "center" )
    frame_submit.propagate(False)
        
    label_explanation = Label(frame_root, text = "Benötigte Informationen zu dem Datensatz")
    label_explanation.place(x = width_window/2, y = height_window/2 - offset_height_label_explanation, anchor = "center")
        
    choices = dp.get_columns(dp.DATAFRAME)
    choices_target_val = []
    
    # Überprüfung ob choices_target_val numerisch ist
    
    for i in choices:
        try:
            int(dp.DATAFRAME[i].iloc[0])
            choices_target_val.append(i)
        except:
            pass
    
    choices_date = ["Kein Datum"] + choices
 
    combobox_target_val = Combobox(frame_options, state = "readonly", values = choices_target_val)
    combobox_date = Combobox(frame_options,  state = "readonly", values = choices_date)
    
    entry_difference = Entry(frame_options)
    entry_difference.insert("end", '0')
    
    
    frame_options.grid_columnconfigure(2, weight = 1)
    frame_options.grid_columnconfigure(4, weight = 1)
    
    combobox_target_val.grid(row = 0, column = 1)
    combobox_date.grid(row = 1, column = 1)
    entry_difference.grid(row = 0, column = 4)
    
    # Die Felder Zielvariable, Datum und Differenzierung müssen für jede Methode ausgefüllt werden
    
    label_target_val = Label(frame_options, text = "Zielvariable: ")
    label_date = Label(frame_options, text = "Datum: ")
    label_seasonality = Label(frame_options, text = "Differenzierung: ")
    
    label_target_val.grid(row = 0, column = 0, sticky = "w")
    label_date.grid(row = 1, column = 0, sticky = "w")
    label_seasonality.grid(row = 0, column = 3, sticky = "w")
    
    # Im Folgenden wird unterschieden, um welche Prognosemethode es sich handelt. Für jede sind unterschiedliche
    # Auswahlfaktoren definiert.
    
    if(model == "sim_mov_avg"):
        label_lags = Label(frame_options, text = "Lag Anzahl: ")
        label_lags.grid(row = 1, column = 3, sticky = "w")
        entry_lags = Entry(frame_options)
        entry_lags.grid(row = 1, column = 4)
        entry_lags.insert("end", '6')
        button_save_data = Button(frame_submit, text = "Prognose starten", command = lambda: 
            create_forecast(window_root, model, window_define_input, combobox_target_val.get(), combobox_date.get(), entry_difference.get(), entry_lags.get(), "0", "0"))
        button_save_data.pack(side = "left")
        
    if(model == "weight_mov_avg"):
        label_lags = Label(frame_options, text = "Lag Anzahl: ")
        label_weight = Label(frame_options, text = "Gewichtung: ")
        label_lags.grid(row = 1, column = 3, sticky = "w")
        label_weight.grid(row = 2, column = 3, sticky = "w")
        entry_lags = Entry(frame_options)
        entry_lags.insert("end", '6')
        entry_weight = Entry(frame_options)
        entry_weight.insert("end", '6,5,4,3,2,1')
        entry_lags.grid(row = 1, column = 4)
        entry_weight.grid(row = 2, column = 4)
        button_save_data = Button(frame_submit, text = "Prognose starten", command = lambda: 
            create_forecast(window_root, model, window_define_input, combobox_target_val.get(), combobox_date.get(), entry_difference.get(), entry_lags.get(), entry_weight.get(), "0"))
    
    if(model == "sin_exp_smth"):
        label_alpha = Label(frame_options, text = "alpha: ")
        label_alpha.grid(row = 1, column = 3, sticky = "w")
        entry_alpha = Entry(frame_options)
        entry_alpha.grid(row = 1, column = 4)
        entry_alpha.insert("end", '0.2')
        button_save_data = Button(frame_submit, text = "Prognose starten", command = lambda: 
            create_forecast(window_root, model, window_define_input, combobox_target_val.get(), combobox_date.get(), entry_difference.get(), "0", "0", entry_alpha.get()))
        button_save_data.pack(side = "left")
        
    if(model == "ar_model"):

        button_save_data = Button(frame_submit, text = "Prognose starten", command = lambda: 
            create_forecast(window_root, model, window_define_input, combobox_target_val.get(), combobox_date.get(), entry_difference.get(), "0", "0", "0"))
        button_save_data.pack(side = "left")
        

    button_save_data.pack(side = "left")
    
    button_cancel = Button(frame_submit, text = "Abbrechen", command = lambda: window_define_input.destroy())
    button_cancel.pack(side = "right")
  
    
def create_forecast(window_root, model, window_define_input, target_val, date, differences, lags, weight, alpha):
    
    # Die vom Nutzer eingegebenen Differenzen sind durch ein Komma getrennt und somit kann der String in einzelne Teile gesplitted werden
    difference = differences.split(",")
    difference = list(map(int, difference))
    
    # Die vom Nutzer eingegebene Gewichtung sind durch ein Komma getrennt und somit kann der String in einzelne Teile gesplitted werden
    weights  = weight.split(",")
    weights = list(map(int, weights))
    
    alpha = float(alpha)
    
    lags = int(lags)
    
    # Es wird versucht ein Objekt von der ausgewählten Prognosemethode zu erstellen und die benötigten Parameter zu übergeben.
    # Anschließend werden durch die Methode create_..._page die einzelnen Seiten der Methode erstellt. Sollte dies nicht
    # funktionieren, so wird eine Fehlermeldung ausgegeben
    
    try:
        if(model == "sin_exp_smth"):
        
            ses.SIN_EXP_SMTH = ses.SinExpSmth(dp.DATAFRAME, target_val, date,0, difference, alpha)
            window_root.create_ses_page()
            window_root.show_frame(SinExpSmthPageOverview)
            window_define_input.destroy()
        
        if(model == "weight_mov_avg"):
        
            wma.WEIGHT_MOV_AVG = wma.WeightMovAvg(dp.DATAFRAME, target_val, date,0, difference, lags, weights)
            window_root.create_wma_page()
            window_root.show_frame(WeightMovAvgPageOverview)
            window_define_input.destroy()
        
        if(model == "sim_mov_avg"):
        
            sma.SIM_MOV_AVG = sma.SimMovAvg(dp.DATAFRAME, target_val, date,0, difference, lags)
            window_root.create_sma_page()
            window_root.show_frame(SimMovAvgPageOverview)
            window_define_input.destroy()
        
        if(model == "ar_model"):
        
            ar.AR_MODEL = ar.ArModel(dp.DATAFRAME, target_val, date, 0, difference)
            window_root.create_ar_page()
            window_root.show_frame(ArModelPageOverview)
            window_define_input.destroy()
    except:
        messagebox.showerror("Error", "Die Prognose ist fehlgeschlagen")
   
# =============================================================================
# Main Methode des Programms. Zunächst wird ein Objekt der Gui Klasse erstellt und ein mainloop aufgerufen.     
# =============================================================================
    
if __name__ == "__main__":
    
    window = Gui()
    window.mainloop()

    
        


   