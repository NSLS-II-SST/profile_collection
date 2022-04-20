from copy import deepcopy


class testing_RE_md:
    def __init__(self, RE):
        self.RE = RE
        self.pre_test_md = deepcopy(self.RE.md)

    @property
    def _md(self):
        return {
            "RSoXS_SAXS_BCY": None,
            "user_email": "egann@bnl.gov",
            "sample_id": "test",
            "location": [],
            "institution": "NSLS2",
            "composition": "",
            "grazing": 0,
            "scan_id": 0,
            "RSoXS_Config": "WAXS",
            "density": "",
            "project_id": "",
            "RSoXS_WAXS_BCY": 543.18,
            "acquisitions": [],
            "SAF_id": "306821",
            "front": 1,
            "exptime": 1,
            "RSoXS_SAXS_SDD": None,
            "sample_desc": "test of bluesky",
            "notes": "testing",
            "angle": 180,
            "project_desc": "testing bluesky",
            "height": 0.2,
            "saf_id": "308705",
            "user_name": "Eliot",
            "cycle": "test-cycle",
            "num_intervals": 35,
            "sample_set": "testing",
            "thickness": "",
            "RSoXS_Main_DET": "WAXS",
            "num_points": 36,
            "proposal_id": "acceptance_test",
            "RSoXS_SAXS_BCX": None,
            "beamline_id": "SST-1 RSoXS",
            "sample_priority": "",
            "sample_date": "2022-03-21 00:00:00",
            "components": "",
            "sample_state": "new",
            "RSoXS_WAXS_SDD": 38.4,
            "samp_user_id": "",
            "sample_name": "test",
            "RSoXS_WAXS_BCX": 394.84,
            "bar_spot": "14A",
            "user_start_date": "2022-02-04",
            "SAXS_Mask": [[473, 472], [510, 471], [515, 1024], [476, 1024]],
            "bar_loc": { },
            "user_id": "0",
            "chemical_formula": "",
            "project_name": "acceptance_test",
            "acq_history": [],
        }

    def __enter__(self):
        self.RE.md.update(self._md)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.RE.md = self.pre_test_md
