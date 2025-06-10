"""
===============================================================================
 File Name   : format.py
 Author      : Jackson Bland
 Created On  : 
 Description : Contains daedalus app tkinter generating, formatted, change functions

 Dependencies:
     - tkinter, matplotlib

 Usage:
     - file is called as part of main loop and app class

 Notes:
     - 
===============================================================================
"""
from tkinter import *
from typing import Type
from main import Daedalus
from export import *

def create_frames(root, obj: Type[Daedalus]):
    """
    generate the frames of the main app

    Args:
        root: root Tk window
        obj: class object of Daedalus main app

    Returns:
        Generated tkinter frames in main root
    """
    # create top frame - where design options are located
    root.grid_rowconfigure(1,weight=1)
    root.grid_columnconfigure(0, weight=1)
    obj.top_frame = Frame(root, width=obj.view_width)
    obj.top_frame.grid(row=0, sticky='ew')
    # creating airfoil and wing design option sections
    obj.airfoil_frame = Frame(obj.top_frame, bg='#ECECEC', width=obj.view_width*0.5, height=obj.view_height*0.3, highlightbackground='black', highlightthickness=1)
    obj.wing_frame = Frame(obj.top_frame, bg='#ECECEC', width=obj.view_width*0.5, height=obj.view_height*0.3, highlightbackground='black', highlightthickness=1)
    obj.top_frame.grid_rowconfigure(0, weight=1)
    obj.top_frame.grid_columnconfigure(1, weight=1)
    obj.airfoil_frame.grid(row=0, column=0, sticky='ew')
    obj.wing_frame.grid(row=0, column=1, sticky='ew')

    # create bottom frame - where plot, view and export options are generated
    obj.bottom_frame = Frame(root, width=obj.view_width, height=obj.view_height*0.7)
    obj.bottom_frame.grid(row=1, sticky='ew')
    obj.plot_frame = Frame(obj.bottom_frame, bg='#ECECEC', width=obj.view_width*0.75, height=obj.view_height*0.7, highlightbackground='black', highlightthickness=1)
    obj.option_frame = Frame(obj.bottom_frame, bg='#ECECEC', width=obj.view_width*0.25, height=obj.view_height*0.7, highlightbackground='black', highlightthickness=1)
    obj.bottom_frame.grid_rowconfigure(0, weight=1)
    obj.bottom_frame.grid_columnconfigure(1, weight=1)
    obj.plot_frame.grid(row=0, column=0, sticky='ew')
    obj.option_frame.grid(row=0, column=1, sticky='ew')

    generate_widgets(root, obj)

