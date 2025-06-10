"""
===============================================================================
 File Name   : main.py
 Author      : Jackson Bland
 Created On  : 
 Description : Contains main daedalus app class and loop

 Dependencies:
     - tkinter, matplotlib, calculations, export, guidelines

 Usage:
     - initiate daedalus loop

 Notes:
     - 
===============================================================================
"""
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from export import *
from calculations import *
from guidelines import *

class Daedalus:
    def __init__(self, master):
        self.view_width = 1200
        self.view_height = 700
        root.geometry('{}x{}'.format(self.view_width, self.view_height))

        # initialize input variables to be assigned to widgets
        self.airfoil_options = ['NACA 0006', 
                                'NACA 0009', 
                                'NACA 0012', 
                                'NACA 0018', 
                                'NACA 0024', 
                                'NACA 1410', 
                                'NACA 2408', 
                                'NACA 2411', 
                                'NACA 2414', 
                                'NACA 2418', 
                                'NACA 2424', 
                                'NACA 4415']
        self.export_options = ['All']
        self.option_var = StringVar()
        self.export_option_val = StringVar()
        self.camber_bool = BooleanVar()
        self.thick_bool = BooleanVar()
        self.airfoil_num_slide_var = IntVar()
        self.inc_LE_TE_var = BooleanVar()
        self.inc_centroid_var = BooleanVar()
        self.LE_taper_var = BooleanVar()
        self.TE_taper_var = BooleanVar()
        self.trap_taper_var = BooleanVar()
        self.elliptical_var = BooleanVar()
        self.guideline_plot_bool = BooleanVar()

        self.create_frames()

    def create_frames(self):
        """
        generate the frames of the main app

        Args:
            root: root Tk window
            : class ect of Daedalus main app

        Returns:
            Generated tkinter frames in main root
        """
        # create top frame - where design options are located
        root.grid_rowconfigure(1,weight=1)
        root.grid_columnconfigure(0, weight=1)
        self.top_frame = Frame(root, width=self.view_width)
        self.top_frame.grid(row=0, sticky='ew')
        # creating airfoil and wing design option sections
        self.airfoil_frame = Frame(self.top_frame, bg='#ECECEC', width=self.view_width*0.5, height=self.view_height*0.3, highlightbackground='black', highlightthickness=1)
        self.wing_frame = Frame(self.top_frame, bg='#ECECEC', width=self.view_width*0.5, height=self.view_height*0.3, highlightbackground='black', highlightthickness=1)
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.airfoil_frame.grid(row=0, column=0, sticky='ew')
        self.wing_frame.grid(row=0, column=1, sticky='ew')

        # create bottom frame - where plot, view and export options are generated
        self.bottom_frame = Frame(root, width=self.view_width, height=self.view_height*0.7)
        self.bottom_frame.grid(row=1, sticky='ew')
        self.plot_frame = Frame(self.bottom_frame, bg='#ECECEC', width=self.view_width*0.75, height=self.view_height*0.7, highlightbackground='black', highlightthickness=1)
        self.option_frame = Frame(self.bottom_frame, bg='#ECECEC', width=self.view_width*0.25, height=self.view_height*0.7, highlightbackground='black', highlightthickness=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.plot_frame.grid(row=0, column=0, sticky='ew')
        self.option_frame.grid(row=0, column=1, sticky='ew')

        self.generate_widgets()

    def generate_widgets(self):
        """
        Generate widgets on all frames

        Args:
            root: root Tk window
            : class ect of Daedalus main app

        Returns:
            Generated tkinter widgets in main root
        """
        # or label
        self.orLabel = Label(text='- or - ',bg='#ECECEC')
        self.orLabel.place(x = 175, y = self.view_height*0.25*0.5, anchor=CENTER)
        # chord length
        self.chord_label = Label(text='Enter Chord Length', bg='#ECECEC')
        self.chord_label.place(x=225,y=20, anchor=W)
        self.chord = Entry(master=self.airfoil_frame, width=21, font=('Helvitica','10'),fg='gray')
        self.chord.place(x=225, y=40, anchor=W)
        self.chord.insert(0,'1')
        # self.chord.bind("<Any-KeyRelease>", self.update_taper_ratio)
        # self.chord.bind("<Any-KeyRelease>", self.update_tip_chord)
        # max camber
        self.max_camber_label = Label(text='Enter Max Camber', bg='#ECECEC')
        self.max_camber_label.place(x=225, y=60, anchor=W)
        self.max_camber = Entry(master=self.airfoil_frame, width=21, font=('Helvitica','10'),fg='gray')
        self.max_camber.place(x=225,y=80, anchor=W)
        self.max_camber.insert(0,'2')
        # max camber location
        self.max_camber_loc_label = Label(text='Enter Max Camber Location', bg='#ECECEC')
        self.max_camber_loc_label.place(x=225, y=100, anchor=W)
        self.max_camber_loc = Entry(master=self.airfoil_frame, width=21, font=('Helvitica','10'),fg='gray')
        self.max_camber_loc.place(x=225,y=120, anchor=W)
        self.max_camber_loc.insert(0,'4')
        # max camber location
        self.thickness_label = Label(text='Enter Thickness', bg='#ECECEC')
        self.thickness_label.place(x=225, y=140, anchor=W)
        self.thickness = Entry(master=self.airfoil_frame, width=21, font=('Helvitica','10'),fg='gray')
        self.thickness.place(x=225,y=160, anchor=W)
        self.thickness.insert(0,'08')
        # dropdown menu for NACA airfoils
        self.airfoil_drop_label = Label(text='Choose predefined airfoil', bg='#ECECEC')
        self.airfoil_drop_label.place(x = 75, y = self.view_height*0.25*0.5-20,anchor=CENTER)
        self.option_var.set(self.airfoil_options[6])
        self.airfoil_dropdown = OptionMenu(self.airfoil_frame, self.option_var, *self.airfoil_options, command=self.airfoil_fill)
        self.airfoil_dropdown.configure(bg='#7B7D7D',fg='white')
        self.airfoil_dropdown.place(x=75,y = self.view_height*0.25*0.5,anchor=CENTER)
        # incidence
        inc_label = Label(self.airfoil_frame, text='Incidence (root)')
        inc_label.place(x=390, y=20, anchor=W)
        self.incidence = Entry(master=self.airfoil_frame, width=21, font=('Helvitica','10'),fg='gray')
        self.incidence.place(x=390,y=40, anchor=W)
        self.incidence.insert(0,'0')
        inc_choice_label = Label(self.airfoil_frame, text='Rotate about')
        inc_choice_label.place(x=390, y=60, anchor=W)
        self.inc_LE_TE = Checkbutton(self.airfoil_frame, text='Leading Edge', variable=self.inc_LE_TE_var, onvalue=True, offvalue=False, bg='#ECECEC', command=self.update_inc_centroid)
        self.inc_LE_TE.place(x=420,y=80, anchor=W)
        self.inc_LE_TE_var.set(True)
        self.inc_centroid = Checkbutton(self.airfoil_frame, text='Centroid', variable=self.inc_centroid_var, onvalue=True, offvalue=False, bg='#ECECEC', command=self.update_inc_LE)
        self.inc_centroid.place(x=420,y=100, anchor=W)
        
        ######################################
        #           making wing data         #
        ######################################
        self.taper_label = Label(self.wing_frame, text='Wing Taper\n------------------------------', bg='#ECECEC')
        self.taper_label.place(x=100, y=25, anchor=CENTER)
        self.taper_ratio = Entry(master=self.wing_frame, width=5, font=('Helvitica','10'),fg='gray')
        self.taper_ratio.place(x=50,y=70, anchor=CENTER)
        self.taper_ratio.insert(0,'1')
        self.tip_chord = Entry(master=self.wing_frame, width=5, font=('Helvitica','10'),fg='gray')
        self.tip_chord.place(x=150, y=70, anchor=CENTER)
        self.tip_chord.insert(0,'1')
        self.taper_choice_label = Label(self.wing_frame, text='Taper ratio   -or-   Tip chord')
        self.taper_choice_label.place(x=100,y=45, anchor=CENTER)
        # binding entries
        self.tip_chord.bind("<Any-KeyRelease>", self.update_taper_ratio)
        self.taper_ratio.bind("<Any-KeyRelease>", self.update_tip_chord)
        # get type of taper 
        self.LE_taper = Checkbutton(self.wing_frame, text='LE', variable=self.LE_taper_var, onvalue=True, offvalue=False, bg='#ECECEC', command=lambda: [self.update_TE(), self.update_TRAP(), self.update_ellip()])
        self.TE_taper = Checkbutton(self.wing_frame, text='TE', variable=self.TE_taper_var, onvalue=True, offvalue=False, bg='#ECECEC', command=lambda: [self.update_LE(), self.update_TRAP(), self.update_ellip()])
        self.trap_taper = Checkbutton(self.wing_frame, text='TRAP', variable=self.trap_taper_var, onvalue=True, offvalue=False, bg='#ECECEC', command=lambda: [self.update_TE(), self.update_LE(), self.update_ellip()])
        self.LE_taper.place(x=20,y=100, anchor=W)
        self.TE_taper.place(x=75,y=100, anchor=W)
        self.trap_taper.place(x=130,y=100, anchor=W)
        self.TE_taper_var.set(True)
        # number of airfoils
        self.airfoil_num_label = Label(self.wing_frame, text='------------------------------\nChoose Number of Airfoils', bg='#ECECEC')
        self.airfoil_num_label.place(x=100, y=130, anchor=CENTER)
        self.airfoil_num_slide = Scale(self.wing_frame, from_=1, to=25, orient='horizontal',bg='#ECECEC', variable = self.airfoil_num_slide_var )
        self.airfoil_num_slide.place(x=100,y=170, anchor=CENTER)
        # span value
        self.wingspan_lab = Label(self.wing_frame, text='Wing Span', bg='#ECECEC')
        self.wingspan_lab.place(x=200, y=20, anchor=W)
        self.wingspan = Entry(self.wing_frame, width=12, font=('Helvitica','10'),fg='gray')
        self.wingspan.place(x=200, y=40, anchor=W)
        self.wingspan.insert(0,'1')
        self.fuse_width_lab = Label(self.wing_frame, text='Fuse Width', bg='#ECECEC')
        self.fuse_width_lab.place(x=200, y=60, anchor=W)
        self.fuse_width = Entry(self.wing_frame, width=12, font=('Helvitica','10'),fg='gray')
        self.fuse_width.place(x=200, y=80, anchor=W)
        self.fuse_width.insert(0,'0')
        # sweep value
        self.sweep_label = Label(self.wing_frame, text='Sweep Angle', bg='#ECECEC')
        self.sweep_label.place(x=320, y=20, anchor=W)
        self.sweep = Entry(self.wing_frame, width=12, font=('Helvitica','10'),fg='gray')
        self.sweep.place(x=320, y=40, anchor=W)
        self.sweep.insert(0,'0')
        # washout value
        self.washout_label = Label(self.wing_frame, text='Washout Angle', bg='#ECECEC')
        self.washout_label.place(x=320, y=60, anchor=W)
        self.washout = Entry(self.wing_frame, width=12, font=('Helvitica','10'),fg='gray')
        self.washout.place(x=320, y=80, anchor=W)
        self.washout.insert(0,'0')
        # hedral value
        self.dihedral_label = Label(self.wing_frame, text='Dihedral Angle', bg='#ECECEC')
        self.dihedral_label.place(x=440, y=20, anchor=W)
        self.dihedral = Entry(self.wing_frame, width=12, font=('Helvitica','10'),fg='gray')
        self.dihedral.place(x=440, y=40, anchor=W)
        self.dihedral.insert(0,'0')
        # elliptical option
        self.elliptical = Checkbutton(self.wing_frame, text='Elliptical\nPlanform', variable=self.elliptical_var, onvalue=True, offvalue=False, bg='#ECECEC', command=lambda: [self.update_LE(), self.update_TE(), self.update_TRAP()])
        self.elliptical.place(x=440, y=75, anchor=W)        
        
        #####################################
        #           making options          #
        #####################################
        # generate plot button
        self.generate_plot_button = Button(master=self.option_frame, command=lambda: [self.generate_plot(self.export_option_val), self.update_export_options_menu(False)], height=2, width=25, text='Plot / Refresh', bg='#21A820', fg='white', activebackground='#1E821D', font=('Helvetica',12,'bold'))
        self.generate_plot_button.place(x=self.view_width*0.25*0.5,y=self.view_height*0.01, anchor=N)
        self.camber_line_plot = Checkbutton(self.option_frame, text='Plot Camber Line', variable=self.camber_bool, onvalue=True, offvalue=False, bg='#ECECEC')
        self.camber_line_plot.place(x=self.view_width*0.01,y=80, anchor=W)
        self.thickness_line_plot = Checkbutton(self.option_frame, text='Plot Thickness Line', variable=self.thick_bool, onvalue=True, offvalue=False, bg='#ECECEC')
        self.thickness_line_plot.place(x=self.view_width*0.01,y=100, anchor=W)
        self.guideline_plot = Checkbutton(self.option_frame, text='Plot Guidelines', variable=self.guideline_plot_bool, onvalue=True, offvalue=False, bg='#ECECEC')
        self.guideline_plot.place(x=self.view_width*0.01, y=120, anchor=W)

        # generate reset button
        self.reset_button = Button(master=self.option_frame, command=self.reset, height=1, width=25, text='Reset All', bg='#F75409', fg='white', activebackground='#923409', font=('Helvetica',10,'bold'))
        self.reset_button.place(x=self.view_width*0.25*0.5,y=self.view_height*0.22, anchor=N)
        # quit button
        self.quit_button = Button(master=self.option_frame, text='Quit', fg='white', command=root.destroy, width = 25, height=1, bg='#E52D06', compound='c', activebackground='#B72607', font=('Helvetica',10,'bold'))
        self.quit_button.place(x = self.view_width*0.25*0.5, y = self.view_height*0.65, anchor=S)
        # export button
        self.export_button = Button(master=self.option_frame, text='Export', command=export_data, width=25, height=2, bg='#00AFF0',fg='white', compound='c', activebackground='#0080AF', font=('Helvetica',10,'bold'))
        self.export_button.place(x = self.view_width*0.25*0.5, y = self.view_height*0.5, anchor=S)
        # export selection dropdown
        self.highlight_button = Button(self.option_frame, command=lambda: self.generate_plot(self.export_option_val), text='Highlight', fg='white', bg='#00AFF0', height= 1,font=('Helvetica',11,'bold'))
        self.highlight_button.place(x = 255, y = self.view_height*0.4, anchor=E)
        self.export_option_val.set(self.export_options[0])
        self.export_option = OptionMenu(self.option_frame, self.export_option_val,*self.export_options)
        self.export_option.config(bg='#00AFF0', fg='white', height=1, font=('Helvetica',10,'bold'))
        self.export_option.place(x = 45, y = self.view_height*0.4, anchor=W)
        self.export_option_label = Label(self.option_frame, text='-----------------------------------------------------\nChoose airfoil to export as .txt file\n-----------------------------------------------------', bg='#ECECEC')
        self.export_option_label.place(x=self.view_width*0.25*0.5,y = self.view_height*0.30, anchor=CENTER)

        self.generate_empty_plot()

    def update_taper_ratio(self, *args):
        try:
            tip = float(self.tip_chord.get())
            root = float(self.chord.get())
            self.taper_ratio.delete(0, END)
            self.taper_ratio.insert(0, str(round(tip/root,2)))
        except:
            self.taper_ratio.delete(0, END)
            self.taper_ratio.insert(0, 'NaN')

    def update_tip_chord(self, *args):
        try:
            c = float(self.chord.get())
            tr = float(self.taper_ratio.get())
            self.tip_chord.delete(0, END)
            self.tip_chord.insert(0,str(round(tr*c,2)))
        except:
            self.tip_chord.delete(0, END)
            self.tip_chord.insert(0,'NaN')

    def airfoil_fill(self, *args):
        NACAcode = self.option_var.get()[-4:]
        M = NACAcode[0]
        P = NACAcode[1]
        XX = NACAcode[2:]
        self.max_camber.delete(0, END)
        self.max_camber.insert(0, M)
        self.max_camber_loc.delete(0, END)
        self.max_camber_loc.insert(0, P)
        self.thickness.delete(0, END)
        self.thickness.insert(0,XX)

    def update_TE(self):
        self.TE_taper_var.set(False)

    def update_TRAP(self):
        self.trap_taper_var.set(False)

    def update_ellip(self):
        self.elliptical_var.set(False)

    def update_inc_centroid(self):
        self.inc_centroid_var.set(False)

    def update_export_options_menu(self, reset_):
        if reset_ == True:
            self.export_options = ['All']
            self.export_option['menu'].delete(0,'end')
            for string in self.export_options:
                self.export_option['menu'].add_command(label=string, command=lambda value=string: self.export_option_val.set(value))
        else:
            # export saving
            self.export_options = ['All']
            if self.airfoil_num_slide.get() != 1:
                for a in range(self.airfoil_num_slide.get()*2): self.export_options.append('Airfoil '+str(a))
                self.export_option['menu'].delete(0,'end')
                for string in self.export_options:
                    self.export_option['menu'].add_command(label=string, command=lambda value=string: self.export_option_val.set(value))
            else:
                for a in range(self.airfoil_num_slide.get()): self.export_options.append('Airfoil '+str(a))
                self.export_option['menu'].delete(0,'end')
                for string in self.export_options:
                    self.export_option['menu'].add_command(label=string, command=lambda value=string: self.export_option_val.set(value))

    def update_inc_LE(self):
        self.inc_LE_TE_var.set(False)

    def update_LE(self):
        self.LE_taper_var.set(False)

    def reset(self):
        self.max_camber.delete(0, END)
        self.max_camber.insert(0, '2')
        self.max_camber_loc.delete(0, END)
        self.max_camber_loc.insert(0, '4')
        self.thickness.delete(0, END)
        self.thickness.insert(0,'08')
        self.taper_ratio.delete(0,END)
        self.taper_ratio.insert(0,'1')
        self.tip_chord.delete(0,END)
        self.tip_chord.insert(0,'1')
        self.chord.delete(0,END)
        self.chord.insert(0,'1')
        self.incidence.delete(0, END)
        self.incidence.insert(0,'0')
        self.wingspan.delete(0, END)
        self.wingspan.insert(0,'1')
        self.fuse_width.delete(0, END)
        self.fuse_width.insert(0,'0')
        self.sweep.delete(0, END)
        self.sweep.insert(0,'0')
        self.washout.delete(0, END)
        self.washout.insert(0,'0')
        self.dihedral.delete(0, END)
        self.dihedral.insert(0, '0')
        self.option_var.set(self.airfoil_options[6])
        self.camber_bool.set(False)
        self.thick_bool.set(False)
        self.inc_LE_TE_var.set(True)
        self.inc_centroid_var.set(False)
        self.LE_taper_var.set(False)
        self.TE_taper_var.set(True)
        self.trap_taper_var.set(False)
        self.elliptical_var.set(False)
        self.guideline_plot_bool.set(False)
        self.airfoil_num_slide_var.set(1)
        self.update_export_options_menu(True)
        self.ax.clear()
        self.ax.set_xticklabels([])     # create axes labels and get rid of tick mark values to clean up plot
        self.ax.set_yticklabels([])     #
        self.ax.set_zticklabels([])     #
        self.ax.set_zlim(-1/2*1, 1/2*1) #
        self.plot_origin_axis(1)        #
        self.canvas.draw()              #  

    def update_export_options_menu(self, reset_):
        if reset_ == True:
            self.export_options = ['All']
            self.export_option['menu'].delete(0,'end')
            for string in self.export_options:
                self.export_option['menu'].add_command(label=string, command=lambda value=string: self.export_option_val.set(value))
        else:
            # export saving
            self.export_options = ['All']
            if self.airfoil_num_slide.get() != 1:
                for a in range(self.airfoil_num_slide.get()*2): self.export_options.append('Airfoil '+str(a))
                self.export_option['menu'].delete(0,'end')
                for string in self.export_options:
                    self.export_option['menu'].add_command(label=string, command=lambda value=string: self.export_option_val.set(value))
            else:
                for a in range(self.airfoil_num_slide.get()): self.export_options.append('Airfoil '+str(a))
                self.export_option['menu'].delete(0,'end')
                for string in self.export_options:
                    self.export_option['menu'].add_command(label=string, command=lambda value=string: self.export_option_val.set(value))
        
    def plot_origin_axis(self, chord):
        self.ax.scatter(0,0,0, color='red')
        unit_length = chord*0.1
        self.ax.plot([0,unit_length],[0,0],[0,0], color='red')
        self.ax.plot([0,0],[0,unit_length],[0,0], color='green')
        self.ax.plot([0,0],[0,0],[0,unit_length], color='blue')

    def generate_empty_plot(self):
        #######################################
        #           making main plot          #
        #######################################
        px = 1/plt.rcParams['figure.dpi']  # pixel in inches
        fig = Figure(figsize=(self.view_width*0.75*px, self.view_height*0.75*px))       # create figure

        self.ax = fig.add_subplot(111, projection="3d")     # create subplot with 3d projection
        fig.tight_layout()
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_zticklabels([])
        self.ax.view_init(0,270)
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)    # create canvas to place the plot
        self.canvas.get_tk_widget().pack()
        ####### plotting origin ###########
        self.ax.scatter(0,0,0, color='red')
        self.ax.set_axis_off()

    def generate_plot(self, export_option_val):
        '''Generate the main plot of the GUI, takes in multiple inputs from multiple options at various stages on completeness'''    
        self.ax.clear() # clears plot such that an updated one can be run
        rc = float(self.chord.get())
        M = float(self.max_camber.get())
        P = float(self.max_camber_loc.get())
        XX = float(self.thickness.get())
        ri = float(self.incidence.get())
        ws = float(self.wingspan.get())
        fw = float(self.fuse_width.get())
        tr = float(self.taper_ratio.get())
        an = self.airfoil_num_slide.get()
        wo = float(self.washout.get())
        sw = float(self.sweep.get())
        dh = float(self.dihedral.get())

        if self.inc_LE_TE_var.get() == True:
            r = 'LE/TE'
        elif self.inc_centroid.cget() == True:
            r = 'CENTROID'
        
        if self.LE_taper_var.get() == True:
            tt = 'LE'
        elif self.TE_taper_var.get() == True:
            tt = 'TE'
        elif self.trap_taper_var.get() == True:
            tt = 'TRAP'
        elif self.elliptical_var.get() == True:
            tt = 'E'

        self.resolution = 100
        self.cs = wing_creation(airfoil_settings=[M,P,XX], root_chord=rc, root_incidence=ri, num_af=an, taper_ratio=tr, taper_type=tt, wing_span=ws, fuse_width=fw, rotation_point=r, washout_angle=wo, sweep_angle=sw, dihedral_angle=dh, resolution=self.resolution, num_sides=2) 
        
        if an > 1:
            self.guidelines = guideline_creator(self.cs, self.resolution)
            surface_mesh_x = np.zeros((self.resolution*2, an*2))
            surface_mesh_y = np.zeros((self.resolution*2, an*2))
            surface_mesh_z = np.zeros((self.resolution*2, an*2))
        for i,a in enumerate(self.cs):
            if an > 1:
                surface = np.vstack((a[2], np.flipud(a[3])))
                surface_mesh_x[:,i] = surface[:,0]
                surface_mesh_y[:,i] = surface[:,2]
                surface_mesh_z[:,i] = surface[:,1]
            if a[0] == self.export_option_val.get():
                c_= 'red'
            else:
                c_ = 'black'
            if self.camber_bool.get() == True:
                self.ax.plot(a[1][:,0], a[1][:,2], a[1][:,1], color='green')
                self.ax.plot_wireframe(surface_mesh_x, surface_mesh_y, surface_mesh_z)
            if self.thick_bool.get() == True:
                self.ax.plot(a[4][:,0], a[4][:,2], a[4][:,1], color='blue')
            self.ax.plot(a[2][:,0], a[2][:,2], a[2][:,1], color=c_)
            self.ax.plot(a[3][:,0], a[3][:,2], a[3][:,1], color=c_)

        if self.guideline_plot_bool.get() == True:
            for g in self.guidelines:
                self.ax.plot(g[:,0], g[:,2], g[:,1], color='gray')
        self.ax.set_xticklabels([])     # create axes labels and get rid of tick mark values to clean up plot
        self.ax.set_yticklabels([])     #
        self.ax.set_zticklabels([])     #
        if an != 1:
            self.ax.set_zlim(-ws/2, ws/2) #
            self.ax.set_ylim(-ws/2,ws/2) 
            self.ax.set_xlim(-ws/4,3*ws/4)
        else:
            self.ax.set_zlim(-rc/2,rc/2)
        self.plot_origin_axis(rc)        #
        self.canvas.draw() 

if __name__ == '__main__':
    root = Tk()
    root.title("Daedalus")
    app = Daedalus(root)
    root.mainloop()