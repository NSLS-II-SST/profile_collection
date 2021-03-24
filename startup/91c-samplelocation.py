import numpy as np
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import queue
from PIL import Image

run_report(__file__)


def default_sample(name):
    return {'proposal_id': 'C-308244', # we set the default folder here - most data shouldn't be taken
            'saf_id': 306821,
            'acquisitions': [],
            'components': '',
            'composition': '',
            'bar_loc': {'spot': '0C',
                        'front': True,
                        'th': 90,
                        'x0': 2.7,
                        'ximg': 1.4,
                        'y0': -186.3,
                        'yimg': -182.2,
                        'th0': 0,
                        'xoff': 1.86,
                        'zoff': -1.8,
                        'z0': 0,
                        'af1y': -186.35,
                        'af2y': 4,
                        'af1zoff': 1.67,
                        'af2zoff': 4.83,
                        'af1xoff': 1.865,
                        'af2xoff': 1.83},
            'bar_spot': '0C',
            'front': True,
            'grazing': False,
            'height': 0.0,
            'angle': 90,
            'density': '',
            'location': [{'motor': 'x', 'position': 3.71, 'order': 0},
                         {'motor': 'y', 'position': -186.3, 'order': 0},
                         {'motor': 'z', 'position': 0, 'order': 0},
                         {'motor': 'th', 'position': 90, 'order': 0}],
            'project_desc': 'Calibration',
            'samp_user_id': 1,
            'sample_date': '2021-03-09 00:00:00',
            'sample_id': name,
            'sample_name': name,
            'sample_desc': name,
            'project_name': 'Calibration',
            'notes': '',
            'sample_set': '',
            'sample_state': 'back',
            'thickness': 0}


# Spiral searches


def samxscan():
    yield from psh10.open()
    yield from bp.rel_scan([Beamstop_SAXS], sam_X, -2, 2, 41)
    yield from psh10.close()


def spiralsearch(diameter=.6, stepsize=.2, energy=270, pol=0):
    yield from bps.mv(en, energy)
    yield from set_polarization(pol)
    x_center = sam_X.user_setpoint.get()
    y_center = sam_Y.user_setpoint.get()
    num = round(diameter / stepsize) + 1
    yield from spiral_square([saxs_det], sam_X, sam_Y, x_center=x_center, y_center=y_center,
                             x_range=diameter, y_range=diameter, x_num=num, y_num=num)


def spiraldata(diameter=.6, stepsize=.2, energy=None, exp_time=None):
    if energy is not None:
        if energy > 70 and energy < 2200:
            yield from bps.mv(en, energy)
    if exp_time is not None:
        if exp_time > 0.001 and exp_time < 1000:
            set_exposure(exp_time)
    x_center = sam_X.user_setpoint.get()
    y_center = sam_Y.user_setpoint.get()
    num = round(diameter / stepsize) + 1
    yield from spiral_square([saxs_det], sam_X, sam_Y, x_center=x_center, y_center=y_center,
                             x_range=diameter, y_range=diameter, x_num=num, y_num=num)


def spiralsearch_all(barin=[], diameter=.5, stepsize=.2):
    for samp in barin:
        yield from load_sample(samp)
        RE.md['project_name'] = 'spiral_searches'
        sample()
        rsoxs_bot.send_message(f'running spiral scan on {samp["proposal_id"]} {samp["sample_name"]}')
        yield from spiralsearch(diameter, stepsize)


def spiralsearchwaxs(diameter=.6, stepsize=.2, energy=None):
    if energy is not None:
        if energy > 150 and energy < 2200:
            yield from bps.mv(en, energy)
    x_center = sam_X.user_setpoint.get()
    y_center = sam_Y.user_setpoint.get()
    num = round(diameter / stepsize) + 1
    yield from spiral_square([waxs_det], sam_X, sam_Y, x_center=x_center, y_center=y_center,
                             x_range=diameter, y_range=diameter, x_num=num, y_num=num)


def spiralsearchwaxs_all(barin=[], diameter=.5, stepsize=.2):
    for sample in barin:
        yield from load_sample(sample)
        RE.md['project_name'] = 'spiral_searches'
        yield from spiralsearchwaxs(diameter, stepsize)


