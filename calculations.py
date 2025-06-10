import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def indidence_rotation(i, coord_of_rotation, coords):
    x = coord_of_rotation[0]
    y = coord_of_rotation[1]
    z = coord_of_rotation[2]

    i = np.deg2rad(i)

    # B = np.array([[np.cos(theta), 0, np.sin(theta)], [0,1,0], [-np.sin(theta), 0, np.cos(theta)]])
    A = np.array([[np.cos(i), -np.sin(i), 0], [np.sin(i), np.cos(i), 0], [0,0,1]])
    B = np.identity(3)
    C = np.identity(3)

    new_coords = A @ B @ C @ coords.transpose()
    new_coords = new_coords.transpose()
    return new_coords


def washout(max_theta, coords, b, f):
    new_coords = np.zeros(coords.shape)
    zero_wo = (b+f)/2
    theta = lambda s: (4*max_theta)/(b-f)*(abs(s)-f/2)-max_theta
    span_loc = coords[0][2]
    theta_ = np.deg2rad(theta(span_loc))
    A = np.array([[np.cos(theta_), -np.sin(theta_), 0], [np.sin(theta_), np.cos(theta_), 0], [0,0,1]])
    B = np.identity(3)
    C = np.identity(3)
    new_coords = A @ B @ C @ coords.transpose()
    new_coords = new_coords.transpose()
    return new_coords

def sweep(max_lambda, coords, b, f):
    new_coords = np.zeros(coords.shape)
    span_loc = coords[0][2]
    if span_loc <= -f/2:
        max_lambda = -np.deg2rad(max_lambda)
    elif span_loc >= f/2:
        max_lambda = np.deg2rad(max_lambda)
    A = np.array([[1, 0, np.tan(max_lambda)], [0,1,0], [0,0,1]])
    B = np.identity(3)
    C = np.identity(3)
    
    new_coords = A @ B @ C @ coords.transpose()
    new_coords = new_coords.transpose()
    return new_coords

def dihedral(max_gamma, coords, b, f):
    new_coords = np.zeros(coords.shape)
    span_loc = coords[0][2]
    if span_loc <= -f/2:
        max_gamma = np.deg2rad(max_gamma)
    elif span_loc >= f/2:
        max_gamma = -np.deg2rad(max_gamma)
    else:
        max_gamma = 0
    
    A = np.identity(3)
    B = np.identity(3)
    C = np.array([[1,0,0],[0,np.cos(max_gamma),-np.sin(max_gamma)],[0,np.sin(max_gamma),np.cos(max_gamma)]])
    new_coords = A @ B @ C @ coords.transpose()
    new_coords = new_coords.transpose()
    return new_coords


