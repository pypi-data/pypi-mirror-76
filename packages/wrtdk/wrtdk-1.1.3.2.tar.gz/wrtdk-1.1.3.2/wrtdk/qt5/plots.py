'''
Created on Aug 17, 2018

@author: reynolds
'''

import sys, random, math, matplotlib, platform
import numpy as np
from PyQt5.Qt import QFrame, QGridLayout, Qt
from PyQt5.QtWidgets import QStatusBar,QWidget,QApplication, QPushButton, QLineEdit, QLabel
#from matplotlib.pyplot import tight_layout
matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
if platform.system() != 'Linux': from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch

class Plot2DWidgetToolbar(QWidget):
	def __init__(self,parent=None):
		QWidget.__init__(self)
		self.plot=Plot2DWidget()
		self.toolbar=NavigationToolbar(self.plot, parent, True)
		l=QGridLayout()
		l.addWidget(self.plot,0,0)
		l.addWidget(self.toolbar,1,0)
		self.setLayout(l)
	def clear(self):
		for line in self.plot.axes.lines:
			del line
		
class PlotParameters(object):
    ''' a class for holding plot parameters '''
    def __init__(self,title='',xlabel='',ylabel='',zlabel=None,grid=True,lsize=10,tsize=16):
        '''  A class for containing the plot labels and properties '''
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.zlabel = zlabel
        self.grid = grid
        self.label_font = lsize
        self.title_font = tsize
class digitalPlotWidget(FigureCanvas):
	def __init__(self):
		self.fig = Figure(tight_layout=True)
		FigureCanvas.__init__(self,self.fig)
		FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.fig.add_subplot(111)
	'''
	x: xdata
	y: ydata
	yn: ynames
	'''
	def plt(self,x,y,yn):
		for i in range(len(y)):
			ax1.plot(x,y[:,i]+2*i,color='black')
		ax1.set_yticks(range(0,len(y)*2,2))
		ax1.set_yticklabels(yn)
class DataSelectionPlotWidget(QWidget):
    def __init__(self,parent=None,parameters=[],lines=1,width=5,height=4,dpi=100):
        ''' constructor for dataselection plot widget '''
        QWidget.__init__(self)
        self.plot=Plot2DWidget(lines=lines)
        
        self.toolbar=NavigationToolbar(self.plot, parent, True)
        layout = QGridLayout()
        layout.addWidget(self.plot       ,0,0,1,1)
        layout.addWidget(self.toolbar    ,1,0,1,1)
        self.setLayout(layout)
        self.zoom=-1
        self.xwind=1
        self.boarder=.05
        self.x=[]
        self.y=[]
        self.start_i=0
        self.stop_i=0
        self.init_plots()
    def set_style(self,style):
        if(style=='Lines'):
            self.plot.set_marker(0, 'None')
            self.plot.set_linestyle(0, '-')
            if(self.plot.line_total()>3):
                self.plot.set_linestyle(3, '-')
                self.plot.set_marker(3, 'None')
        elif(style=='Dots'):
            self.plot.set_marker(0, '.')
            self.plot.set_linestyle(0, 'None')
            if(self.plot.line_total()>3):
                self.plot.set_linestyle(3, 'none')
                self.plot.set_marker(3, '.')
        elif(style=='Both'):
            self.plot.set_marker(0, '.')
            self.plot.set_linestyle(0, '-')
            if(self.plot.line_total()>3):
                self.plot.set_linestyle(3, '-')
                self.plot.set_marker(3, '.')
        self.plot.refresh()
    def init_plots(self):
        self.plot.set_marker(0, '.')
        self.plot.set_linestyle(0, 'none')
        self.plot.set_color(0, 'k')
        self.plot.set_zorder(0,1)
        self.plot.set_marker(1, 'o', 12)
        self.plot.set_linestyle(1)
        self.plot.set_color(1, 'g')
        self.plot.set_zorder(1, 3)
        self.plot.set_marker(2, 'o', 12)     
        self.plot.set_linestyle(2)   
        self.plot.set_color(2, 'r')
        self.plot.set_zorder(2,4)
        if(self.plot.line_total()>3):
            self.plot.set_linestyle(3, 'none')
            self.plot.set_marker(3, '.')
            self.plot.set_color(3, 'c')
            self.plot.set_zorder(3,2)
            self.plot.set_legend(['GPS Data','Start','Stop','Selected'])
        else:
            self.plot.set_legend(['MAG Data','Start','Stop'])
    def set_data(self,x,y):
        self.x=x
        self.y=y
        self.start_i=0
        self.stop_i=len(x)-1
        self.plot.set_data(x, y, 0, False)
        self.plot.set_data(x[self.start_i], y[self.start_i], 1, False)
        self.plot.set_data(x[self.stop_i], y[self.stop_i] ,2, False)
        if(self.plot.line_total()>3):
            self.plot.set_data(x[self.start_i:self.stop_i+1], y[self.start_i:self.stop_i+1], 3, False)
        self.plot.refresh()
    def set_start(self,i):
        self.start_i=i
        self.plot.set_data(self.x[self.start_i], self.y[self.start_i], 1, False)
        if(self.plot.line_total()>3):
            self.plot.set_data(self.x[self.start_i:self.stop_i+1], self.y[self.start_i:self.stop_i+1], 3, False)
