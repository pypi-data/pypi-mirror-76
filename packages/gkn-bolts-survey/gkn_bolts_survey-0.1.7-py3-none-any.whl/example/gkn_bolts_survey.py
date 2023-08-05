
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from numpy.random import uniform as rand


class SignalType():
    def __init__(self, label=None, torque=None, angle=None,
                 torque_filter=None, angle_filter=None,
                 approx_type=None, approx_coef=None):
        self.label = label
        self.torque = torque
        self.angle = angle
        self.torque_filter = torque_filter
        self.angle_filter = angle_filter
        self.approx_type = approx_type
        self.approx_coef = approx_coef

class TargetType():
    def __init__(self, threshold_torque, applied_angle, 
                 angle_tolerance, lower_torque, upper_torque):
        self.threshold_torque = threshold_torque
        self.applied_angle = applied_angle
        self.angle_tolerance = angle_tolerance
        self.lower_torque = lower_torque
        self.upper_torque = upper_torque


def read_signals(file_name):
    """
    This fuction read the torque and angle signals from
    different kind of sources

    Input:
        file_name: string with the file name

    Output:
        Signals: container with the signals:
            signal.label:   string
            signal.torque:  array
            signal.angle:   array
    """
    extension = file_name.split('.')[-1]
    if extension == 'xls':
        Signals = read_AtlasCopco(file_name)

    elif extension == 'xlsx':
        Signals = read_Excel(file_name)

    return Signals


def read_AtlasCopco(file_name):
    """
    This fuction read the torque and angle signals from
    the xls file created by the Smart Key Atlas Copco

    Input:
        file_name: string with the xls file name

    Output:
        Signals: container with the signals:
            signal.label:   string
            signal.torque:  array
            signal.angle:   array
    """
    with open(file_name,'r') as fid:
        mat_list = []
        xls = fid.readlines()
        hidden_char = xls[1][4]
        number_of_line = 0
        for line in xls:
            number_of_line+= 1
            new_line = line.replace(hidden_char,'')
            new_line = new_line.replace(',','.')
            new_line = new_line.replace('<td></td>','<td>-100</td>')
            new_line = new_line.replace('<tr><td>','')
            new_line = new_line.replace('</tr>','')
            new_line = new_line.replace('</td><td>',';')
            new_line = new_line.replace('</td>\n','')
            if number_of_line > 2 and number_of_line < len(xls):
                read_items = new_line.split(';')
                for i,item in enumerate(read_items):
                    read_items[i] = float(item)
                mat_list.append(read_items)
                
    # convert data into an array
    mat_signals = np.asarray(mat_list)
    mat_signals = mat_signals.T

    # store the signals in the container
    Signals = []
    for i in range(0,len(mat_signals),2):
        label = "screw %i"%(len(Signals)+1)
        angle = mat_signals[i][mat_signals[i]>-100]
        torque = mat_signals[i+1][mat_signals[i+1]>-100]
        Signals.append( SignalType(label,torque,angle) )

    return Signals


def read_Excel(file_name):
    """
    This fuction read the torque and angle signals from
    the xlsx file created with MS Excel

    Input:
        file_name: string with the xlsx file name

    Output:
        Signals: container with the signals:
            signal.label:   string
            signal.torque:  array
            signal.angle:   array
    """
    from pandas import read_excel
    excel_data_df = read_excel(file_name) #, sheet_name='Employees')

    # èarse the file
    ArraysContainer = []    # temp container
    for column_label in excel_data_df.columns.ravel():
        list_values = excel_data_df[column_label].tolist()      # read columns as list
        array_values = np.array(list_values)                    # list to array
        array_values = array_values[~np.isnan(array_values)]    # remove nan
        ArraysContainer.append( array_values )                  # store to the temp container
    # next column

    # store the signals in the container
    Signals = []
    for i in range(0,len(ArraysContainer),2):
        label = "screw %i"%(len(Signals)+1)
        angle = ArraysContainer[i]
        torque = ArraysContainer[i+1]
        Signals.append( SignalType(label,torque,angle) )

    return Signals


