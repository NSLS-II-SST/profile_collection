from re_setup import testing_RE_md

print("".join(["=" for _ in range(80)]))
print("Changing PVs to test scan with high data frequency.")

npnts = diode_i400_npnts.get()
update_time = Izero_update_time.get()

with testing_RE_md(RE):
    diode_i400_npnts.set(500)
    Izero_update_time.set(0.2)
    uid, = RE(bp.scan([saxs_det, Beamstop_SAXS], en.monoen, 270, 290, 11))
    _ = db[uid].table(fill=True)

diode_i400_npnts.set(npnts)
Izero_update_time.set(update_time)
print("Completed high data frequency scan over variable energy.")
print("Check the following for suitcase unpack.\n"
      "/nsls2/data/sst/legacy/RSoXS/suitcased_data/users/test-cycle/acceptance_test-NSLS2/auto/acceptance_test/...")
print("".join(["=" for _ in range(80)]))