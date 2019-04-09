
from matplotlib.colors import LogNorm
import numpy as np

def quick_view(hdr):
    waxs = next(hdr.data('Small and Wide Angle Synced CCD Detectors_waxs_image'))
    saxs = next(hdr.data('Small and Wide Angle Synced CCD Detectors_saxs_image'))
    fig = plt.figure('SAXS / WAXS RSoXS snap')
    fig.set_tight_layout(1)



    if not fig.axes:
        saxs_ax, waxs_ax = fig.subplots(1, 2)
        waxs_ax.set_title('Wide Angle')
        saxs_ax.set_title('Small Angle')
        waxsim = waxs_ax.imshow(waxs,norm=LogNorm())
        waxsbar = plt.colorbar(waxsim, ax=waxs_ax)
        saxsim =  saxs_ax.imshow(saxs,norm=LogNorm())
        saxsbar = plt.colorbar(saxsim, ax=saxs_ax)
        mngr = plt.get_current_fig_manager()
        mngr.window.setGeometry(-1920, 30, 1850, 1050)
        zps = ZoomPan()
        zpw = ZoomPan()
        scale = 1.5
        figZooms = zps.zoom_factory(saxs_ax, base_scale=scale)
        figZoomw = zpw.zoom_factory(waxs_ax, base_scale=scale)
        figPans = zps.pan_factory(saxs_ax)
        figPanw = zpw.pan_factory(waxs_ax)
    else:
        saxs_ax, waxs_ax,w2,s2 = fig.axes
        waxs_ax.images[0].set_data(waxs)
        saxs_ax.images[0].set_data(saxs)
        waxs_ax.images[0].set_norm(LogNorm())
        saxs_ax.images[0].set_norm(LogNorm())
        waxsbar = waxs_ax.images[0].colorbar
        saxsbar = saxs_ax.images[0].colorbar
    num_ticks = 2
    waxsbar.set_ticks(np.linspace(np.ceil(waxs.min())+10, np.floor(waxs.max()-10), num_ticks),update_ticks=True)
    waxsbar.update_ticks()
    saxsbar.set_ticks(np.linspace(np.ceil(saxs.min())+10, np.floor(saxs.max()-10), num_ticks),update_ticks=True)
    saxsbar.update_ticks()

class ZoomPan:

    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.xzoom = True
        self.yzoom = True
        self.cidBP = None
        self.cidBR = None
        self.cidBM = None
        self.cidKeyP = None
        self.cidKeyR = None
        self.cidScroll = None
        self.plotted_text = []

    def zoom_factory(self, ax, base_scale = 2.):

        def zoom(event):
            if event.inaxes != ax: return
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            xdata = event.xdata  # get event x location
            ydata = event.ydata  # get event y location
            if(xdata is None):
                return()
            if(ydata is None):
                return()

            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print(event.button)

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            if(self.xzoom):
                ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            if(self.yzoom):
                ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])

            # Limits for the extent
            x_start = xdata - new_width * (1-relx)
            x_end = xdata + new_width * (relx)
            y_start = ydata - new_height * (1-rely)
            y_end = ydata + new_height * (rely)
            sizex = np.int(abs(x_end - x_start))
            sizey = np.int(abs(y_end - y_start))
            for child in self.plotted_text:
                child.remove()
                del(child)
            self.plotted_text.clear()
            if sizex < 30 and sizey < 30:
                # Add the text
                jump_x = 0.5
                jump_y = 0.5
                x_positions = np.linspace(start=x_start + 1, stop=x_end + 1, num=sizex, endpoint=False)
                y_positions = np.linspace(start=y_start, stop=y_end, num=sizey, endpoint=False)

                for y_index, y in enumerate(y_positions):
                    for x_index, x in enumerate(x_positions):
                        label = ax.images[0].get_array()[np.int(y), np.int(x)]
                        text_x = x - jump_x
                        text_y = y - jump_y
                        self.plotted_text.append(ax.text(text_x,
                                                         text_y,
                                                         label,
                                                         color='black',
                                                         ha='center',
                                                         va='center',
                                                         fontsize=10,
                                                         rotation=30))
            ax.figure.canvas.draw()
            ax.figure.canvas.flush_events()

        def onKeyPress(event):
            if event.key == 'x':
                self.xzoom = True
                self.yzoom = False
            if event.key == 'y':
                self.xzoom = False
                self.yzoom = True

        def onKeyRelease(event):
            self.xzoom = True
            self.yzoom = True

        fig = ax.get_figure() # get the figure of interest

        self.cidScroll = fig.canvas.mpl_connect('scroll_event', zoom)
        self.cidKeyP = fig.canvas.mpl_connect('key_press_event',onKeyPress)
        self.cidKeyR = fig.canvas.mpl_connect('key_release_event',onKeyRelease)

        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press


        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)



            sizex = np.int(abs(self.cur_xlim[1] - self.cur_xlim[0]))
            sizey = np.int(abs(self.cur_ylim[1] - self.cur_ylim[0]))
            for child in self.plotted_text:
                child.remove()
                del(child)
            self.plotted_text.clear()
            if sizex < 30 and sizey < 30:
                # Add the text
                jump_x = 0.5
                jump_y = 0.5
                x_positions = np.linspace(start=self.cur_xlim[0]+1, stop=self.cur_xlim[1]+1, num=sizex, endpoint=False)
                y_positions = np.linspace(start=self.cur_ylim[0], stop=self.cur_ylim[1], num=sizey, endpoint=False)

                for y_index, y in enumerate(y_positions):
                    for x_index, x in enumerate(x_positions):
                        label = ax.images[0].get_array()[np.int(y), np.int(x)]
                        text_x = x - jump_x
                        text_y = y - jump_y
                        self.plotted_text.append(ax.text(text_x,
                                                         text_y,
                                                         label,
                                                         color='black',
                                                         ha='center',
                                                         va='center',
                                                         fontsize=10,
                                                         rotation=30))
            ax.figure.canvas.draw()
            ax.figure.canvas.flush_events()

        fig = ax.get_figure() # get the figure of interest

        self.cidBP = fig.canvas.mpl_connect('button_press_event',onPress)
        self.cidBR = fig.canvas.mpl_connect('button_release_event',onRelease)
        self.cidBM = fig.canvas.mpl_connect('motion_notify_event',onMotion)
        # attach the call back

        #return the function
        return onMotion

def spawn_quick_view(name, doc):
    if name == 'stop':
        # A run just completed. Look it up in databroker.
        uid = doc['run_start']  # the 'Run Start UID' used to identify a run.
        hdr = db[uid]
        quick_view(hdr)

RE.subscribe(spawn_quick_view)