def clean_signal(signal, cut_angle=100.0, filter_angle=5.0, 
                  threshold_ratio=0.3, flag_plot=False):
    """
    This clean a signal from reloads and final unload;
    the filtered signal is also cut at predefined angle.
    The reloads are detected with the greatest gap in torque 
    (max Torque x threshold_ratio) within a moving windows 
    in angle (filter_angle).

    Input:
        signal: SignalType object:
            signal.label:   string
            signal.torque:  array
            signal.angle:   array
        cut_angle:        float (default 100)
        filter_angle:     float (default 5)
        threshold_ratio:  float (default 0.3)
        flag_plot:        boolean
    
    Output:
        within signal:
            signal.torque_filter:  array
            signal.angle_filter:   array
    """
    
    # index of the cut off angle 
    if signal.angle[-1] > cut_angle:
        jmax = np.where(signal.angle>cut_angle)[0][0]
    else:
        jmax = len(signal.angle)
    index_jump = int(jmax/10)

    # threeshold torque within the window
    threshold_torque = 0.3 * max(signal.torque[0:jmax])

    # moving windows in angle
    index = np.arange(len(signal.angle))
    for moving_angle in range(0,int(cut_angle),int(0.5*filter_angle)):
        if signal.angle[-1] > moving_angle:
            jin = np.where(signal.angle>moving_angle)[0][0]
        else: continue
        if signal.angle[-1] > moving_angle+filter_angle:
            jout = np.where(signal.angle>moving_angle+filter_angle)[0][0]
        else:
            jout = jmax
        delta_torque = max(signal.torque[jin:jout]) - min(signal.torque[jin:jout])
        if delta_torque > threshold_torque:  index[range(jin,jout)] = -100

    # deselect angles > cut off
    index[range(jmax,len(signal.angle))] = -100

    # store filter angles and torques
    signal.angle_filter = signal.angle[index>-1]
    signal.torque_filter = signal.torque[index>-1]
    
    # plot the filtered signal
    if flag_plot:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_xlabel('tightening angle in deg')
        ax.set_ylabel('tightening torque in Nm')
        ax.set_title(signal.label)
        ax.plot(signal.angle, signal.torque)
        ax.plot(signal.angle_filter, signal.torque_filter, "d")
        ax.grid(True)
        plt.show()

    return  # void


def sigmoid_approximation(signal, learing_rate=0.2, max_iter=100):
    """
    This calculate the approximation of the torque angle tightening 
    function with a sigmoid function:
        T_approx = a / (1+exp(-(b*angle+c))) 
    with a,b,c the output coefficients
    The approximation if applied on the already filtered signals.
    
    Input:
        signal: SignalType object:
            signal.torque_filter:  array
            signal.torque_filter:  array
        learing_rate:     scalar  (default 0.2)
        max_iter:         integer (default 100)
    
    Output:
        within signal:
            signal.approx_coef:    array with [a,b,c]
    """
    
    # parameters: first trial
    approx_coef = get_trial_parameters(signal)
    
    # main loop
    for iter in range(max_iter):

        # calculate the trial signal
        a,b,c = approx_coef
        sigm_function = get_sigmoid_function(signal.angle_filter, a, b, c)
        phi = sigm_function / a

        # derivatives
        df_da = (sigm_function - signal.torque_filter) * phi
        df_dc = (sigm_function - signal.torque_filter) * a
        df_dc*= phi * (1-phi)
        df_db = df_dc * signal.angle_filter
        
        df2_daa = np.power(phi, 2)
        df2_dab = phi * (1-phi)
        df2_dab*= (sigm_function - signal.torque_filter) + sigm_function
        df2_dab*= signal.angle_filter
        df2_dac = 1-phi
        df2_dac*= (sigm_function - signal.torque_filter)*phi + a*np.power(phi,2)
        df2_dcc = (sigm_function - signal.torque_filter)
        df2_dcc*= sigm_function * (1-phi) * (1-2*phi)
        df2_dcc+= np.power(sigm_function * (1-phi), 2)
        df2_dbc = df2_dcc * signal.angle_filter
        df2_dbb = df2_dbc * signal.angle_filter

        # build a solution sistem
        G_matrix = np.zeros((3,3))
        G_matrix[0,0] = df2_daa.sum()
        G_matrix[0,1] = df2_dab.sum()
        G_matrix[0,2] = df2_dac.sum()
        G_matrix[1,1] = df2_dbb.sum()
        G_matrix[1,2] = df2_dbc.sum()
        G_matrix[2,2] = df2_dcc.sum()
        G_matrix[1,0] = G_matrix[0,1]
        G_matrix[2,0] = G_matrix[0,2]
        G_matrix[2,1] = G_matrix[1,2]

        F_vector = np.zeros(3)
        F_vector[0] =-df_da.sum()
        F_vector[1] =-df_db.sum()
        F_vector[2] =-df_dc.sum()
        
        # update the parameters
        upd_param = np.linalg.solve(G_matrix,F_vector)
        approx_coef+= learing_rate * upd_param
        error = np.linalg.norm(upd_param)
        
        if error < 1.0e-3:
            # convergence found
            break
        
        # print(" - %3i  %10.3f"%(iter+1, error))
    # next iteration

    # store the results
    signal.approx_type = "sigmoid"
    signal.approx_coef = approx_coef
        
    return  # void


