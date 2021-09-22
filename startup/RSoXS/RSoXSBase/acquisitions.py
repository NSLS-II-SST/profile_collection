import datetime
from .alignment import load_sample, load_configuration, avg_scan_time,save_samplesxls
from .configurations import all_out
from operator import itemgetter
from ..RSoXSObjects.slackbot import rsoxs_bot
from ..CommonFunctions.functions import boxed_text,run_report,colored
from .startup import db
from .energyscans import (full_ca_scan_nd,full_carbon_calcium_scan_nd,full_carbon_scan_nd,full_carbon_scan_nonaromatic,
                          full_fluorine_scan_nd,full_nitrogen_scan_nd,full_oxygen_scan_nd,short_calcium_scan_nd,
                          short_carbon_scan_nd,short_carbon_scan_nonaromatic,short_fluorine_scan_nd,
                          short_nitrogen_scan_nd,short_oxygen_scan_nd,short_sulfurl_scan_nd,short_zincl_scan_nd,
                          survey_scan_highenergy,very_short_carbon_scan_nd,very_short_oxygen_scan_nd,
                          veryshort_fluorine_scan_nd,survey_scan_lowenergy,survey_scan_veryhighenergy,
                          survey_scan_verylowenergy,sufficient_carbon_scan_nd,picky_carbon_scan_nd,t_carbon_scan_nd,
                          cdsaxs_scan,custom_rsoxs_scan,focused_carbon_scan_nd,g_carbon_scan_nd)
from .NEXAFSscans import (fly_Oxygen_NEXAFS,fly_Nitrogen_NEXAFS,fly_Fluorine_NEXAFS,fly_Boron_NEXAFS,
                          fixed_pol_rotate_sample_nexafs,fixed_sample_rotate_pol_list_nexafs,
                          fixed_sample_rotate_pol_nexafs,fly_Calcium_NEXAFS,fly_Carbon_NEXAFS,fly_SiliconK_NEXAFS,
                          fly_SiliconL_NEXAFS,fly_SulfurL_NEXAFS,full_Carbon_NEXAFS,normal_incidence_rotate_pol_nexafs)

run_report(__file__)


def run_sample(sam_dict):
    yield from load_sample(sam_dict)
    yield from do_acquisitions(sam_dict["acquisitions"])



def do_acquisitions(acq_list):
    uid = None
    for acq in acq_list:
        yield from load_configuration(acq["configuration"])
        uid = yield from eval(acq["plan_name"] + "(" + acq["arguments"] + ")")
    return uid



