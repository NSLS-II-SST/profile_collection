import numpy as np
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import queue
from PIL import Image

run_report(__file__)
# Spiral searches

def spiralsearch(radius=2, stepsize=.4):
    x_center = sam_X.user_setpoint.value
    y_center = sam_Y.user_setpoint.value
    num = round(radius / stepsize)

    yield from spiral_square([sw_det, en.energy, Beamstop_SAXS, IzeroMesh], sam_X, sam_Y, x_center=x_center, y_center=y_center,
                     x_range=radius, y_range=radius, x_num=num, y_num=num)


def spiralsearch_all(barin=[],radius=2, stepsize=.4):
    for sample in barin:
        yield from load_sample(sample)
        RE.md['project_name'] = 'spiral_searches'
        try:
            yield from spiralsearch(radius, stepsize)
        except bluesky.utils.RequestAbort: #need to catch only a RE.stop() exception, NOT a RE.abort() to give the user a chance to bail on a scan and continue searching
            print("Requested an abort, breaking")
            break
        except bluesky.utils.RunEngineInterrupted:
            print("Stopped scan.  Waiting for your input.")


def map_bar_from_spirals(bar,spiralnums,barpos):
	
	for i,pos in enumerate(barpos):
		scan = db[spiralnums[i]]
		data = scan.table()
		print("Sample: " + bar[pos]['sample_name'])
		print("Scan id: "+ spiralnums[i])
		print('Enter good point number from spiral scan or anything non-numeric to skip:')
		good_point = input()
		if isnumeric(good_point):
			sam_x = data[good_point]['RSoXS Sample Outboard-Inboard']
			sam_y = data[good_point]['RSoXS Sample Up-Down']
			bar[pos]['location'][0]['position'] = sam_x
			bar[pos]['location'][1]['position'] = sam_y
		else:
			print('Non-numeric, not touching this sample')



# Bar imaging utilities:

# usage:

#load bar onto imager, load bar file, and do image_bar(bar,path='path_to_image')

# this will automatically go into image tagging, but to pick up where you left off, do 

# locate_samples_from_image(bar,'path_to_image')

# Find alignment fiducials in chamber
#
# Helpful functions goto_af1() goto_af2() and find_af1x(),find_af1y(),find_af2x(),find_af2y()
#
# and then remap the bar using
# correct_bar(bar,af1x,af1y,af2x,af2y)


def image_bar(bar,path = None):
    global loc_Q
    loc_Q = queue.Queue(1)
    ypos = np.arange(-100,110,25)
    images = []
    for pos in ypos:
        yield from bps.mv(sam_viewer,pos)
        imageuid = yield from bp.count([SampleViewer_cam],1)
        print(imageuid)
        images.append(next(db[imageuid].data('Sample Imager Detector Area Camera_image')))
    image = stich_sample(images, 25,5)
    update_bar(bar, loc_Q)
    if isinstance(path,str):
        im = Image.fromarray(image)
        im.save(path)


def locate_samples_from_image(bar,impath):
    global loc_Q
    loc_Q = queue.Queue(1)
    image = stich_sample(False,False,False,from_image=impath)
    update_bar(bar, loc_Q)


def bar_add_from_click(event):
    global bar
    #print(event.xdata, event.ydata)
    if(isinstance(bar,list)):
        barnum = int(input('Bar location : '))

        #print(event.xdata,event.ydata)
        if barnum >=0 and barnum < len(bar) :
            bar[barnum]['location'][0] = {'motor' : 'x','position': event.ydata}
            bar[barnum]['location'][1] = {'motor' : 'y','position': event.xdata}
            bar[barnum]['location'][2] = {'motor' : 'z','position': 0}
            bar[barnum]['location'][3] = {'motor' : 'th','position': 180}
            print('position added')
        else:
            print('Invalid bar location')
    else:
        print('invalid bar')


def update_bar(bar,loc_Q):
    from threading import Thread
    try:
        loc_Q.get_nowait()
    except Exception:
        ...

    def worker():
        global bar,sample_image_axes
        samplenum = 0
        while True:
#        for sample in bar:
            sample = bar[samplenum]
            print(f'Right-click on {sample["sample_name"]} location.  Press n on plot or enter to skip to next sample, p for previous sample, esc to end')
            # ipython input x,y or click in plt which outputs x, y location
            while True:
                try:
                    #print('trying')
                    item = loc_Q.get(timeout=1)
                except Exception:
                    #print('no item')
                    ...
                else:
                    #print('got something')
                    break
            if item is not ('enter' or 'escape' or 'n' or 'p') and isinstance(item,list):
                sample['location'] = item
                annotateImage(sample_image_axes,item,sample['sample_name'])
                # advance sample and loop
                sample += 1
            elif item is 'escape':
                print('aborting')
                break
            elif item is'enter' or item is 'n':
                print(f'leaving this {sample["sample_name"]} unchanged')
                sample += 1
            elif item is 'p':
                print('Previous sample')
                sample -= 1
            if(sample > len(bar)):
                print("done")
                break

    t = Thread(target=worker)
    t.start()


def annotateImage(axes,item,name):
    ycoord = item[0]['position']
    xcoord = item[1]['position']

    a = axes.annotate(name,
            xy=(xcoord,ycoord), xycoords='data',
            xytext=(xcoord-3,ycoord+10), textcoords='data',
            arrowprops=dict(color='red',arrowstyle='->'),
            horizontalalignment='center', verticalalignment='bottom',color='red')

    a.draggable()
    plt.draw()