def airfoil_creation(M, P, XX, chord, span_loc, LE_loc, incidence, rotation_point, washout_angle, sweep_angle, wingspan, fusewidth, dihedral_angle, resolution):
    chord_ = np.linspace(0,chord,resolution)
    M /= 100
    P /= 10
    XX /= 100
    camber_ = []
    thickness_ = []
    theta_ = []
    u_, l_ = [], []
    if M != 0:
        for x in chord_:
            if x < P*chord:
                at_x = M*x/P**2 * (2*P-x/chord)
                dy_dx = 2*M/P**2*(P-x/chord)
                theta = np.arctan(dy_dx)
            else:
                at_x = M*(chord-x)/((1-P)**2) * (1 + x/chord - 2*P)
                dy_dx = 2*M/(1-P)**2*(P-x/chord)
                theta = np.arctan(dy_dx)
            theta_.append(theta)
            thickness_.append(XX*chord/0.2 * (0.2969*np.sqrt(x/chord) - 0.1260*x/chord - 0.3516*(x/chord)**2 + 0.2843*(x/chord)**3 - 0.1036*(x/chord)**4))
            camber_.append(at_x)

        for i,x in enumerate(chord_):
            u_.append([x-thickness_[i]*np.sin(theta_[i]), camber_[i]+thickness_[i]*np.cos(theta_[i])])
            l_.append([x+thickness_[i]*np.sin(theta_[i]), camber_[i]-thickness_[i]*np.cos(theta_[i])])

        camber_coords = np.zeros((len(chord_), 3))
        u_coords = np.zeros((len(chord_), 3))
        l_coords = np.zeros((len(chord_), 3))
        thickness_coords = np.zeros((len(chord_), 3))

        # gets initial airfoil coords before any thing else
        for i in range(len(chord_)):
            camber_coords[i,:] = [chord_[i],camber_[i],span_loc]
            u_coords[i,:] = [u_[i][0], u_[i][1],span_loc]
            l_coords[i,:] = [l_[i][0], l_[i][1],span_loc]
            thickness_coords[i,:] = [chord_[i], thickness_[i],span_loc]
    else:
        for x in chord_:
            t = XX*chord/0.2 * (0.2969*np.sqrt(x/chord) - 0.1260*x/chord - 0.3516*(x/chord)**2 + 0.2843*(x/chord)**3 - 0.1036*(x/chord)**4)
            thickness_.append(t)
            u_.append(t)
            l_.append(-t)
        camber_coords = np.zeros((len(chord_), 3))
        u_coords = np.zeros((len(chord_), 3))
        l_coords = np.zeros((len(chord_), 3))
        thickness_coords = np.zeros((len(chord_), 3))
        # gets initial airfoil coords before any thing else
        for i in range(len(chord_)):
            camber_coords[i,:] = [chord_[i],0,span_loc]
            u_coords[i,:] = [chord_[i], u_[i],span_loc]
            l_coords[i,:] = [chord_[i], l_[i],span_loc]
            thickness_coords[i,:] = [chord_[i], thickness_[i],span_loc]

    if rotation_point == 'LE/TE':
        rotation_point = (0,0,0)
    elif rotation_point == 'CENTROID':
        pass
    camber_coords = indidence_rotation(-incidence, rotation_point, camber_coords)
    u_coords = indidence_rotation(-incidence, rotation_point, u_coords)
    l_coords = indidence_rotation(-incidence, rotation_point, l_coords)
    thickness_coords = indidence_rotation(-incidence, rotation_point, thickness_coords)
    
    camber_coords = washout(washout_angle, camber_coords, wingspan, fusewidth)
    u_coords = washout(washout_angle, u_coords, wingspan, fusewidth)
    l_coords = washout(washout_angle, l_coords, wingspan, fusewidth)
    thickness_coords = washout(washout_angle, thickness_coords, wingspan, fusewidth)
    
    camber_coords = sweep(sweep_angle, camber_coords, wingspan, fusewidth)
    u_coords = sweep(sweep_angle, u_coords, wingspan, fusewidth)
    l_coords = sweep(sweep_angle, l_coords, wingspan, fusewidth)
    thickness_coords = sweep(sweep_angle, thickness_coords, wingspan, fusewidth)
    
    camber_coords = dihedral(dihedral_angle, camber_coords, wingspan, fusewidth)
    u_coords = dihedral(dihedral_angle, u_coords, wingspan, fusewidth)
    l_coords = dihedral(dihedral_angle, l_coords, wingspan, fusewidth)
    thickness_coords = dihedral(dihedral_angle, thickness_coords, wingspan, fusewidth)

    camber_coords[:,0] += LE_loc
    u_coords[:,0] += LE_loc
    l_coords[:,0] += LE_loc
    thickness_coords[:,0] += LE_loc
    return camber_coords, u_coords, l_coords, thickness_coords