def map_bar_from_spirals(bar, spiralnums, barpos):
    for i, pos in enumerate(barpos):
        scan = db[spiralnums[i]]
        data = scan.table()
        print("Sample: " + bar[pos]['sample_name'])
        print("Scan id: " + spiralnums[i])
        print("Enter good point number from spiral scan or anything non-numeric to skip:")
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

# load bar onto imager, load bar file, and do image_bar(bar,path='path_to_image')

# this will automatically go into image tagging, but to pick up where you left off, do 

# locate_samples_from_image(bar,'path_to_image')

# Find alignment fiducials in chamber
#
# Helpful functions goto_af1() goto_af2() and find_af1x(),find_af1y(),find_af2x(),find_af2y()
#
# and then remap the bar using
# correct_bar(bar,af1x,af1y,af2x,af2y)



def image_bar(bar, path=None,front=True):
    global loc_Q
    loc_Q = queue.Queue(1)
    ypos = np.arange(-100, 110, 25)
    images = []

    imageuid = yield from bp.list_scan([SampleViewer_cam], sam_viewer, ypos)
    print(imageuid)
    images = list(db[imageuid].data('Sample Imager Detector Area Camera_image'))
    image = stitch_sample(images, 25, -6) # this will start the interactive pointing of samples
    update_bar(bar, loc_Q,front)
    if isinstance(path, str):
        im = Image.fromarray(image)
        im.save(path)


def locate_samples_from_image(bar, impath,front=True):
    # if the image was just taken itself, before a bar was compiled, then this can be run to just load that image
    # and then interactively place the elements of bar
    global loc_Q
    loc_Q = queue.Queue(1)
    if(front):
        image = stitch_sample(False, False, False, from_image=impath, flip_file=False) # this starts the sample pointing
    else:
        image = stitch_sample(False, False, False, from_image=impath, flip_file=False)
    # stitch samples will be sending signals, update bar will catch those signals and assign the positions to the bar
    update_bar(bar, loc_Q, front)


def update_bar(bar, loc_Q,front):
    '''
    updated with whether we are pointing at the front or the back of the bar
    '''
    from threading import Thread
    try:
        loc_Q.get_nowait()
    except Exception:
        ...

    def worker():
        global bar, sample_image_axes
        samplenum = 0
        if(front):
            # add / replace the front fiducial bar entries (bar[0], bar[-1])
            AF1 = default_sample('AF1_front')
            AF2 = default_sample('AF2_front')
            if sample_by_name(bar, 'AF1_front') is not None:
                bar.remove(sample_by_name(bar, 'AF1_front'))
            if sample_by_name(bar, 'AF2_front') is not None:
                bar.remove(sample_by_name(bar, 'AF2_front'))
            bar.insert(0,AF1)
            bar.append(AF2)
            # add in a diode position as well
            diode = default_sample('diode')
            if sample_by_name(bar, 'diode') is not None:
                bar.remove(sample_by_name(bar, 'diode'))
            bar.insert(-1, diode)

        else:
            # if front fiducials don't exist,add dummy ones (so thge AF2 ones are in the correct position)
            if sample_by_name(bar,'AF1_front') is None:
                AF1 = default_sample('AF1_front')
                bar.insert(0, AF1)
            if sample_by_name(bar,'AF2_front') is None:
                AF2 = default_sample('AF2_front')
                bar.append(AF2)

            # add / replace the back fiducial bar entries (bar[1], bar[-2])

            if sample_by_name(bar, 'AF1_back') is not None:
                bar.remove(sample_by_name(bar, 'AF1_back'))
            if sample_by_name(bar, 'AF2_back') is not None:
                bar.remove(sample_by_name(bar, 'AF2_back'))
            AF1 = default_sample('AF1_back')
            AF2 = default_sample('AF2_back')
            AF1['front'] = False
            AF2['front'] = False
            bar.insert(1,AF1) # inserts in the second position
            bar.insert(-1,AF2) # inserts in the second to last position
        while True:
            #        for sample in bar:
            sample = bar[samplenum]
            if sample['front'] != front: # skip if we are not on the right side of the sample bar
                                         # (only locate samples that we can see in this image!)
                samplenum += 1
                if samplenum >= len(bar):
                    print("done")
                    break
                else:
                    continue
            print(
                f'Right-click on {sample["sample_name"]} location (recorded location is {sample["bar_loc"]["spot"]}).  ' +
                'Press n on plot or enter to skip to next sample, p for previous sample, esc to end')
            # ipython input x,y or click in plt which outputs x, y location
            while True:
                try:
                    # print('trying')
                    item = loc_Q.get(timeout=1)
                except Exception:
                    # print('no item')
                    ...
                else:
                    # print('got something')
                    break
            if item is not ('enter' or 'escape' or 'n' or 'p') and isinstance(item, list):
                sample['location'] = item
                sample['bar_loc']['ximg']=item[0]['position']
                sample['bar_loc']['yimg']=item[1]['position']
                if front:
                    sample['bar_loc']['th0']=0
                else:
                    sample['bar_loc']['th0'] = 180
                annotateImage(sample_image_axes, item, sample['sample_name'])
                # advance sample and loop
                samplenum += 1
            elif item is 'escape':
                print('aborting')
                break
            elif item is 'enter' or item is 'n':
                print(f'leaving this {sample["sample_name"]} unchanged')
                samplenum += 1
            elif item is 'p':
                print('Previous sample')
                samplenum -= 1
            if (samplenum >= len(bar)):
                print("done")
                break

    t = Thread(target=worker)
    t.start()


