## raster_plotter.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## Function to plot the raster data in *.flt format generated by the
## chi analysis code. read_flt() returns flt data as numpy arrays and is
## called by the plot_ChiMValues_hillshade() to quickly visualise the
## m values without launching arcmap. Vectorize() plots the m values
## as individual points. Next step may be to thin the points?
##
## flt reading Built around code from http://pydoc.net/Python/PyTOPKAPI/0.2.0/pytopkapi.arcfltgrid/
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## SWDG 19/06/2013
## modified SMM 09/08/2013
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def round_to_n(x, n):
    if n < 1:
        raise ValueError("number of significant digits must be >= 1")
    # Use %e format to get the n most significant digits, as a string.
    format = "%." + str(n-1) + "e"
    as_string = format % x
    return float(as_string)


def read_headers(input_file):

    with open(input_file+'.hdr','r') as f:
        return [float(h) if not h.isalpha() else h for h in [l.split()[1] for l in f.readlines()]]  #isdigit() does not catch floats

def read_bin(filename):
    import sys
    import numpy as np

    with open(filename + '.flt', "rb") as f:
        raster_data = np.fromstring(f.read(), 'f')

    if sys.byteorder == 'big':
        raster_data = raster_data.byteswap()  #ensures data is little endian

    return raster_data

def read_flt(input_file):

    if input_file.endswith('.flt') or input_file.endswith('.hdr'):
        input_file = input_file[:-4]
    else:
        # # print 'Incorrect filename'
        return 0,0 #exits module gracefully

    headers = read_headers(input_file)

    #read the data as a 1D array and reshape it to the dimensions in the header
    raster_array = read_bin(input_file).reshape(headers[1], headers[0])
    raster_array = raster_array.reshape(headers[1], headers[0]) #rows, columns

    return raster_array, headers

def read_ascii_raster(ascii_raster_file):
    import numpy as np

    with open(ascii_raster_file) as f:
        header_data = [float(f.next().split()[1]) for x in xrange(6)] #read the first 6 lines

    raster_data = np.genfromtxt(ascii_raster_file, delimiter=' ', skip_header=6)
    raster_data = raster_data.reshape(header_data[1], header_data[0]) #rows, columns

    return raster_data, header_data