def run_bar(
    bar,
    sort_by=["sample_num"],
    dryrun=0,
    rev=[False],
    delete_as_complete=True,
    retract_when_done=False,
    save_as_complete="",
):
    """
    run all sample dictionaries stored in the list bar
    @param bar: a list of sample dictionaries
    @param sort_by: list of strings determining the sorting of scans
                    strings include project, configuration, sample_id, plan, plan_args, spriority, apriority
                    within which all of one acquisition, etc
    @param dryrun: Print out the list of plans instead of actually doing anything - safe to do during setup
    @param rev: list the same length of sort_by, or booleans, wetierh to reverse that sort
    @param delete_as_complete: remove the acquisitions from the bar as we go, so we can automatically start back up
    @param retract_when_done: go to throughstation mode at the end of all runs.
    @param save_as_complete: if a valid path, will save the running bar to this position in case of failure
    @return:
    """

    config_change_time = 120  # time to change between configurations, in seconds.
    save_to_file = False
    try:
        open(save_as_complete, "w")
    except OSError:
        save_to_file = False
        pass
    else:
        save_to_file = True

    list_out = []
    for samp_num, s in enumerate(bar):
        sample = s
        sample_id = s["sample_id"]
        sample_project = s["project_name"]
        for acq_num, a in enumerate(s["acquisitions"]):
            if "priority" not in a.keys():
                a["priority"] = 50
            list_out.append(
                [
                    sample_id,  # 0  X
                    sample_project,  # 1  X
                    a["configuration"],  # 2  X
                    a["plan_name"],  # 3
                    avg_scan_time(a["plan_name"], 50),  # 4 calculated plan time
                    sample,  # 5 full sample dict
                    a,  # 6 full acquisition dict
                    samp_num,  # 7 sample index
                    acq_num,  # 8 acq index
                    a["arguments"],  # 9  X
                    s["density"],  # 10
                    s["proposal_id"],  # 11 X
                    s["sample_priority"],  # 12 X
                    a["priority"],
                ]
            )  # 13 X
    switcher = {
        "sample_id": 0,
        "project": 1,
        "config": 2,
        "plan": 3,
        "plan_args": 9,
        "proposal": 11,
        "spriority": 12,
        "apriority": 13,
        "sample_num": 7,
    }
    # add anything to the above list, and make a key in the above dictionary,
    # using that element to sort by something else
    try:
        sort_by.reverse()
        rev.reverse()
    except AttributeError:
        if isinstance(sort_by, str):
            sort_by = [sort_by]
            rev = [rev]
        else:
            print(
                "sort_by needs to be a list of strings\n"
                "such as project, configuration, sample_id, plan, plan_args, spriority, apriority"
            )
            return
    try:
        for k, r in zip(sort_by, rev):
            list_out = sorted(list_out, key=itemgetter(switcher[k]), reverse=r)
    except KeyError:
        print(
            "sort_by needs to be a list of strings\n"
            "such as project, configuration, sample_id, plan, plan_args, spriority, apriority"
        )
        return
    if dryrun:
        text = ""
        total_time = 0
        for i, step in enumerate(list_out):
            text += "load {} from {}, config {}, run {} (p {} a {}), starts @ {} takes {}\n".format(
                step[5]["sample_name"],
                step[1],
                step[2],
                step[3],
                step[12],
                step[13],
                time_sec(total_time),
                time_sec(step[4]),
            )
            total_time += step[4]
            if step[2] != list_out[i - 1][2]:
                total_time += config_change_time
        text += (
            f"\n\nTotal estimated time including config changes {time_sec(total_time)}"
        )
        boxed_text("Dry Run", text, "lightblue", width=120, shrink=True)
    else:
        run_start_time = datetime.datetime.now()
        for i, step in enumerate(list_out):
            time_remaining = sum([avg_scan_time(row[3]) for row in list_out[i:]])
            this_step_time = avg_scan_time(step[3])
            start_time = datetime.datetime.now()
            total_time = datetime.datetime.now() - run_start_time
            boxed_text(
                "Scan Status",
                "\nTime so far: {}".format(str(total_time))
                + "\nStarting scan {} out of {}".format(
                    colored(f"#{i + 1}", "blue"), len(list_out)
                )
                + "{} of {} in project {} Proposal # {}\n which should take {}\n".format(
                    colored(step[3], "blue"),  # plan
                    colored(step[0], "blue"),  # sample_id
                    colored(step[1], "blue"),  # project
                    colored(step[11], "blue"),  # proposal
                    time_sec(this_step_time),
                )
                + f"time remaining approx {time_sec(time_remaining)} \n\n",
                "red",
                width=120,
                shrink=True,
            )
            rsoxs_bot.send_message(
                f"Starting scan {i + 1} out of {len(list_out)}\n"
                + f"{step[3]} of {step[0]} in project {step[1]} Proposal # {step[11]}"
                f"\nwhich should take {time_sec(this_step_time)}"
                + f"\nTime so far: {str(total_time)}"
                f"time remaining approx {time_sec(time_remaining)}"
            )
            yield from load_configuration(step[2])  # move to configuration
            yield from load_sample(step[5])  # move to sample / load sample metadata
            yield from do_acquisitions(
                [step[6]]
            )  # run acquisition (will load configuration again)
            uid = db[-1].uid
            print(f"acq uid = {uid}")
            scan_id = db[uid].start["scan_id"]
            timestamp = db[uid].start["time"]
            success = db[uid].stop["exit_status"]
            bar[step[7]].setdefault("acq_history", []).append(
                {
                    "uid": uid,
                    "scan_id": scan_id,
                    "acq": step[6],
                    "time": timestamp,
                    "status": success,
                }
            )
            if delete_as_complete:
                bar[step[7]]["acquisitions"].remove(step[6])
            if save_to_file:
                save_samplesxls(bar, save_as_complete)
            elapsed_time = datetime.datetime.now() - start_time
            rsoxs_bot.send_message(
                f"Acquisition {scan_id} complete. Actual time : {str(elapsed_time)},"
            )
        rsoxs_bot.send_message("All scans complete!")
        if retract_when_done:
            yield from all_out()


def time_sec(seconds):
    dt = datetime.timedelta(seconds=seconds)
    return str(dt).split(".")[0]
