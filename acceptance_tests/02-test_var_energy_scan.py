from re_setup import testing_RE_md

print("".join(["=" for _ in range(80)]))
print("Testing scan over variable energy.")
with testing_RE_md(RE):
    uid, = RE(bp.scan([saxs_det, Beamstop_SAXS], en.monoen, 270, 290, 11))
    _ = db[uid].table(fill=True)

print("Completed scan over variable energy.")
print("Check /nsls2/data/sst1/legacy/RSoXS/suitcased_data/users for suitcase unpack.")
print("".join(["=" for _ in range(80)]))