def generate_widgets(root, obj: Type[Daedalus]):
    """
    Generate widgets on all frames

    Args:
        root: root Tk window
        obj: class object of Daedalus main app

    Returns:
        Generated tkinter widgets in main root
    """
    # or label
    obj.orLabel = Label(text='- or - ',bg='#ECECEC')
    obj.orLabel.place(x = 175, y = obj.view_height*0.25*0.5, anchor=CENTER)
    # chord length
    obj.chord_label = Label(text='Enter Chord Length', bg='#ECECEC')
    obj.chord_label.place(x=225,y=20, anchor=W)
    obj.chord = Entry(master=obj.airfoil_frame, width=21, font=('Helvitica','10'),fg='gray')
    obj.chord.place(x=225, y=40, anchor=W)
    obj.chord.insert(0,'1')
    obj.chord.bind("<Any-KeyRelease>", update_taper_ratio)
    obj.chord.bind("<Any-KeyRelease>", update_tip_chord)
    # max camber
    obj.max_camber_label = Label(text='Enter Max Camber', bg='#ECECEC')
    obj.max_camber_label.place(x=225, y=60, anchor=W)
    obj.max_camber = Entry(master=obj.airfoil_frame, width=21, font=('Helvitica','10'),fg='gray')
    obj.max_camber.place(x=225,y=80, anchor=W)
    obj.max_camber.insert(0,'2')
    # max camber location
    obj.max_camber_loc_label = Label(text='Enter Max Camber Location', bg='#ECECEC')
    obj.max_camber_loc_label.place(x=225, y=100, anchor=W)
    obj.max_camber_loc = Entry(master=obj.airfoil_frame, width=21, font=('Helvitica','10'),fg='gray')
    obj.max_camber_loc.place(x=225,y=120, anchor=W)
    obj.max_camber_loc.insert(0,'4')
    # max camber location
    obj.thickness_label = Label(text='Enter Thickness', bg='#ECECEC')
    obj.thickness_label.place(x=225, y=140, anchor=W)
    obj.thickness = Entry(master=obj.airfoil_frame, width=21, font=('Helvitica','10'),fg='gray')
    obj.thickness.place(x=225,y=160, anchor=W)
    obj.thickness.insert(0,'08')
    # dropdown menu for NACA airfoils
    obj.airfoil_drop_label = Label(text='Choose predefined airfoil', bg='#ECECEC')
    obj.airfoil_drop_label.place(x = 75, y = obj.view_height*0.25*0.5-20,anchor=CENTER)
    obj.option_var.set(obj.airfoil_options[6])
    obj.airfoil_dropdown = OptionMenu(obj.airfoil_frame, obj.option_var, *obj.airfoil_options, command=lambda: airfoil_fill(obj))
    obj.airfoil_dropdown.configure(bg='#7B7D7D',fg='white')
    obj.airfoil_dropdown.place(x=75,y = obj.view_height*0.25*0.5,anchor=CENTER)
    # incidence
    inc_label = Label(obj.airfoil_frame, text='Incidence (root)')
    inc_label.place(x=390, y=20, anchor=W)
    obj.incidence = Entry(master=obj.airfoil_frame, width=21, font=('Helvitica','10'),fg='gray')
    obj.incidence.place(x=390,y=40, anchor=W)
    obj.incidence.insert(0,'0')
    inc_choice_label = Label(obj.airfoil_frame, text='Rotate about')
    inc_choice_label.place(x=390, y=60, anchor=W)
    obj.inc_LE_TE = Checkbutton(obj.airfoil_frame, text='Leading Edge', variable=obj.inc_LE_TE_var, onvalue=True, offvalue=False, bg='#ECECEC', command=lambda: update_inc_centroid(obj))
    obj.inc_LE_TE.place(x=420,y=80, anchor=W)
    obj.inc_LE_TE_var.set(True)
    obj.inc_centroid = Checkbutton(obj.airfoil_frame, text='Centroid', variable=obj.inc_centroid_var, onvalue=True, offvalue=False, bg='#ECECEC', command=lambda: update_inc_LE(obj))
    obj.inc_centroid.place(x=420,y=100, anchor=W)
    
    ######################################
    #           making wing data         #
    ######################################
    obj.taper_label = Label(obj.wing_frame, text='Wing Taper\n------------------------------', bg='#ECECEC')
    obj.taper_label.place(x=100, y=25, anchor=CENTER)
    obj.taper_ratio = Entry(master=obj.wing_frame, width=5, font=('Helvitica','10'),fg='gray')
    obj.taper_ratio.place(x=50,y=70, anchor=CENTER)
    obj.taper_ratio.insert(0,'1')
    obj.tip_chord = Entry(master=obj.wing_frame, width=5, font=('Helvitica','10'),fg='gray')
    obj.tip_chord.place(x=150, y=70, anchor=CENTER)
    obj.tip_chord.insert(0,'1')
    obj.taper_choice_label = Label(obj.wing_frame, text='Taper ratio   -or-   Tip chord')
    obj.taper_choice_label.place(x=100,y=45, anchor=CENTER)
    # binding entries
    obj.taper_ratio.bind("<Any-KeyRelease>", lambda: update_tip_chord(obj))
    obj.tip_chord.bind("<Any-KeyRelease>", lambda: update_taper_ratio(obj))
    # get type of taper 
    obj.LE_taper = Checkbutton(obj.wing_frame, text='LE', variable=obj.LE_taper_var, onvalue=True, offvalue=False, bg='#ECECEC', command=lambda: [update_TE(obj), update_TRAP(obj), update_ellip(obj)])
    obj.TE_taper = Checkbutton(obj.wing_frame, text='TE', variable=obj.TE_taper_var, onvalue=True, offvalue=False, bg='#ECECEC', command=lambda: [update_LE(obj), update_TRAP(obj), update_ellip(obj)])
    obj.trap_taper = Checkbutton(obj.wing_frame, text='TRAP', variable=obj.trap_taper_var, onvalue=True, offvalue=False, bg='#ECECEC', command=lambda: [update_TE(obj), update_LE(obj), update_ellip(obj)])
    obj.LE_taper.place(x=20,y=100, anchor=W)
    obj.TE_taper.place(x=75,y=100, anchor=W)
    obj.trap_taper.place(x=130,y=100, anchor=W)
    obj.TE_taper_var.set(True)
    # number of airfoils
    obj.airfoil_num_label = Label(obj.wing_frame, text='------------------------------\nChoose Number of Airfoils', bg='#ECECEC')
    obj.airfoil_num_label.place(x=100, y=130, anchor=CENTER)
    obj.airfoil_num_slide = Scale(obj.wing_frame, from_=1, to=25, orient='horizontal',bg='#ECECEC', variable = obj.airfoil_num_slide_var )
    obj.airfoil_num_slide.place(x=100,y=170, anchor=CENTER)
    # span value
    obj.wingspan_lab = Label(obj.wing_frame, text='Wing Span', bg='#ECECEC')
    obj.wingspan_lab.place(x=200, y=20, anchor=W)
    obj.wingspan = Entry(obj.wing_frame, width=12, font=('Helvitica','10'),fg='gray')
    obj.wingspan.place(x=200, y=40, anchor=W)
    obj.wingspan.insert(0,'1')
    obj.fuse_width_lab = Label(obj.wing_frame, text='Fuse Width', bg='#ECECEC')
    obj.fuse_width_lab.place(x=200, y=60, anchor=W)
    obj.fuse_width = Entry(obj.wing_frame, width=12, font=('Helvitica','10'),fg='gray')
    obj.fuse_width.place(x=200, y=80, anchor=W)
    obj.fuse_width.insert(0,'0')
    # sweep value
    obj.sweep_label = Label(obj.wing_frame, text='Sweep Angle', bg='#ECECEC')
    obj.sweep_label.place(x=320, y=20, anchor=W)
    obj.sweep = Entry(obj.wing_frame, width=12, font=('Helvitica','10'),fg='gray')
    obj.sweep.place(x=320, y=40, anchor=W)
    obj.sweep.insert(0,'0')
    # washout value
    obj.washout_label = Label(obj.wing_frame, text='Washout Angle', bg='#ECECEC')
    obj.washout_label.place(x=320, y=60, anchor=W)
    obj.washout = Entry(obj.wing_frame, width=12, font=('Helvitica','10'),fg='gray')
    obj.washout.place(x=320, y=80, anchor=W)
    obj.washout.insert(0,'0')
    # hedral value
    obj.dihedral_label = Label(obj.wing_frame, text='Dihedral Angle', bg='#ECECEC')
    obj.dihedral_label.place(x=440, y=20, anchor=W)
    obj.dihedral = Entry(obj.wing_frame, width=12, font=('Helvitica','10'),fg='gray')
    obj.dihedral.place(x=440, y=40, anchor=W)
    obj.dihedral.insert(0,'0')
    # elliptical option
    obj.elliptical = Checkbutton(obj.wing_frame, text='Elliptical\nPlanform', variable=obj.elliptical_var, onvalue=True, offvalue=False, bg='#ECECEC', command=lambda: [update_LE(obj), update_TE(obj), update_TRAP(obj)])
    obj.elliptical.place(x=440, y=75, anchor=W)        
    
    #####################################
    #           making options          #
    #####################################
    # generate plot button
    obj.generate_plot_button = Button(master=obj.option_frame, command=lambda: [obj.generate_plot(obj.export_option_val),update_export_options_menu(obj, False)], height=2, width=25, text='Plot / Refresh', bg='#21A820', fg='white', activebackground='#1E821D', font=('Helvetica',12,'bold'))
    obj.generate_plot_button.place(x=obj.view_width*0.25*0.5,y=obj.view_height*0.01, anchor=N)
    obj.camber_line_plot = Checkbutton(obj.option_frame, text='Plot Camber Line', variable=obj.camber_bool, onvalue=True, offvalue=False, bg='#ECECEC')
    obj.camber_line_plot.place(x=obj.view_width*0.01,y=80, anchor=W)
    obj.thickness_line_plot = Checkbutton(obj.option_frame, text='Plot Thickness Line', variable=obj.thick_bool, onvalue=True, offvalue=False, bg='#ECECEC')
    obj.thickness_line_plot.place(x=obj.view_width*0.01,y=100, anchor=W)
    obj.guideline_plot = Checkbutton(obj.option_frame, text='Plot Guidelines', variable=obj.guideline_plot_bool, onvalue=True, offvalue=False, bg='#ECECEC')
    obj.guideline_plot.place(x=obj.view_width*0.01, y=120, anchor=W)

    # generate reset button
    obj.reset_button = Button(master=obj.option_frame, command=lambda: reset(obj), height=1, width=25, text='Reset All', bg='#F75409', fg='white', activebackground='#923409', font=('Helvetica',10,'bold'))
    obj.reset_button.place(x=obj.view_width*0.25*0.5,y=obj.view_height*0.22, anchor=N)
    # quit button
    obj.quit_button = Button(master=obj.option_frame, text='Quit', fg='white', command=root.destroy, width = 25, height=1, bg='#E52D06', compound='c', activebackground='#B72607', font=('Helvetica',10,'bold'))
    obj.quit_button.place(x = obj.view_width*0.25*0.5, y = obj.view_height*0.65, anchor=S)
    # export button
    obj.export_button = Button(master=obj.option_frame, text='Export', command=lambda: export_data(obj), width=25, height=2, bg='#00AFF0',fg='white', compound='c', activebackground='#0080AF', font=('Helvetica',10,'bold'))
    obj.export_button.place(x = obj.view_width*0.25*0.5, y = obj.view_height*0.5, anchor=S)
    # export selection dropdown
    obj.highlight_button = Button(obj.option_frame, command=lambda: [obj.generate_plot(obj.export_option_val)], text='Highlight', fg='white', bg='#00AFF0', height= 1,font=('Helvetica',11,'bold'))
    obj.highlight_button.place(x = 255, y = obj.view_height*0.4, anchor=E)
    obj.export_option_val.set(obj.export_options[0])
    obj.export_option = OptionMenu(obj.option_frame, obj.export_option_val,*obj.export_options)
    obj.export_option.config(bg='#00AFF0', fg='white', height=1, font=('Helvetica',10,'bold'))
    obj.export_option.place(x = 45, y = obj.view_height*0.4, anchor=W)
    obj.export_option_label = Label(obj.option_frame, text='-----------------------------------------------------\nChoose airfoil to export as .txt file\n-----------------------------------------------------', bg='#ECECEC')
    obj.export_option_label.place(x=obj.view_width*0.25*0.5,y = obj.view_height*0.30, anchor=CENTER)

