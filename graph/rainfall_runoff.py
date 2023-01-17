class graph_class:

    '''from graph import rainfall_runoff

* sample code

g_class = rainfall_runoff.graph_class()

x = df['time']
y = df['q_rational_D_longer']
y2 = np.arange(0, 20, 1)

g_class.set_data(x=x, y=y, y2=y2)

g_class.set_options()

g_class.make_graph()'''

    def __init__(self):

        pass
    
    def set_data(self, x, y, y2):
        self.x = x
        self.y = y
        self.y2 = y2

    def set_options(self,
                    figsize=(14,8),
                    weight = 1.5,
                    x_min = 0, 
                    x_max = 50,
                    y_min = 0, 
                    y_max = 50,
                    y2_min = 0,
                    y2_max = 60,
                    grid_num_x = 6,
                    grid_num_y = 5,
                    bar_width = 1.0,
                    ):

        self.figsize = figsize
        self.weight = weight 
        self.x_min = x_min 
        self.x_max = x_max 
        self.y_min = y_min  
        self.y_max = y_max 
        self.y2_min = y2_min 
        self.y2_max = y2_max 
        self.grid_num_x = grid_num_x 
        self.grid_num_y = grid_num_y 
        self.bar_width = bar_width 

    def make_graph(self):
        
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import numpy as np 

        x = self.x
        y = self.y
        y2 = self.y2

        figsize = self.figsize
        weight = self.weight 
        x_min = self.x_min 
        x_max = self.x_max 
        y_min = self.y_min  
        y_max = self.y_max 
        y2_min = self.y2_min 
        y2_max = self.y2_max 
        grid_num_x = self.grid_num_x 
        grid_num_y = self.grid_num_y 
        bar_width = self.bar_width 

        xlabel = 'Time (h)'
        ylabel = 'Discharge (m$^3$/s)'
        y2label = 'Rainfall (mm/h)'

        color1 = 'black'
        linewidth1 = 3
        linestyle1 = '--'
        label1 = 'MRM'

        color2 = 'black'
        linewidth2 = 3
        linestyle2 = '--'
        label2 = 'MRM'

        # format 변환 양식
        def format_change(x, x_max):
            if x_max < 5:
                format_box = mpl.ticker.StrMethodFormatter('{x:,.1f}')
            else:
                format_box = mpl.ticker.StrMethodFormatter('{x:,.0f}')

            return format_box(x)
        
        mpl.rc("font", family="Arial", weight='bold') # font setting
        
        fig = plt.figure(figsize=figsize) #, dpi=300) # figure basic setting

        ax1 = fig.subplots() 
        ax2 = ax1.twinx()

        # y2 graph
        ax2.bar(y2, 10, width = bar_width ,  color = 'gray')
        step=(y2_max-y2_min)/grid_num_y
        y2_ticks_list = np.arange(y2_min, y2_max/2+1, step=(y2_max-y2_min)/grid_num_y)
        #ax2.set_yticks(y2_ticks_list)
        #ax2.set_yticklabels([ format_change(y, y2_max) for y in y2_ticks_list] ) # ytick setting 
        ax2.set_yticks([])
        ax2.tick_params(axis='both', direction='out', length = 3, pad = 6, labelsize = 15*weight) # tick_params setting
        ax2.set_ylim(y2_min, y2_max)
        ax2.invert_yaxis()
        ax2.set_ylabel(y2label, family="Arial",weight='bold', labelpad=50, size = 25*weight, rotation = 270) # ylabel setting

        ax1.grid(alpha=0.4, linestyle='--', axis = 'y') # grid setting

        x_min, x_max = 0, x_max
        y_min, y_max = 0, y_max
        grid_num_x = grid_num_x # grid nums in x-axis
        grid_num_y = grid_num_y # grid nums in y-axis

        ax1.set_ylim(y_min,y_max) # y-limit setting
        ax1.set_xlim(x_min,x_max) # x-limit setting

        ax1.tick_params(axis='both', direction='out', length = 3, pad = 6, labelsize = 25) # tick_params setting
        x_ticks_list = np.arange(x_min, x_max+(x_max-x_min)/grid_num_x, step=(x_max-x_min)/grid_num_x)
        #ax1.set_xticks(x_ticks_list)
        #ax1.set_xticklabels([format_change(x, x_max) for x in x_ticks_list] ) # xtick setting
        ax1.set_xticks([])

        y_ticks_list = np.arange(y_min, y_max+(y_max-y_min)/grid_num_y, step=(y_max-y_min)/grid_num_y)
        #ax1.set_yticks(y_ticks_list) # ytick setting 
        #ax1.set_yticklabels([ format_change(y, y_max) for y in y_ticks_list])
        ax1.set_yticks([]) # ytick setting 
        ax1.set_xlabel(xlabel, family="Arial",weight='bold', labelpad=20, size = 35) # xlabel setting
        ax1.set_ylabel(ylabel, family="Arial",weight='bold', labelpad=20, size = 35) # ylabel setting

        # 0.01h 단위이기 때문에..
        ax1.plot(x, y, color = 'black'
                ,linewidth = linewidth1, linestyle= linestyle1, label = label1)

        # ax1.plot(x, y2, color = 'black'
        #         ,linewidth = linewidth2, linestyle= linestyle2, label = label2)

        ax1.legend(ncol =1, columnspacing = 0.5, edgecolor = '0.5', fontsize=15*weight, markerscale=1)

        mpl._mathtext.SHRINK_FACTOR = 0.5

        plt.show()

    def save_graph(self, file_name = 'test.png', dpi=300):

        plt.savefig(file_name, dpi=dpi, bbox_inches='tight')

