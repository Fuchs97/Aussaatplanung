import tkinter
import tkintermapview

# create tkinter window
root_tk = tkinter.Tk()
root_tk.geometry(f"{800}x{600}")
root_tk.title("map_view_example.py")

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

def polygon_click(polygon):
    print(f"polygon clicked - text: {polygon.name}")

switzerland_marker = map_widget.set_address("Switzerland", marker=True, text="Switzerland")
map_widget.set_zoom(8)

polygon_1 = map_widget.set_polygon([(46.0732306, 6.0095215),
                                    (46.3393433, 6.2072754),
                                    (46.5890691, 6.1083984),
                                    (46.7624431, 6.4270020),
                                    (47.2717751, 7.0312500),
                                    (47.4726629, 6.9982910),
                                    (47.4057853, 7.3718262),
                                    (47.5468716, 7.9650879),
                                    (47.5691138, 8.4045410),
                                    (47.7540980, 8.6242676),
                                    (47.5691138, 9.4482422),
                                    (47.1897125, 9.5581055),
                                    (46.9352609, 9.8327637),
                                    (46.9727564, 10.4150391),
                                    (46.6418940, 10.4479980),
                                    (46.4605655, 10.0744629),
                                    (46.2786312, 10.1513672),
                                    (46.3469276, 9.5581055),
                                    (46.4454275, 9.3493652),
                                    (45.8211434, 8.9538574),
                                    (46.1037088, 8.6352539),
                                    (46.3696741, 8.3496094),
                                    (45.9740604, 7.9321289),
                                    (45.8900082, 7.0971680),
                                    (46.1417827, 6.8664551),
                                    (46.4151388, 6.7236328),
                                    (46.3772542, 6.4160156)],
                                    fill_color="white",
                                    outline_color="red",
                                    border_width=12,
                                    command=polygon_click,
                                    name="switzerland_polygon")

def add_marker_event(coords):
    print("Add marker:", coords)
    new_marker = map_widget.set_marker(coords[0], coords[1], text="new marker")


map_widget.add_right_click_menu_command(label="Add Marker",
                                        command=add_marker_event,
                                        pass_coords=True)


def left_click_event(coordinates_tuple):
    print("Left click event with coordinates:", coordinates_tuple)


map_widget.add_left_click_map_command(left_click_event)

root_tk.mainloop()