def update_taper_ratio(obj):
    try:
        tip = float(obj.tip_chord.get())
        root = float(obj.chord.get())
        obj.taper_ratio.delete(0, END)
        obj.taper_ratio.insert(0, str(round(tip/root,2)))
    except:
        obj.taper_ratio.delete(0, END)
        obj.taper_ratio.insert(0, 'NaN')

def update_tip_chord(obj):
    try:
        c = float(obj.chord.get())
        tr = float(obj.taper_ratio.get())
        obj.tip_chord.delete(0, END)
        obj.tip_chord.insert(0,str(round(tr*c,2)))
    except:
        obj.tip_chord.delete(0, END)
        obj.tip_chord.insert(0,'NaN')

def airfoil_fill(obj):
    NACAcode = obj.option_var.get()[-4:]
    M = NACAcode[0]
    P = NACAcode[1]
    XX = NACAcode[2:]
    obj.max_camber.delete(0, END)
    obj.max_camber.insert(0, M)
    obj.max_camber_loc.delete(0, END)
    obj.max_camber_loc.insert(0, P)
    obj.thickness.delete(0, END)
    obj.thickness.insert(0,XX)

def update_TE(obj):
    obj.TE_taper_var.set(False)

def update_TRAP(obj):
    obj.trap_taper_var.set(False)