def get_sigmoid_function(x, a, b, c):
    """
    Calculate the sigmoid function out of parameters:
    Input:
        x: array of angles
        a,b,c: scalars of parameters
    Output:
        y: array of torque
    """
    y =-(b*x + c)
    y = np.exp(y) + 1
    y = a / y
    
    return y
        

def get_trial_parameters(signal):
    """
    This returns the best starting parameters for the Sigmoid 
    approximation function:
        a = max(torque)
        b,c = minor error with the curve passing through 
        the control point at Tcontr = Tmax/2

    Input:
        signal: SignalType object:
            signal.torque_filter:  array
            signal.torque_filter:  array
    
    Output:
        approx_coef:    array with [a0,b0,c0]
    """
    control_torque = 0.5 * np.max(signal.torque_filter)
    index = np.where(signal.torque_filter>control_torque)[0][0]
    control_angle = signal.angle_filter[index]

    # define the set of trials
    a_value  = np.max(signal.torque_filter)  # fix value
    b_values = np.arange(17)*0.005 + 0.02    # range of trials
    c_values =-np.log(a_value/control_torque-1) - control_angle*b_values

    # find errors
    errors = np.zeros(len(b_values))
    for i in range(len(b_values)):
        a,b,c = a_value, b_values[i], c_values[i]
        sigm_function = get_sigmoid_function(signal.angle_filter, a, b, c)
        errors[i] = np.sum(np.power(sigm_function - signal.torque_filter, 2))
    
    # trial parameters
    a_trial = a_value
    b_trial = b_values[np.argmin(errors)]
    c_trial = c_values[np.argmin(errors)]
    approx_coef = np.array([a_trial, b_trial, c_trial])

    return approx_coef


def average_curve(Signals, threshold_torque):
    """
    """
    a_ave, b_ave, c_ave = 0.0, 0.0, 0.0
    torques = np.zeros(len(Signals))
    angles = np.zeros(len(Signals))
    for i,signal in enumerate(Signals):
        # shift curve to threeshold torque
        a,b,c = signal.approx_coef
        c_star =-np.log(a/threshold_torque - 1)

        # update avereges
        a_ave+= a / len(Signals)
        b_ave+= b / len(Signals)
        c_ave+= c_star / len(Signals)

        # yielding point
        torques[i] = a * 0.85355339
        angles[i] =-(np.log(a/torques[i] - 1) + c_star) / b
    # next signal

    average_coef = np.array([a_ave, b_ave, c_ave])

    # yielding point with statistic
    torque_mean = a_ave * 0.85355339
    torque_std = np.std(torques)
    angle_mean =-(np.log(a_ave/torque_mean - 1) + c_ave) / b_ave
    angle_std = np.std(angles)

    yield_point = np.array([torque_mean, torque_std, angle_mean, angle_std])

    return average_coef, yield_point