#         self.set_zoom(self.zoom)
    def set_stop(self,i):
        self.stop_i=i
        self.plot.set_data(self.x[self.stop_i], self.y[self.stop_i], 2, False)
        if(self.plot.line_total()>3):
            self.plot.set_data(self.x[self.start_i:self.stop_i+1], self.y[self.start_i:self.stop_i+1], 3, False)
#         self.set_zoom(self.zoom)
    def set_xwind(self,xwindow):
        ''' set the xwindow '''
        self.xwind=xwindow
    def set_boarder(self,boarder):
        ''' set the boarder percentage '''
        self.boarder=boarder
    def set_zoom(self,zoom):
        ''' select which zoom you want to use '''
        ''' NOT HAPPY WITH ZOOM START OR STOP '''
        self.zoom=zoom
        if(len(self.x)==0):
            return
        xmin=-1
        xmax=1
        ymin=-1
        ymax=1
        #let someone else control zoom
        if(self.zoom==-1):
            self.plot.axes.axis()
        #Full zoom
        elif (self.zoom==0):
            #if we're finding the full graph, just find the min and max points.
            xmin=min(self.x)
            ymin=min(self.y)
            xmax=max(self.x)
            ymax=max(self.y)
            
        #Selection zoom    
        elif (self.zoom==1):
            #same as zoom==0 except only look at the selected section.
            if(len(self.x[self.start_i:self.stop_i])<2):
                xmin=self.x[self.start_i]
                xmax=self.x[self.start_i]
                ymin=self.y[self.start_i]
                ymax=self.y[self.start_i]
            else:
                xmin=min(self.x[self.start_i:self.stop_i])
                ymin=min(self.y[self.start_i:self.stop_i])
                xmax=max(self.x[self.start_i:self.stop_i])
                ymax=max(self.y[self.start_i:self.stop_i])
            
            if(xmax<self.x[self.stop_i]):
                xmax=self.x[self.stop_i]
            if(ymax<self.y[self.stop_i]):
                ymax=self.y[self.stop_i]
            if(xmin>self.x[self.stop_i]):
                xmin=self.x[self.stop_i]
            if(ymin>self.y[self.stop_i]):
                ymin=self.y[self.stop_i]
            
        #zoom start
        elif(self.zoom==2):
            
            yabs=.1*abs(self.y[self.start_i])
            start_v=self.start_i
            done=True
            #iterate backwards to find the first place where either
            #we hit the beginning,
            #we hit the edge of the desired x-window
            #we find a value that is much larger in the y direction than the point
            #we find a value that is much smaller in the y direction than the point
            while(start_v>0 and done):
                if(self.x[start_v]<self.x[self.start_i]-self.xwind or 
                   self.y[start_v]>self.y[self.start_i]+yabs or 
                   self.y[start_v]<self.y[self.start_i]-yabs):
                    done=False
                start_v-=1
            
            done=True
            stop_v=self.start_i
            #same as above but iterating forward
            while(stop_v<self.stop_i and done):
                
                if(self.x[stop_v]>self.x[self.start_i]+self.xwind or 
                   self.y[stop_v]>self.y[self.start_i]+yabs or 
                   self.y[stop_v]<self.y[self.start_i]-yabs):
                    done=False
                stop_v+=1
            #edge case check for if the points are the same
            if len(self.x[start_v:stop_v])==0:
                xmin=self.x[start_v]
                xmax=self.x[start_v]
                ymin=self.y[start_v]
                ymax=self.y[start_v]
            else:
                xmin=min(self.x[start_v:stop_v])
                xmax=max(self.x[start_v:stop_v])
                ymin=min(self.y[start_v:stop_v])
                ymax=max(self.y[start_v:stop_v])
        #zoom stop
        elif(self.zoom==3):
            #basically the same logic as start
            yabs=.1*abs(self.y[self.stop_i])
            start_v=self.stop_i
            done=True
            while(start_v>self.start_i and done):
                if(self.x[start_v]<self.x[self.stop_i]-self.xwind or 
                   self.y[start_v]>self.y[self.stop_i]+yabs or 
                   self.y[start_v]<self.y[self.stop_i]-yabs):
                    done=False
                start_v-=1
            done=True
            stop_v=self.stop_i
            while(stop_v<len(self.x)-1 and done):
                if(self.x[stop_v]>self.x[self.stop_i]+self.xwind or 
                   self.y[stop_v]>self.y[self.stop_i]+yabs or 
                   self.y[stop_v]<self.y[self.stop_i]-yabs):
                    done=False
                stop_v+=1           
            if len(self.x[start_v:stop_v])==0:
                xmin=self.x[start_v]
                xmax=self.x[start_v]
                ymin=self.y[start_v]
                ymax=self.y[start_v]
            else:
                xmin=min(self.x[start_v:stop_v])
                xmax=max(self.x[start_v:stop_v])
                ymin=min(self.y[start_v:stop_v])
                ymax=max(self.y[start_v:stop_v])
        #edge case
        if(xmin==xmax==0):
            xmin=xmin-.05  
            xmax=xmax+.05
        if(ymin==ymax==0):
            ymin=ymin-.05
            ymax=ymax+.05 
        #add the boarder around the values.
        xmin2=xmin-self.boarder*abs(xmax-xmin)
        ymin2=ymin-self.boarder*abs(ymax-ymin)
        xmax2=xmax+self.boarder*abs(xmax-xmin)
        ymax2=ymax+self.boarder*abs(ymax-ymin)
        #set it and draw it
        self.plot.axes.axis(xmin=xmin2,
                       ymin=ymin2,
                       xmax=xmax2,
                       ymax=ymax2)



        self.plot.refresh()
        