def annotateImage(axes, item, name):
    ycoord = item[0]['position']
    xcoord = item[1]['position']

    a = axes.annotate(name,
                      xy=(xcoord, ycoord), xycoords='data',
                      xytext=(xcoord - 3, ycoord + 10), textcoords='data',
                      arrowprops=dict(color='red', arrowstyle='->'),
                      horizontalalignment='center', verticalalignment='bottom', color='red')

    a.draggable()
    plt.draw()


def stitch_sample(images, step_size, y_off, from_image=None, flip_file=False):
    global sample_image_axes

    if isinstance(from_image, str):
        im_frame = Image.open(from_image)
        result = np.array(im_frame)
        if (flip_file):
            result = np.flipud(result)
    else:
        pixel_step = int(step_size * (1760) / 25)
        pixel_overlap = 2464 - pixel_step
        result = images[0][0]
        i = 0
        for imageb in images[1:]:
            image = imageb[0]
            i += 1
            if y_off>0:
                result = np.concatenate((image[(y_off * i):, :], result[:-(y_off), pixel_overlap:]), axis=1)
            elif y_off<0:
                result = np.concatenate((image[:(y_off * i), :], result[-(y_off):, pixel_overlap:]), axis=1)
            else:
                result = np.concatenate((image[:,:], result[:, pixel_overlap:]), axis=1)
        # result = np.flipud(result)

    fig, ax = plt.subplots()
    ax.imshow(result, extent=[-210, 25, -14.5, 14.5])
    sample_image_axes = ax
    fig.canvas.mpl_connect('button_press_event', plot_click)
    fig.canvas.mpl_connect('key_press_event', plot_key_press)
    plt.show()
    return result


def print_click(event):
    # print(event.xdata, event.ydata)
    global bar, barloc
    item = []
    item.append({'motor': 'x', 'position': event.ydata})
    item.append({'motor': 'y', 'position': event.xdata})
    item.append({'motor': 'z', 'position': 0})
    item.append({'motor': 'th', 'position': 180})
    bar[loc]['location'] = item
    print(f'Setting location {barloc} on bar to clicked position')


def plot_click(event):
    # print(event.xdata, event.ydata)
    global loc_Q
    item = []
    item.append({'motor': 'x', 'position': event.ydata, 'order': 0})
    item.append({'motor': 'y', 'position': event.xdata, 'order': 0})
    item.append({'motor': 'z', 'position': 0, 'order': 0})
    item.append({'motor': 'th', 'position': 180, 'order': 0})
    if not loc_Q.full() and event.button == 3:
        loc_Q.put(item, block=False)


