class graph_class:

    '''from graph import rainfall_runoff

* sample code

c = graph_class()
c.set_data(x = x, y = result_K_10['Qp'])
c.set_options()
c.make_graph(xlabel='ss', ylabel='ss')'''

    def __init__(self):

        pass
    
    def set_data(self, x, y):
        self.x = x
        self.y = y
        
        self.x_min = min(x)
        self.x_max = max(x)
        self.y_min = min(x)
        self.y_max = max(x)

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

    def make_graph(self, xlabel, ylabel,
                    color = 'black',
                    size = 5,
                    edge_width = 1,
                    linewidth = 1,
                    linestyle = '--',
                    label = 'Label',
                    marker = 'o'):
        
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        import numpy as np 

        x = self.x
        y = self.y
        
        figsize = self.figsize
        weight = self.weight 
        x_min = self.x_min 
        x_max = self.x_max 
        y_min = self.y_min  
        y_max = self.y_max 
        
        grid_num_x = self.grid_num_x 
        grid_num_y = self.grid_num_y 
        
        # format 변환 양식
        def format_change(x, x_max):
            if x_max < 5:
                format_box = mpl.ticker.StrMethodFormatter('{x:,.1f}')
            else:
                format_box = mpl.ticker.StrMethodFormatter('{x:,.0f}')

            return format_box(x)
        
        mpl.rc("font", family="Arial", weight='bold') # font setting
        
        fig = plt.figure(figsize=figsize) #, dpi=300) # figure basic setting

        mpl._mathtext.SHRINK_FACTOR = 0.5
        
        # 축 레이블 설정
        plt.xlabel(xlabel, family="Arial",weight='bold', labelpad=20, size = 30)
        plt.ylabel(ylabel, family="Arial",weight='bold', labelpad=20, size = 30)

        # of m$^3$/s
        # tiok 설정
        xticks_list = np.arange(x_min, x_max+1, step=(x_max-x_min)/grid_num_x )
        yticks_list = np.arange(y_min, y_max+1, step=(y_max-y_min)/grid_num_y )

        def format_change(x):
            if x<1:
                format_box = mpl.ticker.StrMethodFormatter('{x:,.0f}')
            else:
                format_box = mpl.ticker.StrMethodFormatter('{x:,.0f}')

            return format_box(x)

        plt.xticks(xticks_list, [format_change(x) for x in xticks_list])
        plt.yticks(yticks_list, [format_change(y) for y in yticks_list])

        # Set limits
        plt.ylim(y_min, y_max)
        plt.xlim(x_min, x_max)

        # 그리드 설정
        plt.grid(alpha=0.4, linestyle='--')

        # 틱 설정
        plt.tick_params(axis='both', direction='out', length = 3, pad = 6, labelsize = 20)

        # 색상 및 사이즈 설정
        # cmap_all=plt.get_cmap(face_color)
        # size = size 
        # #edge_c= edge_color 
        # edge_width = edge_width 
        # linewidth = linewidth
        # linestyle = linestyle
        # marker = marker
        # color = color

        # 색상
        #custom_pal = sns.color_palette('Greys_r', 8)
        # 심볼
        # all_shape=[ 'P', 'X', 'd','h','v','^','>','<', '8', 's','p','o','*','H','D', '$X$','1', '2', '3', '4', '+']

        #plt.title('Peak discharge')
        # plt.plot(x, result_K_6['Qp_rational'], label = 'MRM'
        #         ,linestyle = '-', linewidth = linewidth*3
        #         #, marker = all_shape[0], markersize = size
        #          , color = custom_pal[0])

        plt.plot(x, y, label = label
                ,linestyle = linestyle, linewidth = linewidth
                , marker = marker, markersize = size
                , color = color)
        #plt.show()

    def save_graph(self, file_name = 'test.png', dpi=300):

        plt.savefig(file_name, dpi=dpi, bbox_inches='tight')