def update_ellip(obj):
    obj.elliptical_var.set(False)

def update_inc_centroid(obj):
    obj.inc_centroid_var.set(False)

def update_export_options_menu(obj, reset_):
    if reset_ == True:
        obj.export_options = ['All']
        obj.export_option['menu'].delete(0,'end')
        for string in obj.export_options:
            obj.export_option['menu'].add_command(label=string, command=lambda value=string: obj.export_option_val.set(value))
    else:
        # export saving
        obj.export_options = ['All']
        if obj.airfoil_num_slide.get() != 1:
            for a in range(obj.airfoil_num_slide.get()*2): obj.export_options.append('Airfoil '+str(a))
            obj.export_option['menu'].delete(0,'end')
            for string in obj.export_options:
                obj.export_option['menu'].add_command(label=string, command=lambda value=string: obj.export_option_val.set(value))
        else:
            for a in range(obj.airfoil_num_slide.get()): obj.export_options.append('Airfoil '+str(a))
            obj.export_option['menu'].delete(0,'end')
            for string in obj.export_options:
                obj.export_option['menu'].add_command(label=string, command=lambda value=string: obj.export_option_val.set(value))

def update_inc_LE(obj):
    obj.inc_LE_TE_var.set(False)

def update_LE(obj):
    obj.LE_taper_var.set(False)