def plot_key_press(event):
    global loc_Q
    if not loc_Q.full() and (event.key == 'enter' or event.key == 'escape' or event.key == 'n' or event.key == 'p'):
        loc_Q.put(event.key, block=False)

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


def correct_bar(bar, fiduciallist, include_back, training_wheels=True):
    '''
    originally this function adjusted the x, y, positions of samples on a bar
    to align with the x-y locations found by fiducials
    now the fiducial needs 4 x measurements at the different angles, (-90,0.90,180)
    and the one measurement of y for each fiducial
    and the sample z offset can be found as well
    so apritrary angles can be gone to if requested (this should be recorded in the 'th' parameter in bar_loc

    fiducial list is the list output by find_fiducials()
    '''
    af2y = fiduciallist[0]
    af2xm90 = fiduciallist[1]
    af2x0 = fiduciallist[2]
    af2x90 = fiduciallist[3]
    af2x180 = fiduciallist[4]
    af1y = fiduciallist[5]
    af1xm90 = fiduciallist[6]
    af1x0 = fiduciallist[7]
    af1x90 = fiduciallist[8]
    af1x180 = fiduciallist[9]
    af1_front = sample_by_name(bar,"AF1_front")
    af2_front = sample_by_name(bar,"AF2_front")
    af1_back = sample_by_name(bar,"AF1_back")
    af2_back = sample_by_name(bar,"AF2_back")
    if af1_back is None:
        back = False
    else:
        back = include_back
    af1x_img = af1_front['location'][0]['position']
    af1y_img = af1_front['location'][1]['position']
    af2x_img = af2_front['location'][0]['position']
    af2y_img = af2_front['location'][1]['position']
    # adding the possibility of a back fiducial position as well as front
    # these will be nonsense if there was no back image (image bar didn't add in these positions)
    # but they won't be used, unless a sample is marked as being on the back
    if back:
        af1xback_img = af1_back['location'][0]['position']
        af1yback_img = af1_back['location'][1]['position']
        af2xback_img = af2_back['location'][0]['position']
        af2yback_img = af2_back['location'][1]['position']



    af1x, af1zoff,af1xoff = af_rotation(af1xm90, af1x0, af1x90, af1x180) # find the center of rotation from fiducials
    af2x, af2zoff,af2xoff = af_rotation(af2xm90, af2x0, af2x90, af2x180)
    # these values are the corresponding values at theta=0,
    # which is what we want if the image is of the front of the bar
    af1xback = rotatedx(af1x,180,af1zoff,af1xoff)
    af2xback = rotatedx(af2x,180,af2zoff,af2xoff)
    # if we are looking at the sample from the back,
    # then we need to rotate the fiducial x and y location for the sample corrections

    x_offset = af1x - af1x_img # offset from X-rays to image in x
    y_offset = af1y - af1y_img # offset from X-rays to image in y
    y_image_offset = af1y_img - af2y_img  # distance between fiducial y positions (should be ~ -190)
    if back:
        x_offset_back = af1xback - af1xback_img  # offset from X-rays to image in x
        y_offset_back = af1y - af1yback_img  # offset from X-rays to image in x
        y_image_offset_back = af1yback_img - af2yback_img  # distance between fiducial y positions (should be ~ -190)

    if (training_wheels):
        assert abs(abs(af2y - af1y) - abs(y_image_offset)) < 5, \
            "Hmm... " \
            "it seems like the length of the bar has changed by more than" \
            " 5 mm between the imager and the chamber.  \n \n Are you sure" \
            " your alignment fiducials are correctly located?  \n\n If you're" \
            " really sure, rerun with training_wheels=false."

    dx = af2x - af2x_img - x_offset  # offset of Af2 X-rays to image in x relative to Af1 (mostly rotating)
    dy = af2y - af2y_img - y_offset  # offset of Af2 X-rays to image in y relative to Af1 (mostly stretching)
    if back:
        dxb = af2xback - af2xback_img - x_offset_back  # offset of Af2 X-rays to image in x relative to Af1 (mostly rotating)
        dyb = af2y - af2yback_img - y_offset_back  # offset of Af2 X-rays to image in y relative to Af1 (mostly stretching)

    run_y = af2y - af1y # (distance between the fiducial markers) (above are the total delta over this run,
                        # in between this will be scaled

    for samp in bar:
        xpos = samp['bar_loc']['ximg'] # x position from the image
        ypos = samp['bar_loc']['yimg'] # y position from the image
        xoff = af1xoff - (af1xoff - af2xoff) * (ypos - af1y) / run_y
        samp['bar_loc']['xoff'] = xoff  # this should pretty much be the same for both fiducials,
        # but just in case there is a tilt,
        # we account for that here

        if samp['front']:
            newx = xpos + x_offset + (ypos - af1y) * dx / run_y
            newy = ypos + y_offset + (ypos - af1y) * dy / run_y
            samp['bar_loc']['x0'] = newx # these are the positions at 0 rotation, so for the front, we are already good
        elif back:
            newx = xpos + x_offset_back + (ypos - af1y) * dxb / run_y
            newy = ypos + y_offset_back + (ypos - af1y) * dyb / run_y
            samp['bar_loc']['x0'] = 2*xoff - newx # these are the positions at 0 rotation,
                                                    # so for the back, we have to correct
        else:
            continue # sample is on the back, and we are not doing the back of the bar, so skip
        samp['bar_loc']['y0'] = newy
        # recording of fiducial information as well with every sample, so they will know how to rotate
        samp['bar_loc']['af1y'] = af1y
        samp['bar_loc']['af2y'] = af2y
        samp['bar_loc']['af1xoff'] = af1xoff
        samp['bar_loc']['af2xoff'] = af2xoff
        samp['bar_loc']['af1zoff'] = af1zoff
        samp['bar_loc']['af2zoff'] = af2zoff

        zoff = zoffset(af1zoff,af2zoff,newy,front=samp['front'],height=samp['height'],af1y=af1y,af2y=af2y)
        samp['bar_loc']['zoff'] = zoff

        # now we can rotate the sample to the desired position (in the 'angle' metadata)
        # moving z is dangerous = best to keep it at 0 by default
        rotate_sample(samp) # this will take the positions found above and the desired incident angle and
                            # rotate the location of the sample accordingly