def format_ticks_for_UTM_imshow(hillshade_header,x_max,x_min,y_max,y_min,n_target_tics):
    import numpy as np

    xmax_UTM = hillshade_header[2]+x_max*hillshade_header[4]
    xmin_UTM = hillshade_header[2]+x_min*hillshade_header[4]

    # need to be careful with the ymax_UTM since the rows go from the top
    # but the header index is to bottom corner

    # print "yll: "+str(hillshade_header[3])+" and nrows: " +str(hillshade_header[1]) + " dx: "+str(hillshade_header[4])   

    ymax_from_bottom = hillshade_header[1]-y_min
    ymin_from_bottom = hillshade_header[1]-y_max
    ymax_UTM = hillshade_header[3]+ymax_from_bottom*hillshade_header[4]
    ymin_UTM = hillshade_header[3]+ymin_from_bottom*hillshade_header[4]

    # print "now UTM, xmax: " +str(xmax_UTM)+" x_min: " +str(xmin_UTM)+" y_maxb: " +str(ymax_UTM)+" y_minb: " +str(ymin_UTM)

    dy_fig = ymax_UTM-ymin_UTM
    dx_fig = xmax_UTM-xmin_UTM

    dx_spacing = dx_fig/n_target_tics
    dy_spacing = dy_fig/n_target_tics

    if (dx_spacing>dy_spacing):
        dy_spacing = dx_spacing

    str_dy = str(dy_spacing)
    str_dy = str_dy.split('.')[0]
    n_digits = str_dy.__len__()
    nd = int(n_digits)

    first_digit = float(str_dy[0])

    # print "str_dy: " +str_dy+ " n_digits: " +str(nd)+" first_digit: " + str(first_digit)

    dy_spacing_rounded = first_digit*pow(10,(nd-1))
    # print "n_digits: "+str(n_digits)+" dy_spacing: " +str(dy_spacing) + " and rounded: "+str(dy_spacing_rounded)

    str_xmin = str(xmin_UTM)
    str_ymin = str(ymin_UTM)
    str_xmin = str_xmin.split('.')[0]
    str_ymin = str_ymin.split('.')[0]
    xmin_UTM = float(str_xmin)
    ymin_UTM = float(str_ymin)

    n_digx = str_xmin.__len__()
    n_digy = str_ymin.__len__()

    front_x = str_xmin[:(n_digx-nd+1)]
    front_y = str_ymin[:(n_digy-nd+1)]

    # print "xmin: " + str_xmin + " ymin: " + str_ymin + " n_digx: " + str(n_digx)+ " n_digy: " + str(n_digy)
    # print "frontx: " +front_x+" and fronty: "+ front_y

    round_xmin = float(front_x)*pow(10,nd-1)
    round_ymin = float(front_y)*pow(10,nd-1)

    # print "x_min: " +str(xmin_UTM)+ " round xmin: " +str(round_xmin)+ " y_min: " +str(ymin_UTM)+" round y_min: " + str(round_ymin)

    # now we need to figure out where the xllocs and ylocs are
    xUTMlocs = np.zeros(2*n_target_tics)
    yUTMlocs = np.zeros(2*n_target_tics)
    xlocs = np.zeros(2*n_target_tics)
    ylocs = np.zeros(2*n_target_tics)

    new_x_labels = []
    new_y_labels = []

    for i in range(0,2*n_target_tics):
        xUTMlocs[i] = round_xmin+(i)*dy_spacing_rounded
        yUTMlocs[i] = round_ymin+(i)*dy_spacing_rounded

        xlocs[i] = (xUTMlocs[i]-hillshade_header[2])/hillshade_header[4]

        # need to account for the rows starting at the upper boundary
        ylocs[i] = hillshade_header[1]-((yUTMlocs[i]-hillshade_header[3])/hillshade_header[4])

        new_x_labels.append( str(xUTMlocs[i]).split(".")[0] )
        new_y_labels.append( str(yUTMlocs[i]).split(".")[0] )

    return xlocs,ylocs,new_x_labels,new_y_labels


def coloured_chans_like_graphs(hillshade_file):
    """
    Plots outlines of channels taken from the *.tree file over a hillshade
    giving each channel a unique colour which corresponds to the colours used
    in the Chi plotting routines in chi_visualisation.py.

    """

    label_size = 20
    #title_size = 30
    axis_size = 28



    import matplotlib.pyplot as pp
    import numpy as np
    import matplotlib.colors as colors
    import matplotlib.cm as cmx
    from matplotlib import rcParams
    import matplotlib.lines as mpllines

    #get data
    hillshade, hillshade_header = read_flt(hillshade_file)

    #ignore nodata values
    hillshade = np.ma.masked_where(hillshade == -9999, hillshade)

    #fonts
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = label_size

    #get bounding box & pad to 10% of the dimension
    x_max = hillshade_header[0]
    x_min = 0
    y_max = hillshade_header[1]
    y_min = 0

    fig = pp.figure(1, facecolor='white',figsize=(10,7.5))
    ax = fig.add_subplot(1,1,1)
    ax.imshow(hillshade, vmin=0, vmax=255, cmap=cmx.gray)

    # now get the tick marks
    n_target_tics = 5
    xlocs,ylocs,new_x_labels,new_y_labels = format_ticks_for_UTM_imshow(hillshade_header,x_max,x_min,y_max,y_min,n_target_tics)
    pp.xticks(xlocs, new_x_labels, rotation=60)  #[1:-1] skips ticks where we have no data
    pp.yticks(ylocs, new_y_labels)

    pp.xlim(x_min,x_max)
    pp.ylim(y_max,y_min)

    pp.xlabel('Easting (m)',fontsize = axis_size)
    pp.ylabel('Northing (m)', fontsize = axis_size)

    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5)
    ax.tick_params(axis='both', width=2.5)



    pp.show()

#coloured_chans_like_graphs('NC_HS.flt')