def plot_raw_signals(Signals, title=None, flag_show=False):
    """
    This function plot all the signals into a unique graph

    Inputs:
        Signals: container with the signals:
            signal.label:   string
            signal.torque:  array
            signal.angle:   array
        title:      string
        flag_show:  boolean

    Outputs:  none
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlabel('tightening angle in deg')
    ax.set_ylabel('tightening torque in Nm')
    if title is not None:
        ax.set_title(title)
    for signal in Signals:
        ax.plot(signal.angle, signal.torque, label=signal.label)
    ax.grid(True)
    ax.legend(loc='lower right')
    
    # save the graph
    if title is not None:   plt_file_name = title + '_raw.png'
    else:                   plt_file_name = 'screw_survey_raw.png'
    plt.savefig(plt_file_name)

    # show the graph
    if flag_show:
        plt.show()
    
    return  # void


def plot_survey(Signals, threshold_torque, target=None, 
                cut_angle=100.0, title=None, flag_show=False):
    """
    This plot the complete set of signals aligned at the threshold 
    torque with the average approxiamting curve and the yield point
    
    Input:
        Signals: container with the signals:
            signal.label:   string
            signal.torque:  array
            signal.angle:   array
        threshold_torque:   scalar
        cut_angle:          scalar  (default 100 deg)
        title:              string
        flag_show:          boolean

    Output:     none
    """
    # get the average curve
    average_coef, yield_point = average_curve(Signals, threshold_torque)

    # start figure
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlabel('tightening angle in deg')
    ax.set_ylabel('tightening torque in Nm')
    if title is not None:
        ax.set_title(title)
    
    # plot all raw signals shifted to the threshold torque
    for i,signal in enumerate(Signals):
        if i == 0: label='%ix measures'%(len(Signals))
        else: label=None
        a,b,c = signal.approx_coef
        c_star =-np.log(a/threshold_torque - 1)
        alpha_0 = (c_star-c)/b
        signal_angle_shift = signal.angle - alpha_0
        ax.plot(signal_angle_shift, signal.torque, c='b', lw=0.9,  
                alpha=rand(0.2,0.5), label=label)
    
    # plot the average curve
    x_low =-20.0    # deg
    ave_angle = np.linspace(x_low, cut_angle, 200)
    a_ave, b_ave, c_ave = average_coef
    ave_torque = get_sigmoid_function(ave_angle, a_ave, b_ave, c_ave)
    ax.plot(ave_angle, ave_torque, c='r', lw=3, label='average')
    
    # plot yield point
    Ty, Tstd, Ay, Astd = yield_point
    ax.plot(Ay, Ty, 'ro', ms=11, alpha=0.7, mfc='orange', label='yield')
    
    # plot standard deviations
    for lbd in range(1,4):
        if lbd == 2: label='1,2,3x st.dev'
        else: label=None
        rect = patches.Rectangle((Ay-lbd*Astd,Ty-lbd*Tstd),2*lbd*Astd,2*lbd*Tstd,
               lw=2.0,edgecolor='k',alpha=0.8-lbd*0.2,facecolor='none',
               label=label)
        ax.add_patch(rect)

    # plot target
    if target is not None:
        x0 = target.applied_angle - target.angle_tolerance
        y0 = target.lower_torque
        dx = 2*target.angle_tolerance
        dy = target.upper_torque - target.lower_torque
        rect = patches.Rectangle((x0,y0),dx,dy, ls='--',lw=2.0,edgecolor='g',
                    alpha=1.0,facecolor='none',label='target')
        ax.add_patch(rect)
        ax.arrow(0,0,0,threshold_torque*4/5,  lw=3, alpha=0.5, head_width=2, head_length=threshold_torque/5)
        ax.arrow(0,threshold_torque,target.applied_angle*0.9,0,  lw=3, alpha=0.5, head_width=threshold_torque/10, head_length=target.applied_angle/10)
        ax.plot([target.applied_angle,target.applied_angle], [0.,2*Ty], '--k', lw=2)

        # add target texts
        props = dict(boxstyle='round', facecolor='white', alpha=0.5)
        x, y = 2, 0.45*threshold_torque
        textstr = '%i Nm'%threshold_torque          # threshold torque
        ax.text(x, y, textstr, bbox=props)

        x, y = 0.4*target.applied_angle, 1.15*threshold_torque
        textstr = '%i deg'%target.applied_angle     # applied angle
        ax.text(x, y, textstr, bbox=props)

        x, y = target.applied_angle+target.angle_tolerance+2, 0.975*target.lower_torque
        textstr = '%i Nm'%target.lower_torque      # lower torque
        ax.text(x, y, textstr, bbox=props)

        x, y = target.applied_angle+target.angle_tolerance+2, 0.975*target.upper_torque
        textstr = '%i Nm'%target.upper_torque     # upper torque
        ax.text(x, y, textstr, bbox=props)


    # add yield texts
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    textstr = '\n'.join((
    r'$T_{th} = %i Nm$'%threshold_torque,
    r'$T_y = %i Nm$'%Ty,
    r'$\alpha_y = %i deg$'%Ay))
    ax.text(0.03, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

    # plot further settings
    x_low =-20.0    # deg
    plt.xlim(x_low, cut_angle)
    plt.ylim(0.0, 1.5*Ty)
    ax.grid(True)
    ax.legend(loc='lower right')

    # save the graph
    if title is not None:   plt_file_name = title + '.png'
    else:                   plt_file_name = 'screw_survey.png'
    plt.savefig(plt_file_name)

    # show the graph
    if flag_show:
        plt.show()
    
    return


def plot_failure(Signals, threshold_torque, target=None, 
                 title=None, flag_show=False):
    """
    This plot the complete set of signals aligned at the threshold 
    torque with the average approxiamting curve and the yield point
    
    Input:
        Signals: container with the signals:
            signal.label:           string
            signal.torque_filter:   array
            signal.angle_filter:    array
        threshold_torque:   scalar
        target:             TargetType
        title:              string
        flag_show:          boolean

    Output:     none
    """
    
    # start figure
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlabel('tightening angle in deg')
    ax.set_ylabel('tightening torque in Nm')
    if title is not None:
        ax.set_title(title)

    # plot all raw signals shifted to the threshold torque
    for i,signal in enumerate(Signals):
        if i == 0: label='%ix measures'%(len(Signals))
        else: label=None
        # shift to threshold_torque 
        index = np.where(signal.torque_filter>threshold_torque)[0][0]
        alpha_0 = signal.angle_filter[index]
        ax.plot(signal.angle_filter-alpha_0, signal.torque_filter, c='b', lw=1.0,  
                alpha=rand(0.5,0.8), label=label)
        # plot failure mark
        if i == 0: label='failure'
        else: label=None
        ax.plot(signal.angle_filter[-1]-alpha_0, signal.torque_filter[-1], 
                'kX', ms=11, alpha=0.6, mfc='red', label=label)
    
    
    # plot threshold torque
    ax.plot(0, threshold_torque, 'bo', ms=10, alpha=0.6, mfc='green', label='$T_{th} = %i Nm$'%threshold_torque)
    
    # plot target
    if target is not None:
        x0 = target.applied_angle - target.angle_tolerance
        y0 = target.lower_torque
        dx = 2*target.angle_tolerance
        dy = target.upper_torque - target.lower_torque
        rect = patches.Rectangle((x0,y0),dx,dy, ls='--',lw=2.0,edgecolor='g',
                    alpha=1.0,facecolor='none',label='target')
        ax.add_patch(rect)


    # plot further settings
    ax.grid(True)
    ax.legend(loc='lower right')

    # save the graph
    if title is not None:   plt_file_name = title + '.png'
    else:                   plt_file_name = 'screw_survey_failure.png'
    plt.savefig(plt_file_name)

    # show the graph
    if flag_show:
        plt.show()
    
    return  # void