def zoffset(af1zoff,af2zoff,y,front=True,height=.25,af1y=-186.3,af2y=4):
    '''
    Using the z offset of the fiducial positions from the center of rotation,
    project the z offset of the surface of a given sample at some y position between
    the fiducials.
    '''

    m = (af1zoff-af2zoff)/(af1y-af2y)
    z0 = af1zoff - m*af1y

    # offset the line by the front/back offset + height
    if front:
        return z0 - 3.5 - height + y*m
    else:
        return z0 + height + y*m
    # return the offset intersect


def rotatedx(x0,theta,zoff,xoff=1.88,thoff=1.6):
    '''
    given the x position at 0 rotation (from the image of the sample bar)
    and a rotation angle, the offset of rotation in z and x (as well as a potential theta offset)
    find the correct x position to move to at a different rotation angle
    '''
    return xoff + (x0 - xoff) * np.cos((theta - thoff) * np.pi / 180) - zoff * np.sin((theta - thoff) * np.pi / 180)


def rotatedz(x0,theta,zoff,xoff=1.88,thoff=1.6):
    '''
    given the x position at 0 rotation (from the image of the sample bar)
    and a rotation angle, the offset of rotation in z and x axes (as well as a potential theta offset)
    find the correct z position to move to to keep a particular sample at the same intersection point with X-rays
    '''
    return zoff + (x0 - xoff) * np.sin((theta - thoff) * np.pi / 180) - zoff * np.cos((theta - thoff) * np.pi / 180)


def af_rotation(xfm90,xf0,xf90,xf180):
    '''
    takes the fiducial centers measured in the x direction at -90, 0, 90, and 180 degrees
    and returns the offset in x and z from the center of rotation, as well as the
    unrotated x positon of the fiducial marker.

    the x offset is not expected to vary between loads, and has been measured to be 1.88,
    while the z offset is as the bar flexes in this direction, and will be used to
    map the surface locations of other samples between the fiducials

    '''

    x0 = xf0
    xoff = (xf180+x0)/2
    zoff = (xfm90 - xf90)/2
    return (x0,zoff, xoff)

