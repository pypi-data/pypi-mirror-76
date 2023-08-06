import mne


class Utils:
    MONTAGE_TYPES = {
        "standard_1005": "Electrodes are named and positioned according to the international 10-05 system (343+3 locations)",
        "standard_1020": "Electrodes are named and positioned according to the international 10-20 system (94+3 locations)",
        "standard_alphabetic": "Electrodes are named with LETTER-NUMBER combinations (A1, B2, F4, …) (65+3 locations)",
        "standard_postfixed": "Electrodes are named according to the international 10-20 system using postfixes for intermediate positions (100+3 locations)",
        "standard_prefixed": "Electrodes are named according to the international 10-20 system using prefixes for intermediate positions (74+3 locations)",
        "standard_primed": "Electrodes are named according to the international 10-20 system using prime marks (‘ and ‘’) for intermediate positions (100+3 locations)",
        "biosemi16": "BioSemi cap with 16 electrodes (16+3 locations)",
        "biosemi32": "BioSemi cap with 32 electrodes (32+3 locations)",
        "biosemi64": "BioSemi cap with 64 electrodes q(64+3 locations)",
        "biosemi128": "BioSemi cap with 128 electrodes (128+3 locations)",
        "biosemi160": "BioSemi cap with 160 electrodes (160+3 locations)",
        "biosemi256": "BioSemi cap with 256 electrodes (256+3 locations)",
        "easycap-M1": "EasyCap with 10-05 electrode names (74 locations)",
        "easycap-M10": "EasyCap with numbered electrodes (61 locations)",
        "EGI_256": "Geodesic Sensor Net (256 locations)",
        "GSN-HydroCel-32": "HydroCel Geodesic Sensor Net and Cz (33+3 locations)",
        "GSN-HydroCel-64_1.0": "HydroCel Geodesic Sensor Net (64+3 locations)",
        "GSN-HydroCel-65_1.0": "HydroCel Geodesic Sensor Net and Cz (65+3 locations)",
        "GSN-HydroCel-128": "HydroCel Geodesic Sensor Net (128+3 locations)",
        "GSN-HydroCel-129": "HydroCel Geodesic Sensor Net and Cz (129+3 locations)",
        "GSN-HydroCel-256": "HydroCel Geodesic Sensor Net (256+3 locations)",
        "GSN-HydroCel-257": "HydroCel Geodesic Sensor Net and Cz (257+3 locations)",
        "mgh60": "The (older) 60-channel cap used at MGH (60+3 locations)",
        "mgh70": "The (newer) 70-channel BrainVision cap used at MGH (70+3 locations)"
        }

    FIF_RAW_EXTENSION = '-raw.fif'
    FIF_EPOCHS_EXTENSION = '-epo.fif'
    FIF_EVOKEDS_EXTENSION = '-ave.fif'

    @staticmethod
    def find_events_and_count(raw_data):
        event_ids = None

        try:
            events = mne.find_events(raw_data, shortest_event=1)
        except:
            events, event_ids = mne.events_from_annotations(raw_data)

        return events, event_ids, Utils.find_count(events, event_ids)

    @staticmethod
    def find_count(events, event_ids):
        event_ids_count = {}

        for index in event_ids:
            event_ids_count[event_ids[index]] = 0

        for index in range(len(events)):
            event_id = events[index][2]
            event_ids_count[event_id] += 1

        return event_ids_count

    @staticmethod
    def format_annotation(index, event_ids, event_ids_count):
        # Format show name of the stimul plus appearance count, e.g., Stimul [30x]
        return f"{index} [{event_ids_count[event_ids[index]]}x]"