def reset(obj):
    obj.max_camber.delete(0, END)
    obj.max_camber.insert(0, '2')
    obj.max_camber_loc.delete(0, END)
    obj.max_camber_loc.insert(0, '4')
    obj.thickness.delete(0, END)
    obj.thickness.insert(0,'08')
    obj.taper_ratio.delete(0,END)
    obj.taper_ratio.insert(0,'1')
    obj.tip_chord.delete(0,END)
    obj.tip_chord.insert(0,'1')
    obj.chord.delete(0,END)
    obj.chord.insert(0,'1')
    obj.incidence.delete(0, END)
    obj.incidence.insert(0,'0')
    obj.wingspan.delete(0, END)
    obj.wingspan.insert(0,'1')
    obj.fuse_width.delete(0, END)
    obj.fuse_width.insert(0,'0')
    obj.sweep.delete(0, END)
    obj.sweep.insert(0,'0')
    obj.washout.delete(0, END)
    obj.washout.insert(0,'0')
    obj.dihedral.delete(0, END)
    obj.dihedral.insert(0, '0')
    obj.option_var.set(obj.airfoil_options[6])
    obj.camber_bool.set(False)
    obj.thick_bool.set(False)
    obj.inc_LE_TE_var.set(True)
    obj.inc_centroid_var.set(False)
    obj.LE_taper_var.set(False)
    obj.TE_taper_var.set(True)
    obj.trap_taper_var.set(False)
    obj.elliptical_var.set(False)
    obj.guideline_plot_bool.set(False)
    obj.airfoil_num_slide_var.set(1)
    obj.update_export_options_menu(True)
    obj.ax.clear()
    obj.ax.set_xticklabels([])     # create axes labels and get rid of tick mark values to clean up plot
    obj.ax.set_yticklabels([])     #
    obj.ax.set_zticklabels([])     #
    obj.ax.set_zlim(-1/2*1, 1/2*1) #
    obj.plot_origin_axis(1)        #
    obj.canvas.draw()              #  