def find_fiducials():
    thoffset = 1.6
    angles = [-90+thoffset,0+thoffset,90+thoffset,180+thoffset]
    xrange = 3.5
    xnum = 36
    startxss = [[7,3,-3,1.1],[3.84,2.94,.55,1.1]]
    yield from bps.mv(Shutter_enable, 0)
    yield from bps.mv(Shutter_control, 0)
    yield from load_configuration('SAXSNEXAFS')
    Beamstop_SAXS.kind = 'hinted'
    startys = [4,-186.25] # af2 first because it is a safer location
    maxlocs = []
    for startxs,starty in zip(startxss,startys):
        yield from bps.mv(sam_Y,starty,sam_X,startxs[1],sam_Th,0,sam_Z,0)
        yield from bps.mv(Shutter_control, 1)
        yield from bp.rel_scan([Beamstop_SAXS], sam_Y, -1,.5,16)
        yield from bps.mv(Shutter_control, 0)
        maxlocs.append(bec.peaks.max["SAXS Beamstop"][0])
        for startx,angle in zip(startxs,angles):
            yield from bps.mv(sam_X,startx,sam_Th,angle)
            yield from bps.mv(Shutter_control, 1)
            yield from bp.scan([Beamstop_SAXS],sam_X,startx-.5*xrange,startx+.5*xrange,xnum)
            yield from bps.mv(Shutter_control, 0)
            maxlocs.append(bec.peaks.max["SAXS Beamstop"][0])
    return maxlocs # [af2y,af2xm90,af2x0,af2x90,af2x180,af1y,af1xm90,af1x0,af1x90,af1x180]


def rotate_now(theta):
    samp = get_sample_dict()
    samp['angle'] = theta
    rotate_sample(samp)
    yield from load_sample(samp)


def rotate_sample(samp):
    '''
    rotate a sample position to the requested theta position
    the requested sample position is set in the angle metadata (sample['angle'])
    '''
    sanatize_angle(samp) # makes sure the requested angle is translated into a real angle for acquisition
    theta_new = samp['bar_loc']['th']
    x0 = samp['bar_loc']['x0']
    y0 = samp['bar_loc']['y0']
    xoff = samp['bar_loc']['xoff']
    zoff = samp['bar_loc']['zoff']

    newx = rotatedx(x0, theta_new, zoff, xoff=xoff)
    for motor in samp['location']:
        if motor['motor'] is 'x':
            motor['position'] = newx
        if motor['motor'] is 'th':
            motor['position'] = theta_new
        if motor['motor'] is 'y':
            motor['position'] = y0

    # in future, updating y (if the rotation axis is not perfectly along y
    # and z (to keep the sample-detector distance constant) as needed would be good as well
    # newz = rotatedz(newx, th, zoff, af1xoff)


def sample_recenter_sample(samp):
    # the current samp['location'] is correct, the point of this is to make sure the x0 and y0 and incident angles
    # are updated accordingly, because the samp['location'] will generally be recalculated and overwritten next time
    # a sample rotation is requested
    # assume the center of rotation for the sample is already calculated correctly (otherwise correct bar is needed)
    # first record the location
    for loc in samp['location']:
        if loc['motor'] is 'x':
            newrotatedx = loc['position']
        if loc['motor'] is 'y':
            newy = loc['position']
        if loc['motor'] is 'th':
            newangle = loc['position']
    # get the rotation parameters from the metadata
    xoff = samp['bar_loc']['xoff']
    zoff = samp['bar_loc']['zoff']
    # find the x0 location which would result in this new position
    newx0 = rotatedx(newrotatedx, -newangle, zoff, xoff=xoff) # we rotate by the negative angle to get back to x0
    samp['bar_loc']['x0'] = newx0
    samp['bar_loc']['y0'] = newy # y and y0 are the same, so we can just copy this
    samp['angle'] = newangle


def read_positions(bar):
    # for when the positions are altered by hand in the excel sheet, (i.e. after spiral scans)
    # this reads those positions and sets the default positions (x0 and y0) to match
    for samp in bar:
        sample_recenter_sample(samp)