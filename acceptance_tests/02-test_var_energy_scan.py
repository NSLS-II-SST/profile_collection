from re_setup import testing_RE_md

print("".join(["=" for _ in range(80)]))
print("Testing scan over variable energy.")
with testing_RE_md(RE):
    uid, = RE(bp.scan([saxs_det, Beamstop_SAXS], en.monoen, 270, 290, 11))
    _ = db[uid].table(fill=True)

print("Completed scan over variable energy.")
print("Check the following for suitcase unpack.\n"
      "/nsls2/data/sst/legacy/RSoXS/suitcased_data/users/test-cycle/acceptance_test-NSLS2/auto/acceptance_test/...")
print("".join(["=" for _ in range(80)]))


