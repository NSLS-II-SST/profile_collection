run_report(__file__)
# load RSoXS stuff into the monitors

sd.monitors.extend([Shutter_control,
                    mono_en.readback,
                    ring_current,
                    Beamstop_WAXS,
                    Beamstop_SAXS,
                    Izero_Mesh,
                    Sample_TEY,
                    ])