class PlotWidget(FigureCanvas):
    ''' a super class for plot widgets in PyQt5 '''
    
    def __init__(self,parent=None,parameters=[],lines=1,width=5,height=5,dpi=100,n_axes=2):
        '''  Constructor  '''
        self.lines = []
        self.axes = []
        self._n = 0# the lines are incremented in add_line
        self._n_axes = n_axes
        
        # create the figure
        self.fig = Figure(figsize=(width,height),dpi=dpi,tight_layout=True)
        FigureCanvas.__init__(self,self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        #self._2d == self.is2D()
        #self._3d == self.is3D()
        
        # setup the plot
        self.setup_plot(lines)
        
        # set the plot parameters
        if parameters != []: self.set_properties(parameters)
        
        # adjust the plot to the screen size
        self.fig.tight_layout()
        
    def is2D(self):
        return self._n_axes == 2
    
    def is3D(self):
        return self._n_axes == 3
        
    def new_line(self):
        ''' adds a line to the plot '''
        self._n += 1
            
    def line_total(self):
        ''' returns the number of lines '''
        return self._n
    
    def compute_initial_figure(self):
        '''  Not sure what this does  '''
        pass
    def set_properties(self,labels):
        '''  Sets the labels for the plot  '''
        if self.axes == []: return
        self.axes.set_title(labels.title,fontsize=labels.title_font)
        self.axes.set_xlabel(labels.xlabel,fontsize=labels.label_font)
        self.axes.set_ylabel(labels.ylabel,fontsize=labels.label_font)
        if labels.zlabel != None: self.axes.set_zlabel(labels.zlabel,fontsize=labels.label_font)
        self.axes.grid(labels.grid)
        
    def setup_plot(self,lines):
        ''' setups the axes of the plot '''
        pass
    
    def refresh(self):
        ''' refreshes the plot '''
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
    
    def autoscale(self,autoscale=True,update=True):
        ''' scales the plot '''
        if autoscale:
            self.axes.relim()
            self.axes.autoscale_view()
        if update: self.refresh()
            
    def _limits(self,x,xn):
        ''' returns the limits of the plot '''
        return [min([min(x),min(xn)]),
                max([max(x),max(xn)])]
                       
    def _append_array(self,x,xn):
        ''' appends to an array '''
        return np.append(x,xn).tolist()
        
    def set_linestyle(self,line=0,style='None',linew=None):
        ''' sets the line style '''
        self.lines[line].set_linestyle(style)
        if linew != None: self.lines[line].set_linewidth(linew)
    def set_color(self,line=0,color='k'):
        ''' sets the line color '''
        self.lines[line].set_color(color)     
    def set_marker(self,line=0,marker='.',msize=None,fc=None,ec=None):
        ''' sets the marker style '''
        self.lines[line].set_marker(marker)
        if msize != None: self.lines[line].set_markersize(msize)
        if fc != None: self.lines[line].set_markerfacecolor(fc)
        if ec != None: self.lines[line].set_markeredgecolor(ec)
    def set_zorder(self,line,zorder):
        self.lines[line].set_zorder(zorder)
    def set_legend(self,leg=[],loc='best'):
        ''' sets the legend '''
        if leg == []: return
        if self._n < len(leg): leg = leg[:self.lines]
        self.axes.legend(leg,loc=loc)
    
    def set_aspect(self,aspect='equal'):
        ''' sets the aspect ratio '''
        if(self._n_axes == 3):
            print("ERROR: Can't set aspect for 3D plot in matplotlib")
            return
        self.axes.set_aspect(aspect)
        
    def set_title(self,txt=''):
        ''' sets the title of the axes '''
        self.axes.set_title(txt)
        self.refresh()
    
    def clear(self):
        ''' clears all the lines '''
        for i in range(self._n): self.clear_line(i,autoscale=False)
        for line in self.axes.lines:
        	del line
        self.refresh() 
        
    def clear_line(self,line=0,autoscale=True):
        ''' clears one line '''
        self.set_data([],[],line=line,autoscale=autoscale)
        
    def remove_line(self,line=0):
        ''' removes a line '''
        self._n -= 1
        self.lines[line].remove()
        del self.lines[line]
        
    def remove(self):
        ''' removes all lines '''
        for i in self._n: self.remove(i)
        
class Plot2DWidget(PlotWidget):
    ''' a plot for a Cartesian 2D plot '''
    
    def __init__(self,parent=None,parameters=[],lines=1,width=5,height=4,dpi=100):
        ''' constructor for 2D cartesian plot '''
        PlotWidget.__init__(self,parent,parameters,lines,width,height,dpi)
        
    def setup_plot(self,lines):
        ''' sets up a 2D cartesian plot axes and lines '''
        self.axes = self.fig.add_subplot(111)
        self.axes.grid(True)
        for _ in range(lines): self.add_line([],[])
            
    def add_line(self,x=[],y=[],*args,**kwargs):
        ''' adds a 2D line '''
        l, = self.axes.plot(x,y,*args,**kwargs)
        self.lines.append(l)
        if x != [] and y != []: self.autoscale(True)
        self.new_line()
        
    def clear_line(self,line=0,autoscale=True):
        ''' clears one line of data '''
        self.set_data([],[],line=line,autoscale=autoscale)
        
    def append(self,x=0,y=0,line=0,autoscale=True):
        ''' appends to the data set '''
        _x = self._append_array(self.lines[line].get_xdata(),x)
        _y = self._append_array(self.lines[line].get_ydata(),y)
        self.set_data(_x,_y,line=line,autoscale=autoscale)
        self.autoscale(autoscale)
        
    def set_xdata(self,x,line=0,autoscale=True):
        ''' sets the x data on the given line '''
        self.lines[line].set_xdata(x)
        self.autoscale(autoscale)
    def get_xline_data(self,line):
        return self.lines[line].get_xdata()
    def get_yline_data(self,line):
        return self.lines[line].get_ydata()
    #ATTEMPT FIX
    def set_aspect(self):
        pass
    def set_ydata(self,y,line=0,autoscale=True,update=True):
        ''' sets the y data on the given line '''
        self.lines[line].set_ydata(y)
        self.autoscale(autoscale,update=update)
        
    def set_data(self,x=0,y=0,line=0,autoscale=True,update=True):
        ''' set the data '''
        self.lines[line].set_data(x,y)
        self.autoscale(autoscale,update=update)
        
class Plot3DWidget(PlotWidget):
    ''' a class for 3D cartesian plot '''
    
    def __init__(self,parent=None,parameters=[],lines=1,width=5,height=4,dpi=100):
        ''' constructor for a 3D cartesian plot '''
        PlotWidget.__init__(self,parent,parameters,lines,width,height,dpi)
        
    def setup_plot(self,lines):
        ''' setup for axes and lines of a 2D cartesian plot '''
        self.axes = self.fig.add_subplot(111,projection='3d')
        self.axes.grid(True)
        for _ in range(lines): self.add_line([], [], [])
            
    def add_line(self,x=[],y=[],z=[],*args,**kwargs):
        ''' adds a 3D line '''
        l, = self.axes.plot(x,y,z,*args,**kwargs)
        self.lines.append(l)
        self.new_line()
        if x and y and z: self.autoscale(True)
        
    def clear_line(self,line=0,autoscale=True):
        ''' clears the specific line '''
        self.set_data([],[],[],line=line,autoscale=autoscale)
            
    def autoscale(self,autoscale=True):
        ''' autoscale the view '''
        if autoscale:
            x,y,z = self._limits3d()
            self.axes.auto_scale_xyz(x,y,z)
            self.axes.autoscale_view()
        self.refresh()
        
    def set_xdata(self,x,line=0,autoscale=True):
        ''' sets the x data '''
        self.lines[line].set_xdata(x)
        self.autoscale(autoscale)
        
    def set_ydata(self,y,line=0,autoscale=True):
        ''' sets the x data '''
        self.lines[line].set_ydata(y)
        self.autoscale(autoscale)
    
    def set_data(self,x,y,z,line=0,autoscale=True):
        ''' set the data '''
        self.lines[line].set_data(x,y)
        self.lines[line].set_3d_properties(z)
        self.autoscale(autoscale)
        
    def append(self,x,y,z,line=0,autoscale=True):
        ''' appends data '''
        _x,_y,_z =self.lines[line]._verts3d
        _x = self._append_array(_x,x)
        _y = self._append_array(_y,y)
        _z = self._append_array(_z,z)
        self.set_data(_x,_y,_z,line=line,autoscale=autoscale)
        
    def _limits3d(self):
        ''' returns the scale of the plot '''
        x,y,z = [],[],[]
        for l in self.lines:
            _x,_y,_z = l._verts3d
            x,y,z = np.append(x,_x),np.append(y,_y),np.append(z,_z)
        if not x.any(): x = [0,1]
        if not y.any(): y = [0,1]
        if not z.any(): z = [0,1]
            
        return [min(x),max(x)],[min(y),max(y)],[min(z),max(z)]
    
class Arrow3DWidget(PlotWidget):
    
    def __init__(self,parent=None,parameters=[],lines=1,width=5,height=4,dpi=100):
        ''' constructor for a 3D cartesian plot '''
        PlotWidget.__init__(self,parent,parameters,lines,width,height,dpi)
        
    def setup_plot(self,lines):
        ''' setup for axes and lines of a 2D cartesian plot '''
        self.axes = self.fig.add_subplot(111,projection='3d')
        self.axes.grid(True)
        
        # get the colormap
        cmap = matplotlib.cm.get_cmap('jet',lines)
        
        for i in range(lines):
            rgb = cmap(i)[:3]
            self.add_line([0,0],[0,0],[0,0],mutation_scale=20,lw=3,arrowstyle="-|>",color=matplotlib.colors.rgb2hex(rgb))
            
    def add_line(self,x=[],y=[],z=[],*args,**kwargs):
        ''' adds a 3D vector line '''
        self.new_line()
        l = Arrow3D(x,y,z,*args,**kwargs)
        self.lines.append(l)
        self.axes.add_artist(l)
        
    def clear_line(self,line=0,autoscale=True):
        ''' clears one line '''
        self.set_data(0,0,0,line=line,autoscale=autoscale)
            
    def set_limits(self,xmin,xmax,ymin,ymax,zmin,zmax):
        ''' sets the limits '''
        self.axes.set_xlim(xmin,xmax)
        self.axes.set_ylim(ymin,ymax)
        self.axes.set_zlim(zmin,zmax)
            
    def autoscale(self, autoscale=True):
        ''' scales the view '''
        if autoscale:
            x,y,z = self._limits3d()
            self.axes.auto_scale_xyz(x,y,z)
            self.axes.autoscale_view()
        self.refresh()
        
    def set_xdata(self,x,line=0,autoscale=True):
        ''' sets the x data '''
        self.lines[line].set_xdata(x)
        self.autoscale(autoscale)
        
    def set_ydata(self,y,line=0,autoscale=True):
        ''' sets the x data '''
        self.lines[line].set_ydata(y)
        self.autoscale(autoscale)
    
    def set_data(self,x,y,z,line=0,autoscale=True):
        ''' set the plot data '''
        self.lines[line].set_data(x,y,z)
        self.autoscale(autoscale)
            
    def set_legend(self,leg=[],loc='best'):
        ''' sets the legend '''
        if leg == []: return
        if self._n < len(leg): leg = leg[:self.lines]
        self.axes.legend(self.lines,leg,loc=loc)
            
    def _limits3d(self):
        ''' returns the scale of the plot '''
        
        # gather all the limits for the lines
        x,y,z = [],[],[]
        for l in self.lines:
            _x,_y,_z = l._verts3d
            x,y,z = np.append(x,_x),np.append(y,_y),np.append(z,_z)
            
        # make sure the lines are populated
        if not x.any(): x = [0,1]
        if not y.any(): y = [0,1]
        if not z.any(): z = [0,1]
        
        # set the limits to axes equal
        x,y,z = [min(x),max(x)],[min(y),max(y)],[min(z),max(z)]
        r = abs(max(x[1]-x[0],y[1]-y[0],z[1]-z[0]))/2
        return [-r,r]+np.sum(x)/2.0,[-r,r]+np.sum(y)/2.0,[-r,r]+np.sum(z)/2.0

class Arrow3D(FancyArrowPatch):
    ''' adds arrows to 3d lines '''
    
    def __init__(self, xs, ys, zs, *args, **kwargs):
        ''' constructor '''
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        ''' draws the patch '''
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, _ = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)
        
    def set_data(self,x,y,z):
        ''' sets the data '''
        self._verts3d = x,y,z