def stich_sample(images, step_size, y_off, from_image=None,flip_file=False):
    global sample_image_axes

    if isinstance(from_image,str):
        im_frame = Image.open(from_image)
        result = np.array(im_frame)
        if(flip_file):
            result = np.flipud(result)
    else:
        pixel_step = int(step_size * (1760) / 25)
        pixel_overlap = 2464 - pixel_step
        result = images[0]
        i = 0
        for image in images[1:]:
            i += 1
            result = np.concatenate((image[(y_off * i):, :], result[:-(y_off), pixel_overlap:]), axis=1)
        result = np.flipud(result)


    fig, ax = plt.subplots()
    ax.imshow(result, extent=[0, 235, -14.5, 14.5])
    sample_image_axes = ax
    fig.canvas.mpl_connect('button_press_event', plot_click)
    fig.canvas.mpl_connect('key_press_event', plot_key_press)
    plt.show()
    return result


def print_click(event):
    #print(event.xdata, event.ydata)
    global bar, barloc
    item = []
    item.append({'motor': 'x', 'position': event.ydata})
    item.append({'motor': 'y', 'position': event.xdata})
    item.append({'motor': 'z', 'position': 0})
    item.append({'motor': 'th', 'position': 180})
    bar[loc]['location'] = item
    print(f'Setting location {barloc} on bar to clicked position')


def plot_click(event):
    #print(event.xdata, event.ydata)
    global loc_Q
    item = []
    item.append({'motor': 'x', 'position': event.ydata, 'order': 0})
    item.append({'motor': 'y', 'position': event.xdata, 'order': 0})
    item.append({'motor': 'z', 'position': 0, 'order': 0})
    item.append({'motor': 'th', 'position': 180, 'order': 0})
    if not loc_Q.full() and event.button == 3:
        loc_Q.put(item,block=False)


def plot_key_press(event):
    global loc_Q
    if not loc_Q.full() and (event.key == 'enter' or event.key == 'escape' or event.key == 'n' or event.key == 'p'):
        loc_Q.put(event.key,block=False)


def set_loc(bar_name,locnum):
    global bar, barloc
    bar = bar_name
    barloc = locnum

def go_to_af2():
    yield from bps.mv(sam_X,7.3,sam_Y,9.75)

def find_af2x():
    yield from bps.mvr(sam_Y,-4)
    yield from bp.rel_scan([IzeroMesh,Beamstop_SAXS,Beamstop_WAXS],sam_X,-3,3,61)
    yield from bps.mvr(sam_Y,4)

def find_af2y():
    yield from bps.mvr(sam_X,-4)
    yield from bp.rel_scan([IzeroMesh,Beamstop_SAXS,Beamstop_WAXS],sam_Y,-3,3,61)
    yield from bps.mvr(sam_X,4)
def go_to_af1():
    yield from bps.mv(sam_X,-8.75,sam_Y,-110.2)

def find_af1x():
    yield from bps.mvr(sam_Y,-4)
    yield from bp.rel_scan([IzeroMesh,Beamstop_SAXS,Beamstop_WAXS],sam_X,-3,3,61)
    yield from bps.mvr(sam_Y,4)

def find_af1y():
    yield from bps.mvr(sam_X,4)
    yield from bp.rel_scan([IzeroMesh,Beamstop_SAXS,Beamstop_WAXS],sam_Y,-3,3,61)
    yield from bps.mvr(sam_X,-4)


def offset_bar(bar, xoff, yoff, zoff, thoff):
    for samp in bar:
        for mot in samp['location']:
            if mot['motor'] is 'x':
                mot['position'] += xoff
            if mot['motor'] is 'y':
                mot['position'] += yoff
            if mot['motor'] is 'z':
                mot['position'] += zoff
            if mot['motor'] is 'th':
                mot['position'] += thoff


def flip_bar(bar):
    for samp in bar:
        for mot in samp['location']:
            if mot['motor'] is 'x':
                mot['position'] = .5 - mot['position']
            if mot['motor'] is 'th':
                mot['position'] = 180

def straighten_bar(bar,d_y, d_x, y_center):
 for samp in bar:
     xpos = samp['location'][0]['position']
     ypos = samp['location'][1]['position']
     samp['location'][0]['position'] = straighten_x(xpos,ypos,d_x,d_y,y_center)

def straighten_x(x, y, dx, dy, y_center ):
    return x - (y+y_center)*dx/dy

def correct_bar(bar,af1x,af1y,af2x,af2y,training_wheels=True):
    x_offset = af1x - bar[0]['location'][0]['position']
    y_offset = af1y - bar[0]['location'][1]['position']
    x_image_offset = bar[0]['location'][0]['position'] - bar[-1]['location'][0]['position']
    y_image_offset = bar[0]['location'][1]['position'] - bar[-1]['location'][0]['position']
    if(training_wheels):
        assert abs((af2y-af1y)-y_image_offset) < 5, "Hmm... " \
                                                    "it seems like the length of the bar has changed by more than" \
                                                    " 5 mm between the imager and the chamber.  \n \n Are you sure" \
                                                    " your alignment fiducials are correctly located?  \n\n If you're" \
                                                    " really sure, rerun with training_wheels=false."
    dx = (af2x-af1x) + x_image_offset
    dy = af2y-af1y


    for samp in bar:
        xpos = samp['location'][0]['position']
        ypos = samp['location'][1]['position']

        xpos = xpos + x_offset
        ypos = ypos + y_offset

        newx = xpos + (ypos - af1y) * dx/dy

        samp['location'][0]['position'] = newx
        samp['location'][1]['position'] = ypos