# arguements: airfoil_settings, root_chord, root_incidence, num_af, taper_ratio, taper_type, wing_span, fuse_width
def wing_creation(airfoil_settings, root_chord, root_incidence, num_af, taper_ratio, taper_type, wing_span, fuse_width, rotation_point, washout_angle, sweep_angle, dihedral_angle, resolution, num_sides):
    M = airfoil_settings[0]
    P = airfoil_settings[1]
    XX = airfoil_settings[2]
    # get location of airfoil placement
    if taper_type != 'E':
        if num_af == 1:
            airfoil_loc = [0]
        else:
            if num_sides == 2:
                airfoil_loc = []
                airfoil_loc.extend(np.linspace(-wing_span/2,-fuse_width/2,num_af))
                airfoil_loc.extend(np.linspace(fuse_width/2,wing_span/2, num_af))
            else:
                airfoil_loc = []
                airfoil_loc.extend(np.linspace(fuse_width/2,wing_span/2, num_af))            
        tip_chord = root_chord*taper_ratio
        chord_len_func = lambda span_loc: (tip_chord-root_chord)/(wing_span/2-fuse_width/2)*(abs(span_loc) - wing_span/2)+tip_chord
        
        # get chord lengths at this location
        chord_len_list, chord_diff_list = [], []
        for c in airfoil_loc:
            chord_len_list.append(chord_len_func(c))
            chord_diff_list.append(root_chord-chord_len_func(c))
        # dealing with taper placement
        cs = []
        if taper_type == 'LE':
            for i,c in enumerate(chord_len_list):
                airfoil_entry = [f'Airfoil {i}']
                airfoil_data = airfoil_creation(M,P,XX,c,airfoil_loc[i], chord_diff_list[i], root_incidence, rotation_point, washout_angle, sweep_angle, wing_span, fuse_width, dihedral_angle,resolution)
                airfoil_entry.extend(airfoil_data)
                cs.append(airfoil_entry)
        elif taper_type == 'TE':
            for i,c in enumerate(chord_len_list):
                airfoil_entry = [f'Airfoil {i}']
                airfoil_data = airfoil_creation(M,P,XX,c,airfoil_loc[i], 0, root_incidence, rotation_point, washout_angle, sweep_angle, wing_span, fuse_width, dihedral_angle,resolution)
                airfoil_entry.extend(airfoil_data)
                cs.append(airfoil_entry)
        elif taper_type == 'TRAP':
            for i,c in enumerate(chord_len_list):
                airfoil_entry = [f'Airfoil {i}']
                airfoil_data = airfoil_creation(M,P,XX,c,airfoil_loc[i], chord_diff_list[i]/2, root_incidence, rotation_point, washout_angle, sweep_angle, wing_span, fuse_width, dihedral_angle,resolution)
                airfoil_entry.extend(airfoil_data)
                cs.append(airfoil_entry)
        elif taper_type == None:
            for i,c in enumerate(chord_len_list):
                airfoil_entry = [f'Airfoil {i}']
                airfoil_data = airfoil_creation(M,P,XX,c,airfoil_loc[i], chord_diff_list[i]/2, root_incidence, rotation_point, washout_angle, sweep_angle, wing_span, fuse_width, dihedral_angle,resolution)
                airfoil_entry.extend(airfoil_data)
                cs.append(airfoil_entry)
    else:
        if num_sides == 2:
            airfoil_loc = np.linspace(-wing_span/2, wing_span/2, num_af*2)
        else:
            airfoil_loc = np.linspace(0, wing_span/2, num_af*2)
        chord_len_func = lambda span_loc, b1, b2, a: abs(np.sqrt(b1**2*(1-span_loc**2/a**2)) + np.sqrt(b2**2*(1-span_loc**2/a**2))) 
        ellip_LE_loc_fun = lambda span_loc, b1, a: np.sqrt(b1**2*(1-span_loc**2/a**2))
        b1 = root_chord/3
        b2 = 2*root_chord/3
        a = wing_span/2
        chord_len_list = []
        LE_loc_list = []
        for i,loc in enumerate(airfoil_loc):
            chord_len_list.append(chord_len_func(loc, b1, b2, a))
            LE_loc_list.append(-ellip_LE_loc_fun(loc, b1, a))
        cs = []
        for i,c in enumerate(chord_len_list):
            airfoil_entry = [f'Airfoil {i}']
            airfoil_data = airfoil_creation(M,P,XX,c,airfoil_loc[i], LE_loc_list[i], root_incidence, rotation_point, washout_angle, sweep_angle, wing_span, fuse_width, dihedral_angle,resolution)
            airfoil_entry.extend(airfoil_data)
            cs.append(airfoil_entry)
    return cs
# funciton call for testing only
# wing_creation([2,2,18],14.4,0,1,1,'TE',60,0,(0,0,0),20,15, 15, 20)