class WaterfallWidget(QFrame):
    ''' a class for a mean removed waterfall plot '''
    
    def __init__(self,parent=None,parameters=[],label='',lines=1,font=None):
        '''  constructor  '''
        QFrame.__init__(self,parent)
        
        self.label = self._get_qlabel(txt=label,font=font)
        self.value = self._get_qlineedit(font=font)
        self.plot = Plot2DWidget(parent=self,parameters=parameters,lines=lines)
        self.plot.axes.invert_yaxis()# invert the y axis
        
        l = QGridLayout()
        l.setSpacing(0)
        l.addWidget(self.label,0,0,1,1)
        l.addWidget(self.value,0,1,1,1)
        l.addWidget(self.plot,1,0,1,2)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setStyleSheet('background-color: white')
        
    def _get_qlabel(self,txt='',font=None,align=None):
        ''' creates the qlabels '''
        l = QLabel(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        return l
        
    def _get_qlineedit(self,txt='',font=None,align=None,readonly=False):
        ''' creates the qlabels '''
        l = QLineEdit(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        l.setReadOnly(readonly)
        return l
        
    def set_xdata(self,x,line=0,autoscale=True):
        ''' sets the x data '''
        self.plot.set_xdata(x,line,autoscale)
        
    def set_data(self,x,y,line=0,autoscale=True):
        ''' sets the line data '''
        self.plot.set_data(x,y,line,autoscale)
        
    def append(self,x,y,line=0,autoscale=True):
        ''' appends to the waterfall '''
        self.plot.append(x,y,line,autoscale)
        
    def setText(self,m=0,lbl='',fmt='%.2f',units=''):
        ''' Sets the text in the text box '''
        fmt = '%s %s %s' % (lbl,fmt,units)
        self.value.setText(fmt % (m))
        
    def set_legend(self,leg=[],loc='best'):
        ''' sets the legend '''
        self.plot.set_legend(leg,loc)
        
    def clear(self):
        ''' clears the waterfall plot and textbox '''
        self.plot.clear()
        self.value.setText('')
        
class Vector3DWidget(QFrame):
    ''' a class for plotting a 3d vector '''
    
    def __init__(self,parent=None,parameters=[],font=None):
        ''' constructor '''
        QFrame.__init__(self,parent)
        
        self.plot = Arrow3DWidget(parameters=parameters,lines=0)
        self.plot.add_line([0,0],[0,0],[0,0],mutation_scale=20,lw=3,arrowstyle="-|>",color='b')
        self.plot.add_line([0,0],[0,0],[0,0],mutation_scale=20,lw=3,arrowstyle="-|>",color='r')
        self.plot.add_line([0,0],[0,0],[0,0],mutation_scale=20,lw=3,arrowstyle="-|>",color='g')
        self.plot.add_line([0,0],[0,0],[0,0],mutation_scale=20,lw=3,arrowstyle="-|>",color='k')
        self.plot.set_legend(['x','y','z','Total'])
#         self.plot.set_aspect('equal')
        _x = self._get_qlabel(txt='x',font=font,align=Qt.AlignCenter)
        _y = self._get_qlabel(txt='y',font=font,align=Qt.AlignCenter)
        _z = self._get_qlabel(txt='z',font=font,align=Qt.AlignCenter)
        _t = self._get_qlabel(txt='Total', font=font, align=Qt.AlignCenter)
        self.x = self._get_qlineedit(font=font,readonly=True)
        self.y = self._get_qlineedit(font=font,readonly=True)
        self.z = self._get_qlineedit(font=font,readonly=True)
        self.t = self._get_qlineedit(font=font,readonly=True)
        _x.setStyleSheet('color: rgba(%f,%f,%f,%f);' % self._color2stylesheet(self.plot.lines[0].get_facecolor()))
        _y.setStyleSheet('color: rgba(%f,%f,%f,%f);' % self._color2stylesheet(self.plot.lines[1].get_facecolor()))
        _z.setStyleSheet('color: rgba(%f,%f,%f,%f);' % self._color2stylesheet(self.plot.lines[2].get_facecolor()))
        _t.setStyleSheet('color: rgba(%f,%f,%f,%f);' % self._color2stylesheet(self.plot.lines[3].get_facecolor()))
        self.x.setStyleSheet('color: rgba(%f,%f,%f,%f);' % self._color2stylesheet(self.plot.lines[0].get_facecolor()))
        self.y.setStyleSheet('color: rgba(%f,%f,%f,%f);' % self._color2stylesheet(self.plot.lines[1].get_facecolor()))
        self.z.setStyleSheet('color: rgba(%f,%f,%f,%f);' % self._color2stylesheet(self.plot.lines[2].get_facecolor()))
        self.t.setStyleSheet('color: rgba(%f,%f,%f,%f);' % self._color2stylesheet(self.plot.lines[3].get_facecolor()))
        
        #layout the map
        l = QGridLayout()
        l.setSpacing(0)
        l.addWidget(self.plot,0,1,8,1)
        l.addWidget(_x,0,0,1,1)
        l.addWidget(self.x,1,0,1,1)
        l.addWidget(_y,2,0,1,1)
        l.addWidget(self.y,3,0,1,1)
        l.addWidget(_z,4,0,1,1)
        l.addWidget(self.z,5,0,1,1)
        l.addWidget(_t,6,0,1,1)
        l.addWidget(self.t,7,0,1,1)
        l.setColumnStretch(0,1)
        l.setColumnStretch(1,4)
        #for i in range(4): 
        #    l.setColumnStretch(2*i,1)
        #    l.setColumnStretch(2*i+1,3)
        self.setLayout(l)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setStyleSheet('background-color: white')
        
    def _get_qlabel(self,txt='',font=None,align=None):
        ''' creates the qlabels '''
        l = QLabel(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        return l
        
    def _get_qlineedit(self,txt='',font=None,align=None,readonly=False):
        ''' creates the qlabels '''
        l = QLineEdit(txt)
        if font is not None: l.setFont(font)
        if align is not None: l.setAlignment(align)
        l.setReadOnly(readonly)
        return l
        
    def _color2stylesheet(self,color):
        ''' converts the color '''
        return (color[0]*255,color[1]*255,color[2]*255,color[3]*255)
        
    def set_data(self,x,y,z,ts=0,dp=2,units=''):
        ''' updates the vector plot '''
        self.plot.set_data([0,x],[0,0],[0,0],line=0,autoscale=False)
        self.plot.set_data([0,0],[0,y],[0,0],line=1,autoscale=False)
        self.plot.set_data([0,0],[0,0],[0,z],line=2,autoscale=False)
        self.plot.set_data([0,x],[0,y],[0,z],line=3,autoscale=True)
        fmt = '%' + str(ts) + '.' + str(dp) + 'f %s'
        self.x.setText(fmt % (x,units))
        self.y.setText(fmt % (y,units))
        self.z.setText(fmt % (z,units))
        self.t.setText(fmt % ( math.sqrt(x**2+y**2+z**2),units) )
        
    def clear(self):
        ''' clears the plot and textboxes '''
        self.set_data(0,0,0)
        self.x.setText('')
        self.y.setText('')
        self.z.setText('')

class B_scan(FigureCanvas):
    ''' 
    a class for B-Scan Graphs 
    tic=pixel
    '''
    """UNDO TO HERE"""
    def __init__(self,parent=None,parameters=[],data=[[0]],width=10,height=5,dpi=100,
                 xmin=[],xmax=[],ymin=[],ymax=[],
                 aspect='auto',origin='upper',cb=False):
        '''  Constructor  '''
        #Widget Setup
        self.fig = Figure(figsize=(width,height),dpi=dpi)
        FigureCanvas.__init__(self,self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #create the graph space
        self.axes = self.fig.add_subplot(111,aspect='equal')

        #Labels
        self.parameters=parameters
        #set aspect and origin
        self.aspect=aspect
        self.origin=origin
        self.cb=[]
        self.x_s=False
        self.y_s=False
        #Create the image with given parameters
        if(xmin!=[] or xmax!=[]):
            self.x_s=True
        if(ymin!=[] or ymax!=[]):
            self.y_s=True
        if(self.x_s and self.y_s):
            self.image=self.axes.imshow(data, cmap='gray',
                extent=(xmin,xmax,ymin,ymax),
                origin=self.origin,aspect=self.aspect)
        else:
            self.image=self.axes.imshow(data, cmap='gray',
                extent=(0,10,0,10),
                origin=self.origin,aspect=self.aspect)
        self.set_labels(self.parameters)
        #how many A scans have been done

    def get_data(self):
        return self.image.get_data()
    #set functions        
    def set_aspect(self,aspect='auto'):
        ''' sets the aspect ratio '''
        self.aspect=aspect
    def set_labels(self,labels):
        '''sets all labels. takes in a PlotParameters'''
        if (labels==[]):
            self.axes.set_title("")
            self.axes.set_xlabel("")
            self.axes.set_ylabel("")
        else:
            self.axes.set_title(labels.title,fontsize=labels.title_font)
            self.axes.set_xlabel(labels.xlabel,fontsize=labels.label_font)
            self.axes.set_ylabel(labels.ylabel,fontsize=labels.label_font)
            
        self.refresh()
    def setStrength(self,strength=''):
        pass
    def setStatus(self,status=''):
        pass
    def set_z_axis(self,zmin=[],zmax=[]):
        '''change the max and min z values.'''
        if(zmin==[] or zmax==[]):
            self.image.autoscale()
        else:
            self.image.set_clim(vmin=zmin,vmax=zmax)
    def set_axes(self, xmin=0,xmax=20,ymin=0,ymax=20):
        '''set x and y axis'''
        if (ymin>ymax):
            self.axes.invert_yaxis()
        self.image.set_extent((xmin,xmax,ymin,ymax))
    def set_cb(self, label="",lsize=10,tsize=6,active=True):
        '''function to add or remove colorbar'''
        if(active==True):
            #check if there is a color bar already. if not, make one.
            if(self.cb==[]):
                self.cb=self.fig.colorbar(self.my_im)
                self.cb.set_label(label=label,fontsize=lsize)
            else:
                self.cb.set_label(label=label,fontsize=lsize)
        else:
            if(self.cb!=[]):
                self.fig.delaxes(self.fig.axes[1])
                self.cb=[]        
        self.fig.tight_layout()


    def refresh(self):
        ''' refreshes the plot '''
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def set_data(self, data=[]):
        '''how to actually update the image'''
        if(not self.x_s and not self.y_s):
            self.set_axes(0,np.size(data,0),0,np.size(data,1))
        self.image.set_data(np.transpose(data))
        self.image.autoscale()
        self.refresh()
       
class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.button = QPushButton('Change')
        self.button2 = QPushButton('filter')
        self.arrow3 = Vector3DWidget(self,parameters=PlotParameters(title='Vector Magnetometer',
                                                                    xlabel='X',
                                                                    ylabel='Y',
                                                                    zlabel='Z',lsize=16))
        self.arrow3.plot.set_limits(-1,1,-1,1,-1,1)
        pars=PlotParameters(title="B-Scan",xlabel="distance",ylabel="frequency")
        self.Scan =B_scan(parameters=pars)
        
        
        self.plot2 = Plot2DWidget(self,
                                  parameters=PlotParameters(title='Plot2D',tsize=16),
                                  lines=0)
        self.plot2.add_line([],[],'b--')
        self.plot2.add_line([],[],'r--')
        self.plot2.set_legend(['Total Field','Compensated'])
        self.plot3 = Plot3DWidget(self,
                                  parameters=PlotParameters(title='Plot3D'),
                                  lines=0)
        self.plot3.add_line([],[],[],'b-')
        self.plot3.add_line([],[],[],'g-')
        self.plot3.set_legend(['Flight Path','g'])
        self.waterfall = WaterfallWidget(self,
                                         parameters=PlotParameters(title='Waterfall'),
                                         label='Mean Value:')
        
        self.statusbar = QStatusBar()
        self.statusbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout = QGridLayout()
        layout.addWidget(self.button,0,0,1,2)
        layout.addWidget(self.button2,0,1,1,2)
        layout.addWidget(self.plot2,1,0)
        layout.addWidget(self.plot3,1,1)
        layout.addWidget(self.Scan,2,0)
        layout.addWidget(self.arrow3,2,0)
        layout.addWidget(self.waterfall,2,1)
        layout.addWidget(self.statusbar,3,0)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)
        
        self.button.clicked.connect(self.onClick)
        self.button2.clicked.connect(self.onClick2)
        
    def onClick(self):
        # test 2D
        self.plot2.set_data([1,2,3,4,5,6],[1,2,3,4,5,6],line=0,autoscale=True)
        self.plot2.append([1,2,3,4,5,6],[2,3,4,5,6,7],line=1,autoscale=True)
        
        # test 3D
        self.plot3.set_data([1,2],[1,2],[1,14],line=0,autoscale=True)
        self.plot3.append(3,3,0,line=0,autoscale=True)
        self.plot3.append([2,2],[3,3],[0,1],line=1,autoscale=True)
        
        #test the arrow
        x = 50*random.random()-25
        y = 50*random.random()-25
        z = 50*random.random()-25
        t = (x**2+y**2+z**2)**.5
        self.arrow3.set_data(x,y,z,units='nT')
        
        # test waterfall
        self.waterfall.set_data([1,2,2,0],[1,2,3,4],autoscale=True)
        self.waterfall.append([2,3,4,5],[5,6,7,8],autoscale=True)
        self.waterfall.setText(1.234,'DC Offset:','%.2f','mH')
        self.waterfall.clear()


        #test B-Scan
        data=np.zeros([100,1000])
        for i in range(np.size(data,0)):
            a=np.arange(np.size(data,1))
            r=random.randint(0,2)
            if(r==0):
                data[i]=a
            else:
                data[i]=np.flip(a)
            self.Scan.set_data(data)
    def onClick2(self):
    	#test B-Scan
        data=np.zeros([300,2000])
        filtered=np.zeros([300,2000])
        for i in range(np.size(data,0)):
            a=(2000)*np.random.randint(1,2000,np.size(data,1))
            r=random.randint(0,2)
            if(r==0):
                a[100:400]=800
                data[i]=a
            elif(r==1):
                a[400:600]=200
                data[i]=a
            else:
                data[i]=np.flip(a)
            data[i,800:900]=240
            filtered[:i,:]=GPR_filter(data[:i,:],gwin=50,pos=i)
            
            self.Scan.set_data(filtered)
def GPR_proc(real_data=[],imaginary_data=[],t=True):
    '''take complex data and fourier transform into output data'''
    #combine real and imaginary into a single complex nparray
    complex_data=np.empty(real_data.size, dtype=complex)
    for i in range(real_data.size):
        complex_data[i]=complex(real_data[i],imaginary_data[i])
    #perform inverse fast fourier transform of the data
    ifft_data=np.fft.ifft(complex_data,1024)
    #get the real part of the transpose of ifft_data
    #using same variable names...
    A=ifft_data.real
    if t:   #result without any processing
        return A
def GPR_filter(A=[],gwin=25,pos=0):
    '''
    assumes A is (Frequencies, A-Scans)
    takes in FULL B-Scan Data, and processes it(IDENTICAL TO GPR_PROC.m)
    '''
    
    #mean(background) removal
    a=np.copy(A)
    y=np.copy(A)
    for j in range(np.size(A,1)):
        a[:pos,j]=A[:pos,j]-np.mean(A[:pos,j])
    #return a
    #NOT WORKING
    
    #adjust gain with depth using gain window
    
    for j in range(pos-(gwin)+1):
        avg=np.mean(np.abs(a[j:(j+gwin)]))
        y[j:j+gwin]=a[j:j+gwin]/avg
    return y
if __name__.startswith('__main__'):
    print('matplotlib.__version__: %s' % matplotlib.__version__)
    print('matplotlib.__version__numpy__: %s' % matplotlib.__version__numpy__)
    print('numpy.__version__: %s' % np.__version__)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Color Picker Demo")
    window.show()
    app.exec_()
    