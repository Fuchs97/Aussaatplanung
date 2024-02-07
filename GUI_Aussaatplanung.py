from tkinter import messagebox
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from rotate_pattern import generate_triangular_points_rotated
from shapely.geometry import Polygon, Point
from save_data import save_data_seed_coords, save_data_seed_coords_kml
from polygon_with_field_edge import reduced_polygon
from coords_kml_tkinter import select_kml_file, extract_coordinates
from coords_transformation import get_utm_zone, geo_to_utm, utm_to_geo_points
from PSO import pyswarm_global_optimization
from tkinter import filedialog
from headland_coords import points_headland_area, points_headland_circ
import numpy as np
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

class PlotApp(customtkinter.CTk):
    def __init__(self):
        # customtkinter.CTk-Methoden erben
        super().__init__()

        # Titel und Fenstergröße
        self.title("Aussaatplanung")
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        #self.geometry("700x700")

        # Rahmen für Konfiguration, Berechnung und Vorschau
        self.sidebar_frame1 = customtkinter.CTkFrame(self)
        self.sidebar_frame1.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), rowspan=5, columnspan=3, sticky="nsew")
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame1, text="Konfiguration", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_frame1_sitechange = customtkinter.CTkFrame(self, height=400)
        self.sidebar_frame1_sitechange.place(x=30, y=70)
        self.sidebar_frame2 = customtkinter.CTkFrame(self)
        self.sidebar_frame2.grid(row=5, column=0, padx=(20, 20), pady=(20, 0), rowspan=5, columnspan=3, sticky="nsew")
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame2, text="Berechnung", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_frame2_sitechange = customtkinter.CTkFrame(self, height=400)
        self.sidebar_frame2_sitechange.place(x=30, y=470)
        self.sidebar_frame3 = customtkinter.CTkFrame(self)
        self.sidebar_frame3.grid(row=0, column=4, padx=(20, 20), pady=(20, 0), rowspan=10, columnspan=3, sticky="nsew")
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame3, text="Vorschau",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Buttons für Seitenwechsel der Felder 1,2,3
        self.field_1_button = customtkinter.CTkButton(self.sidebar_frame1_sitechange, text="Feld 1", command=lambda: self.configuration_change_site(1))
        self.field_1_button.grid(row=1, column=0, padx=0, pady=10, columnspan=1)
        self.field_2_button = customtkinter.CTkButton(self.sidebar_frame1_sitechange, text="Feld 2", command=lambda: self.configuration_change_site(2))
        self.field_2_button.grid(row=2, column=0, padx=0, pady=10, columnspan=1)
        self.field_3_button = customtkinter.CTkButton(self.sidebar_frame1_sitechange, text="Feld 3", command=lambda: self.configuration_change_site(3))
        self.field_3_button.grid(row=3, column=0, padx=0, pady=10, columnspan=1)

        # Buttons für Seitenwechsel der Berechnung (manuell/optimiert)
        self.field_1_button = customtkinter.CTkButton(self.sidebar_frame2_sitechange, text="manuell", command=lambda: self.calculation_change_site(1))
        self.field_1_button.grid(row=1, column=0, padx=0, pady=10, columnspan=1)
        self.field_2_button = customtkinter.CTkButton(self.sidebar_frame2_sitechange, text="optimiert", command=lambda: self.calculation_change_site(2))
        self.field_2_button.grid(row=2, column=0, padx=0, pady=10, columnspan=1)

        # Infotext Koordinaten
        self.info_label = customtkinter.CTkLabel(self.sidebar_frame1, text="")
        self.info_label.grid(row=0, column=1, padx=10, pady=10, columnspan=2, sticky="w")

        # Combobox Vorgewende
        self.field_edge_label = customtkinter.CTkLabel(self.sidebar_frame1, text="Option Vorgewende:")
        self.field_edge_label.grid(row=2, column=1, padx=10, pady=10, sticky="nw")
        self.combobox_1 = customtkinter.CTkComboBox(self.sidebar_frame1, command=self.on_combobox_change, values=["Individueller Bereich", "Umlaufender Bereich"], width=250, state="readonly")
        self.combobox_1.grid(row=2, column=2, padx=0, pady=10, sticky="n")

        # Eingabefelder Konfiguration
        self.field_edge_label = customtkinter.CTkLabel(self.sidebar_frame1, text="Feldgrenzen:")
        self.field_edge_label.grid(row=1, column=1, padx=10, pady=0, sticky="nw")
        self.coords_entry = customtkinter.CTkTextbox(self.sidebar_frame1, width=250, height=60)
        self.coords_entry.grid(row=1, column=2, rowspan=1, padx=10, pady=0, sticky="nw")
        self.coords_entry.bind("<FocusIn>", self.add_info_text_coords)
        self.coords_entry.bind("<FocusOut>", self.remove_info_text)
        self.field_edge1_label = customtkinter.CTkLabel(self.sidebar_frame1, text="Vorgewendebereich 1:")
        self.field_edge1_label.grid(row=3, column=1, padx=10, pady=10, sticky="nw")
        self.headland1_entry = customtkinter.CTkTextbox(self.sidebar_frame1, width=250, height=60)
        self.headland1_entry.grid(row=3, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
        self.headland1_entry.bind("<FocusIn>", self.add_info_text_coords)
        self.headland1_entry.bind("<FocusOut>", self.remove_info_text)
        self.field_edge2_label = customtkinter.CTkLabel(self.sidebar_frame1, text="Vorgewendebereich 2:")
        self.field_edge2_label.grid(row=4, column=1, padx=10, pady=10, sticky="nw")
        self.headland2_entry = customtkinter.CTkTextbox(self.sidebar_frame1, width=250, height=60)
        self.headland2_entry.grid(row=4, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
        self.headland2_entry.bind("<FocusIn>", self.add_info_text_coords)
        self.headland2_entry.bind("<FocusOut>", self.remove_info_text)

        self.field_edge_label = customtkinter.CTkLabel(self.sidebar_frame1, text="Vorgewende Breite [m]:")
        self.field_edge_label.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.field_edge_entry = customtkinter.CTkEntry(self.sidebar_frame1)
        self.field_edge_entry.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

        # Optionsliste Saatgut Konfiguration
        self.option_plants_label = customtkinter.CTkLabel(self.sidebar_frame1, text="Saatgut:")
        self.option_plants_label.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.option_plants_entry = customtkinter.CTkOptionMenu(self.sidebar_frame1, values=["", "Zuckerrübe", "Mais", "Getreide", "Test 10m", "Test 100m"], state="readonly")
        self.option_plants_entry.grid(row=5, column=2, padx=10, pady=10, sticky="ew")

        # Button um Koordinaten der KML-File zu extrahieren
        self.coords1_kml = customtkinter.CTkButton(self.sidebar_frame1, text="KML-Datei hochladen", command=self.extract_coordinates_kml)
        self.coords1_kml.grid(row=1, column=3, pady=0, padx=10, sticky="n")
        self.coords2_kml = customtkinter.CTkButton(self.sidebar_frame1, text="KML-Datei hochladen", command=lambda: self.extract_coordinates_kml_headland_1())
        self.coords2_kml.grid(row=3, column=3, pady=10, sticky="n")
        self.coords3_kml = customtkinter.CTkButton(self.sidebar_frame1, text="KML-Datei hochladen", command=lambda: self.extract_coordinates_kml_headland_2())
        self.coords3_kml.grid(row=4, column=3, pady=10, sticky="n")

        # Eingabefelder für die Berechnung manuell
        self.disp_x_label = customtkinter.CTkLabel(self.sidebar_frame2, text="Verschiebung in X-Richtung in %:")
        self.disp_x_label.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
        self.disp_x_entry = customtkinter.CTkEntry(self.sidebar_frame2, width=60, height=20)
        self.disp_x_entry.grid(row=1, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
        self.disp_y_label = customtkinter.CTkLabel(self.sidebar_frame2, text="Verschiebung in Y-Richtung in %:")
        self.disp_y_label.grid(row=2, column=1, padx=10, pady=10, sticky="nw")
        self.disp_y_entry = customtkinter.CTkEntry(self.sidebar_frame2, width=60, height=20)
        self.disp_y_entry.grid(row=2, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
        self.angle_label = customtkinter.CTkLabel(self.sidebar_frame2, text="Winkel in °:")
        self.angle_label.grid(row=3, column=1, padx=10, pady=10, sticky="nw")
        self.angle_entry = customtkinter.CTkEntry(self.sidebar_frame2, width=60, height=20)
        self.angle_entry.grid(row=3, column=2, rowspan=1, padx=10, pady=10, sticky="nw")

        # Eingabefelder für die Berechnung optimiert
        self.maxiter_label = customtkinter.CTkLabel(self.sidebar_frame2, text="Maximale Anzahl an Iterationen:")
        self.maxiter_label.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
        self.maxiter_entry = customtkinter.CTkEntry(self.sidebar_frame2, width=60, height=20)
        self.maxiter_entry.grid(row=1, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
        self.swarmsize_label = customtkinter.CTkLabel(self.sidebar_frame2, text="Schwarmgröße:")
        self.swarmsize_label.grid(row=2, column=1, padx=10, pady=10, sticky="nw")
        self.swarmsize_entry = customtkinter.CTkEntry(self.sidebar_frame2, width=60, height=20)
        self.swarmsize_entry.grid(row=2, column=2, rowspan=1, padx=10, pady=10, sticky="nw")

        # Button zum Berechnen und Anzeigen des Plots
        self.calculate_button = customtkinter.CTkButton(self, text="Berechnung starten", command=lambda: self.calculate_and_plot())
        self.calculate_button.grid(row=11, column=0, columnspan= 4, pady=10)

        # Matplotlib-Figure für den Plot
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.sidebar_frame3)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        # Button, um Saatpunkte zu speichern und um SVG-Datei zu erstellen
        self.seed_points_list = customtkinter.CTkButton(self.sidebar_frame3, text="Koordinatenliste als txt.-Datei generieren",
                                                        command=lambda: self.generate_seed_points_list())
        self.seed_points_list.grid(row=2, column=0, columnspan=1, padx=20, pady=10, sticky="w")
        self.save_svg = customtkinter.CTkButton(self.sidebar_frame3, text="SVG-Datei speichern",
                                                        command=lambda: self.save_as_svg())
        self.save_svg.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
        self.save_svg = customtkinter.CTkButton(self.sidebar_frame3,
                                                text="Saat-Koordinaten in einer KML-Datei speichern",
                                                command=lambda: self.save_as_kml())
        self.save_svg.grid(row=3, column=0, columnspan=1, padx=20,
                           pady=10, sticky="w")

        # Platzhalter für den Plot
        self.plot_placeholder()

        # Zeilen- und Spaltenanpassung bei Lücken im Fenster
        #self..grid_rowconfigure(3, weight=1)
        #self.grid_rowconfigure(5, weight=0)
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_columnconfigure(2, weight=3)

        # Konfiguration Parameter für 3 Felder
        self.feldgrenzen1 = ""
        self.vorgewende11 = ""
        self.vorgewende12 = ""
        self.umlaufbreite1 = 0
        self.saatgut1 = ""
        self.vorgewendeoption1 = "Individueller Bereich"
        self.points1 = 0
        self.feldgrenzen2 = ""
        self.vorgewende21 = ""
        self.vorgewende22 = ""
        self.umlaufbreite2 = 0
        self.saatgut2 = ""
        self.vorgewendeoption2 = "Individueller Bereich"
        self.points2 = 0
        self.feldgrenzen3 = ""
        self.vorgewende31 = ""
        self.vorgewende32 = ""
        self.umlaufbreite3 = 0
        self.saatgut3 = ""
        self.vorgewendeoption3 = "Individueller Bereich"
        self.points3 = 0
        self.points_total = []

        # Berechnung Parameter
        self.disp_x = ""
        self.disp_y = ""
        self.angle = ""
        self.maxiter = ""
        self.swarmsize = ""

        # Standard-Einstellungen
        self.field_edge_label.grid_forget()
        self.field_edge_entry.grid_forget()
        self.swarmsize_entry.grid_forget()
        self.swarmsize_label.grid_forget()
        self.maxiter_entry.grid_forget()
        self.maxiter_label.grid_forget()
        self.combobox_1.set("Individueller Bereich")
        self.currentsite_config = 1
        self.currentsite_calc = 1
        self.placeholder1_entry = customtkinter.CTkTextbox(self.sidebar_frame2, width=60, height=20)
        self.placeholder1_entry.grid(row=1, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
        self.placeholder2_entry = customtkinter.CTkTextbox(self.sidebar_frame2, width=60, height=20)
        self.placeholder2_entry.grid(row=2, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
        self.placeholder3_entry = customtkinter.CTkTextbox(self.sidebar_frame2, width=60, height=20)
        self.placeholder3_entry.grid(row=3, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
        self.sidebar_frame2.grid_propagate(False)  # Frame fixieren
        self.placeholder1_entry.grid_forget()
        self.placeholder2_entry.grid_forget()
        self.placeholder3_entry.grid_forget()
        self.field_edge_entry.insert("0", 0)
        self.angle_entry.insert("0", 0)
        self.swarmsize_entry.insert("0", 50)
        self.maxiter_entry.insert("0", 10)
        self.disp_x_entry.insert("0", 0)
        self.disp_y_entry.insert("0", 0)
        self.points = 0
        self.utm_zone = ""

    def configuration_change_site(self, button_number):
        # Einträge speichern
        if self.currentsite_config == 1:
            self.feldgrenzen1 = str(self.coords_entry.get("1.0", "end-1c"))
            self.vorgewende11 = str(self.headland1_entry.get("1.0", "end-1c"))
            self.vorgewende12 = str(self.headland2_entry.get("1.0", "end-1c"))
            self.vorgewendeoption1 = str(self.combobox_1.get())
            self.umlaufbreite1 = str(self.field_edge_entry.get())
            self.saatgut1 = self.option_plants_entry.get()
            if self.combobox_1.get() == "Individueller Bereich":
                self.vorgewendeoption1 = "Individueller Bereich"
            else:
                self.vorgewendeoption1 = "Umlaufender Bereich"
        elif self.currentsite_config == 2:
            self.feldgrenzen2 = str(self.coords_entry.get("1.0", "end-1c"))
            self.vorgewende21 = str(self.headland1_entry.get("1.0", "end-1c"))
            self.vorgewende22 = str(self.headland2_entry.get("1.0", "end-1c"))
            self.vorgewendeoption2 = str(self.combobox_1.get())
            self.umlaufbreite2 = str(self.field_edge_entry.get())
            self.saatgut2 = self.option_plants_entry.get()
            if self.combobox_1.get() == "Individueller Bereich":
                self.vorgewendeoption2 = "Individueller Bereich"
            else:
                self.vorgewendeoption2 = "Umlaufender Bereich"
        elif self.currentsite_config == 3:
            self.feldgrenzen3 = str(self.coords_entry.get("1.0", "end-1c"))
            self.vorgewende31 = str(self.headland1_entry.get("1.0", "end-1c"))
            self.vorgewende32 = str(self.headland2_entry.get("1.0", "end-1c"))
            self.vorgewendeoption3 = str(self.combobox_1.get())
            self.umlaufbreite3 = str(self.field_edge_entry.get())
            self.saatgut3 = self.option_plants_entry.get()
            if self.combobox_1.get() == "Individueller Bereich":
                self.vorgewendeoption3 = "Individueller Bereich"
            else:
                self.vorgewendeoption3 = "Umlaufender Bereich"

        # Einträge löschen
        self.coords_entry.delete("1.0", "end")
        self.headland1_entry.delete("1.0", "end")
        self.headland2_entry.delete("1.0", "end")
        self.field_edge_entry.delete(0, "end")

        # Gespeicherte Einträge hinzufügen
        if button_number == 1:
            self.currentsite_config = 1
            self.option_plants_entry.set(self.saatgut1)
            self.coords_entry.insert("1.0", self.feldgrenzen1)
            self.headland1_entry.insert("1.0", self.vorgewende11)
            self.headland2_entry.insert("1.0", self.vorgewende12)
            self.field_edge_entry.insert("0", self.umlaufbreite1)
            self.on_combobox_change(self.vorgewendeoption1)
        elif button_number == 2:
            self.currentsite_config = 2
            self.option_plants_entry.set(self.saatgut2)
            self.coords_entry.insert("1.0", self.feldgrenzen2)
            self.headland1_entry.insert("1.0", self.vorgewende21)
            self.headland2_entry.insert("1.0", self.vorgewende22)
            self.field_edge_entry.insert("0", self.umlaufbreite2)
            self.on_combobox_change(self.vorgewendeoption2)
        elif button_number == 3:
            self.currentsite_config = 3
            self.option_plants_entry.set(self.saatgut3)
            self.coords_entry.insert("1.0", self.feldgrenzen3)
            self.headland1_entry.insert("1.0", self.vorgewende31)
            self.headland2_entry.insert("1.0", self.vorgewende32)
            self.field_edge_entry.insert("0", self.umlaufbreite3)
            self.on_combobox_change(self.vorgewendeoption3)

    def calculation_change_site(self, button_number):
        # Wechsel zwischen den Seiten manuell und optimiert
        if button_number == 1:
            self.currentsite_calc = 1
            self.disp_x_label.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
            self.disp_x_entry.grid(row=1, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
            self.disp_y_label.grid(row=2, column=1, padx=10, pady=10, sticky="nw")
            self.disp_y_entry.grid(row=2, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
            self.angle_label.grid(row=3, column=1, padx=10, pady=10, sticky="nw")
            self.angle_entry.grid(row=3, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
            self.swarmsize_entry.grid_forget()
            self.swarmsize_label.grid_forget()
            self.maxiter_entry.grid_forget()
            self.maxiter_label.grid_forget()

        elif button_number == 2:
            self.currentsite_calc = 2
            self.maxiter_label.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
            self.maxiter_entry.grid(row=1, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
            self.swarmsize_label.grid(row=2, column=1, padx=10, pady=10, sticky="nw")
            self.swarmsize_entry.grid(row=2, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
            self.disp_x_label.grid_forget()
            self.disp_x_entry.grid_forget()
            self.disp_y_label.grid_forget()
            self.disp_y_entry.grid_forget()
            self.angle_label.grid_forget()
            self.angle_entry.grid_forget()

    def on_combobox_change(self, selected_option: str):

        self.sidebar_frame1.grid_propagate(False)   # Frame fixieren

        if selected_option == "Umlaufender Bereich":
            self.field_edge_label.grid(row=3, column=1, padx=10, pady=10, sticky="w")
            self.field_edge_entry.grid(row=3, column=2, padx=10, pady=10, sticky="ew")
            self.combobox_1.set("Umlaufender Bereich")
            self.field_edge1_label.grid_forget()
            self.headland1_entry.grid_forget()
            self.field_edge2_label.grid_forget()
            self.headland2_entry.grid_forget()
            self.coords2_kml.grid_forget()
            self.coords3_kml.grid_forget()
        elif selected_option == "Individueller Bereich":
            self.field_edge_label.grid_forget()
            self.field_edge_entry.grid_forget()
            self.combobox_1.set("Individueller Bereich")
            self.field_edge1_label.grid(row=3, column=1, padx=10, pady=10, sticky="nw")
            self.headland1_entry.grid(row=3, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
            self.field_edge2_label.grid(row=4, column=1, padx=10, pady=10, sticky="nw")
            self.headland2_entry.grid(row=4, column=2, rowspan=1, padx=10, pady=10, sticky="nw")
            self.coords2_kml.grid(row=3, column=3, pady=10, sticky="n")
            self.coords3_kml.grid(row=4, column=3, pady=10, sticky="n")

    def save_field_parameters(self):
        # Einträge der Konfigurationsseite "Feld 1" speichern (notwendig, wenn die Felder 2 und 3 nicht genutzt wurden)
        if self.currentsite_config == 1:
            self.feldgrenzen1 = str(self.coords_entry.get("1.0", "end-1c"))
            self.vorgewende11 = str(self.headland1_entry.get("1.0", "end-1c"))
            self.vorgewende12 = str(self.headland2_entry.get("1.0", "end-1c"))
            self.vorgewendeoption1 = str(self.combobox_1.get())
            self.umlaufbreite1 = str(self.field_edge_entry.get())
            self.saatgut1 = self.option_plants_entry.get()
            if self.combobox_1.get() == "Individueller Bereich":
                self.vorgewendeoption1 = "Individueller Bereich"
            else:
                self.vorgewendeoption1 = "Umlaufender Bereich"
        elif self.currentsite_config == 2:
            self.feldgrenzen2 = str(self.coords_entry.get("1.0", "end-1c"))
            self.vorgewende21 = str(self.headland1_entry.get("1.0", "end-1c"))
            self.vorgewende22 = str(self.headland2_entry.get("1.0", "end-1c"))
            self.vorgewendeoption2 = str(self.combobox_1.get())
            self.umlaufbreite2 = str(self.field_edge_entry.get())
            self.saatgut2 = self.option_plants_entry.get()
            if self.combobox_1.get() == "Individueller Bereich":
                self.vorgewendeoption2 = "Individueller Bereich"
            else:
                self.vorgewendeoption2 = "Umlaufender Bereich"
        elif self.currentsite_config == 3:
            self.feldgrenzen3 = str(self.coords_entry.get("1.0", "end-1c"))
            self.vorgewende31 = str(self.headland1_entry.get("1.0", "end-1c"))
            self.vorgewende32 = str(self.headland2_entry.get("1.0", "end-1c"))
            self.vorgewendeoption3 = str(self.combobox_1.get())
            self.umlaufbreite3 = str(self.field_edge_entry.get())
            self.saatgut3 = self.option_plants_entry.get()
            if self.combobox_1.get() == "Individueller Bereich":
                self.vorgewendeoption3 = "Individueller Bereich"
            else:
                self.vorgewendeoption3 = "Umlaufender Bereich"

    def calculate_and_plot(self):
        self.save_field_parameters()
        self.ax.clear()
        self.points_total = []
        if self.feldgrenzen1 != "":
            self.points1 = self.calculate_field(self.feldgrenzen1,
                                           self.saatgut1)
            self.points = self.points1
            self.plot(self.points1,
                      self.feldgrenzen1,
                      self.vorgewendeoption1,
                      self.umlaufbreite1,
                      self.vorgewende11,
                      self.vorgewende12)
            for point in self.points1:
                self.points_total.append(point)
        if self.feldgrenzen2 != "":
            self.points2 = self.calculate_field(self.feldgrenzen2,
                                           self.saatgut2)
            self.points = self.points2
            self.plot(self.points2,
                      self.feldgrenzen2,
                      self.vorgewendeoption2,
                      self.umlaufbreite2,
                      self.vorgewende21,
                      self.vorgewende22)
            for point in self.points2:
                self.points_total.append(point)
        if self.feldgrenzen3 != "":
            self.points3 = self.calculate_field(self.feldgrenzen3,
                                           self.saatgut3)
            self.points = self.points3
            self.plot(self.points3,
                      self.feldgrenzen3,
                      self.vorgewendeoption3,
                      self.umlaufbreite3,
                      self.vorgewende31,
                      self.vorgewende32)
            for point in self.points3:
                self.points_total.append(point)
    def calculate_field(self, coords_str, plant):
        try:
            plants_distance = 0
            if plant == "Zuckerrübe":
                plants_distance = 40 #0.2
            elif plant == "Mais":
                plants_distance = 40 #0.35
            elif plant == "Getreide":
                plants_distance = 40 #0.25
            elif plant == "Test 10m":
                plants_distance = 10
            elif plant == "Test 100m":
                plants_distance = 100

            coords = self.convert_coordinates_string_to_list(coords_str)
            # Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
            utm_zone = get_utm_zone(coords)
            # UTM-Zone als Parameter speichern
            self.utm_zone = utm_zone
            # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
            coords_utm = geo_to_utm(coords, utm_zone)
            # Polygon erstellen
            polygon = Polygon(coords_utm)
        # Fehlermeldung für ungültige Eingaben
        except ValueError as error:
            messagebox.showerror("Fehler", f"Ungültige Eingabe: {str(error)}")
        # Wenn Berechnung manuell
        if self.currentsite_calc == 1:
            try:
                # Drehung des Musters (bis max. 60 Grad)
                angle_degrees = float(self.angle_entry.get())
                # Verschiebung des Musters in X-Richtung in % (max. so groß wie distance_plant)
                pattern_move_x = float(self.disp_x_entry.get())
                # Verschiebung des Musters in Y-Richtung in % (max. so groß wie das Doppelte der Dreieckshöhe)
                pattern_move_y = float(self.disp_y_entry.get())
                # Generiere die dreiecksförmigen Punkte innerhalb des Polygons
                points = generate_triangular_points_rotated(polygon,
                                                            plants_distance,
                                                            angle_degrees,
                                                            pattern_move_x,
                                                            pattern_move_y)
            # Fehlermeldung für ungültige Eingaben
            except ValueError as error:
                messagebox.showerror("Fehler", f"Ungültige Eingabe: {str(error)}")
        # Wenn Berechnung optimiert
        if self.currentsite_calc == 2:
            try:
                # Drehung des Musters (bis max. 60 Grad)
                maxiter = int(self.maxiter_entry.get())
                # Verschiebung des Musters in X-Richtung in % (max. so groß wie distance_plant)
                swarmsize = int(self.swarmsize_entry.get())
                # Generiere die dreiecksseitigen Punkte mithilfe der globalen Optimierungsfunktion
                points = pyswarm_global_optimization(polygon,
                                                     plants_distance,
                                                     maxiter,
                                                     swarmsize)
            # Fehlermeldung für ungültige Eingaben
            except ValueError as error:
                messagebox.showerror("Fehler", f"Ungültige Eingabe: {str(error)}")
        return points

    def plot(self, points, coords_str, vorgewendeoption, field_edge, vorgewende1, vorgewende2):


        coords = self.convert_coordinates_string_to_list(coords_str)
        # Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
        utm_zone = get_utm_zone(coords)
        # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
        coords_utm = geo_to_utm(coords, utm_zone)
        polygon = Polygon(coords_utm)
        # Zeichne das Polygon und die Punkte
        self.x, self.y = polygon.exterior.xy
        self.ax.fill(self.x, self.y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
        # Größe der Saatpunkte in Abhängigkeit der Gesamtpunktzahl
        for point in points:
            if 100 >= len(points) > 0:
                self.ax.plot(point.x, point.y, 'bo', markersize=5)
            elif 500 >= len(points) > 100:
                self.ax.plot(point.x, point.y, 'bo', markersize=3)
            elif 1000 >= len(points) > 500:
                self.ax.plot(point.x, point.y, 'bo', markersize=2)
            elif 5000 >= len(points) > 1000:
                self.ax.plot(point.x, point.y, 'bo', markersize=1)
            elif 15000 >= len(points) > 5000:
                self.ax.plot(point.x, point.y, 'bo', markersize=0.5)
            elif len(points) > 15000:
                self.ax.plot(point.x, point.y, 'bo', markersize=0.3)

        # Aktualisieren des Plots
        self.ax.plot(*polygon.exterior.xy, color='black')
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlabel('Östliche Koordinate [m]')
        self.ax.set_ylabel('Nördliche Koordinate [m]')
        # self.ax.ticklabel_format(style='sci', axis='x', scilimits=(3, 0))
        self.ax.set_title('Koordinatenpunkte der Aussaat mit gleichseitigem \n Dreiecksmuster im UTM-System', y=1.03)
        # Maximalen und minimalen Wert der X-Achse abrufen
        x_min, x_max = plt.gca().get_xlim()
        # Max. 3 Ticks für die Übersicht
        self.ax.set_xticks(np.linspace(x_min, x_max, 3))

        # Vorgewende berücksichtigen!
        if vorgewendeoption == "Individueller Bereich":
            if vorgewende1 != "":
                coords_headland1 = self.convert_coordinates_string_to_list(vorgewende1)
                # Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
                utm_zone = get_utm_zone(coords_headland1)
                # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
                coords_headland1_utm = geo_to_utm(coords_headland1, utm_zone)
                polygon_headland1 = Polygon(coords_headland1_utm)
                x, y = polygon_headland1.exterior.xy
                self.ax.fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen', hatch='//')
                self.ax.plot(*polygon_headland1.exterior.xy, color='black')
            if vorgewende2 != "":
                coords_headland2 = self.convert_coordinates_string_to_list(vorgewende2)
                # Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
                utm_zone = get_utm_zone(coords_headland2)
                # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
                coords_headland2_utm = geo_to_utm(coords_headland2, utm_zone)
                polygon_headland2 = Polygon(coords_headland2_utm)
                x, y = polygon_headland2.exterior.xy
                self.ax.fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen', hatch='//')
                self.ax.plot(*polygon_headland2.exterior.xy, color='black')
        else:
            if field_edge == 0 or "":
                pass
            else:
                # Verkleinertes Polygon mit Berücksichtigung des Feldrandes
                field_edge_polygon = reduced_polygon(coords_utm, float(field_edge))
                x_red, y_red = field_edge_polygon.exterior.xy
                self.ax.plot(x_red, y_red, 'g--', label='Reduziertes Polygon')
        # Neuzeichnen der Matplotlib-Figur
        self.canvas.draw()
    def convert_coordinates_string_to_list(self, coordinates_str):
        # Entfernen Sie die geschweiften Klammern am Anfang und Ende
        coordinates_str = coordinates_str.strip('{}')

        # Teilen Sie den String in Teile, die durch "}" getrennt sind
        coordinate_pairs = coordinates_str.split('}')

        # Entfernen Sie Leerzeichen und Klammern von jedem Koordinatenpaar
        cleaned_pairs = [pair.replace('{', '').replace('}', '').strip() for pair in coordinate_pairs]

        # Aufteilen der Koordinatenpaare in separate Zahlen und Umwandlung in Tupel
        coordinates_list = [tuple(map(float, pair.split())) for pair in cleaned_pairs]

        return coordinates_list
    def extract_coordinates_kml(self):
        self.ax.clear()
        selected_file = select_kml_file()
        koordinaten = extract_coordinates(selected_file)
        self.coords_entry.delete("1.0", "end")
        self.coords_entry.insert("1.0", text=koordinaten)
        # Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
        utm_zone = get_utm_zone(koordinaten)
        # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
        coords = geo_to_utm(koordinaten, utm_zone)
        polygon = Polygon(coords)
        x, y = polygon.exterior.xy
        self.ax.fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen')
        self.ax.plot(*polygon.exterior.xy, color='black')
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlabel('Breitengrad')
        self.ax.set_ylabel('Längengrad')
        self.ax.set_title('Darstellung des Feldes')
        # Neuzeichnen der Matplotlib-Figur
        self.canvas.draw()

    def extract_coordinates_kml_headland_1(self):
        selected_file = select_kml_file()
        koordinaten = extract_coordinates(selected_file)
        self.headland1_entry.delete("1.0", "end")
        self.headland1_entry.insert("1.0", text=koordinaten)
        # Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
        utm_zone = get_utm_zone(koordinaten)
        # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
        coords = geo_to_utm(koordinaten, utm_zone)
        polygon = Polygon(coords)
        x, y = polygon.exterior.xy
        self.ax.fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen', hatch='//')
        self.ax.plot(*polygon.exterior.xy, color='black')
        # Neuzeichnen der Matplotlib-Figur
        self.canvas.draw()

    def extract_coordinates_kml_headland_2(self):
        selected_file = select_kml_file()
        koordinaten = extract_coordinates(selected_file)
        self.headland2_entry.delete("1.0", "end")
        self.headland2_entry.insert("1.0", text=koordinaten)
        # Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
        utm_zone = get_utm_zone(koordinaten)
        # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
        coords = geo_to_utm(koordinaten, utm_zone)
        polygon = Polygon(coords)
        x, y = polygon.exterior.xy
        self.ax.fill(x, y, alpha=0.5, edgecolor='brown', facecolor='lightgreen', hatch='//')
        self.ax.plot(*polygon.exterior.xy, color='black')
        # Neuzeichnen der Matplotlib-Figur
        self.canvas.draw()
    def add_info_text_coords(self, event):
        self.info_label.configure(text="Info: Schreibe die Koordinaten der Feldpunkte in folgender \n Form auf: {Längengrad Breitengrad}{L2 B2}{L3 B3}...", text_color="gray")
    def remove_info_text(self, event):
        self.info_label.configure(text="")
    def generate_seed_points_list(self):
        # Dateiname
        file_name = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Textdateien", "*.txt"),
                       ("Alle Dateien", "*.*")])
        if self.feldgrenzen1 != "":
            fieldnumber = 1
            points_headland1_geo = ""
            points_headland2_geo = ""
            points_head_circ_geo = ""
            if self.vorgewendeoption1 == "Individueller Bereich":
                if self.vorgewende11 != "":
                    coords_headland1 = self.convert_coordinates_string_to_list(self.vorgewende11)
                    # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
                    coords_utm_head1 = geo_to_utm(coords_headland1, self.utm_zone)
                    # Polygon erstellen
                    polygon_headland1 = Polygon(coords_utm_head1)
                    points_headland1, self.points1 = points_headland_area(polygon_headland1, self.points1)
                    # Saatpunkte in geographische Koordinaten transformieren
                    points_headland1_geo = utm_to_geo_points(points_headland1, self.utm_zone)
                if self.vorgewende12 != "":
                    coords_headland2 = self.convert_coordinates_string_to_list(self.vorgewende12)
                    coords_utm_head2 = geo_to_utm(coords_headland2, self.utm_zone)
                    polygon_headland2 = Polygon(coords_utm_head2)
                    points_headland2, self.points1 = points_headland_area(polygon_headland2, self.points1)
                    points_headland2_geo = utm_to_geo_points(points_headland2, self.utm_zone)
            else:
                if self.umlaufbreite1 != "":
                    # Polygon erstellen
                    coords = self.convert_coordinates_string_to_list(self.feldgrenzen1)
                    # Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
                    utm_zone = get_utm_zone(coords)
                    # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
                    coords_utm = geo_to_utm(coords, utm_zone)
                    polygon_circ = reduced_polygon(coords_utm, float(self.umlaufbreite1))
                    points_head_circ, self.points1 = points_headland_circ(polygon_circ, self.points1)
                    # Saatpunkte in geographische Koordinaten transformieren
                    points_head_circ_geo = utm_to_geo_points(points_head_circ, self.utm_zone)
            points_geo = utm_to_geo_points(self.points1, self.utm_zone)
            # Speichere Koordinaten der Saat in einer Textdatei
            save_data_seed_coords(file_name, points_geo, fieldnumber, self.vorgewendeoption1, points_headland1_geo, points_headland2_geo, points_head_circ_geo, self.saatgut1)
        if self.feldgrenzen2 != "":
            fieldnumber = 2
            points_headland1_geo = ""
            points_headland2_geo = ""
            points_head_circ_geo = ""
            if self.vorgewendeoption2 == "Individueller Bereich":
                if self.vorgewende21 != "":
                    coords_headland1 = self.convert_coordinates_string_to_list(self.vorgewende21)
                    # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
                    coords_utm_head1 = geo_to_utm(coords_headland1, self.utm_zone)
                    # Polygon erstellen
                    polygon_headland1 = Polygon(coords_utm_head1)
                    points_headland1, self.points2 = points_headland_area(polygon_headland1, self.points2)
                    # Saatpunkte in geographische Koordinaten transformieren
                    points_headland1_geo = utm_to_geo_points(points_headland1, self.utm_zone)
                if self.vorgewende22 != "":
                    coords_headland2 = self.convert_coordinates_string_to_list(self.vorgewende22)
                    coords_utm_head2 = geo_to_utm(coords_headland2, self.utm_zone)
                    polygon_headland2 = Polygon(coords_utm_head2)
                    points_headland2, self.points2 = points_headland_area(polygon_headland2, self.points2)
                    points_headland2_geo = utm_to_geo_points(points_headland2, self.utm_zone)
            else:
                if self.umlaufbreite2 != "":
                    # Polygon erstellen
                    coords = self.convert_coordinates_string_to_list(self.feldgrenzen2)
                    # Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
                    utm_zone = get_utm_zone(coords)
                    # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
                    coords_utm = geo_to_utm(coords, utm_zone)
                    polygon_circ = reduced_polygon(coords_utm, float(self.umlaufbreite2))
                    points_head_circ, self.points2 = points_headland_circ(polygon_circ, self.points2)
                    # Saatpunkte in geographische Koordinaten transformieren
                    points_head_circ_geo = utm_to_geo_points(points_head_circ, self.utm_zone)
            points_geo = utm_to_geo_points(self.points2, self.utm_zone)
            # Speichere Koordinaten der Saat in einer Textdatei
            save_data_seed_coords(file_name, points_geo, fieldnumber, self.vorgewendeoption2, points_headland1_geo, points_headland2_geo,
                                  points_head_circ_geo, self.saatgut2)
        if self.feldgrenzen3 != "":
            fieldnumber = 3
            points_headland1_geo = ""
            points_headland2_geo = ""
            points_head_circ_geo = ""
            if self.vorgewendeoption1 == "Individueller Bereich":
                if self.vorgewende31 != "":
                    coords_headland1 = self.convert_coordinates_string_to_list(self.vorgewende31)
                    # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
                    coords_utm_head1 = geo_to_utm(coords_headland1, self.utm_zone)
                    # Polygon erstellen
                    polygon_headland1 = Polygon(coords_utm_head1)
                    points_headland1, self.points3 = points_headland_area(polygon_headland1, self.points3)
                    # Saatpunkte in geographische Koordinaten transformieren
                    points_headland1_geo = utm_to_geo_points(points_headland1, self.utm_zone)
                if self.vorgewende32 != "":
                    coords_headland2 = self.convert_coordinates_string_to_list(self.vorgewende32)
                    coords_utm_head2 = geo_to_utm(coords_headland2, self.utm_zone)
                    polygon_headland2 = Polygon(coords_utm_head2)
                    points_headland2, self.points3 = points_headland_area(polygon_headland2, self.points3)
                    points_headland2_geo = utm_to_geo_points(points_headland2, self.utm_zone)
            else:
                if self.umlaufbreite3 != "":
                    # Polygon erstellen
                    coords = self.convert_coordinates_string_to_list(self.feldgrenzen3)
                    # Anhang der ersten Koordinate aus der KML-Datei aktuelle UTM-Zone ermitteln
                    utm_zone = get_utm_zone(coords)
                    # Koordinaten in das UTM KGS projizieren, um in Metern weiterzurechnen
                    coords_utm = geo_to_utm(coords, utm_zone)
                    polygon_circ = reduced_polygon(coords_utm, float(self.umlaufbreite3))
                    points_head_circ, self.points3 = points_headland_circ(polygon_circ, self.points3)
                    # Saatpunkte in geographische Koordinaten transformieren
                    points_head_circ_geo = utm_to_geo_points(points_head_circ, self.utm_zone)
            points_geo = utm_to_geo_points(self.points3, self.utm_zone)
            # Speichere Koordinaten der Saat in einer Textdatei
            save_data_seed_coords(file_name, points_geo, fieldnumber, self.vorgewendeoption3, points_headland1_geo, points_headland2_geo,
                                  points_head_circ_geo, self.saatgut3)
    def save_as_svg(self):
        file_name = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG-Dateien", "*.svg"), ("Alle Dateien", "*.*")])
        # Speichere den Plot als SVG-Datei
        plt.savefig(file_name, format='svg')

    def save_as_kml(self):
        # Saatpunkte in geographische Koordinaten transformieren
        points_geo = utm_to_geo_points(self.points_total, self.utm_zone)
        # Dateiname
        file_name = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML-Dateien", "*.kml"), ("Alle Dateien", "*.*")])
        # Speichere Koordinaten der Saat in einer KML-Datei
        save_data_seed_coords_kml(file_name, points_geo)

    def plot_placeholder(self):
        # Platzhalter-Plot anzeigen
        self.ax.set_xlabel('X-Achse')
        self.ax.set_ylabel('Y-Achse')
        self.ax.set_title('Feld mit Saatmuster')
        self.canvas.draw()

if __name__ == "__main__":
    app = PlotApp()
    app.mainloop()

