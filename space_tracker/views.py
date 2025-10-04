from django.shortcuts import render
import datetime
import requests
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from sgp4.api import Satrec, jday

TLE_FEED = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

# helper: fetch TLEs (returns list of tuples: (name, line1, line2))
def fetch_tles(limit=200):
    try:
        text = requests.get(TLE_FEED, timeout=10).text.strip().splitlines()
    except Exception:
        return []
    # TLEs are 3 lines: name, l1, l2
    tles = []
    for i in range(0, len(text) - 2, 3):
        tles.append((text[i].strip(), text[i+1].strip(), text[i+2].strip()))
        if len(tles) >= limit:
            break
    return tles

# helper: propagate a Satrec to current ECI position (km)
def sat_ecipos(satrec, when=None):
    if when is None:
        when = datetime.datetime.utcnow()
    jd, fr = jday(when.year, when.month, when.day, when.hour, when.minute, when.second + when.microsecond * 1e-6)
    err, r, v = satrec.sgp4(jd, fr)
    if err != 0:
        raise RuntimeError(f"prop error code {err}")
    return np.array(r)  # km

# template view
def tracker_ui(request):
    return render(request, 'space_tracker/index.html')

# API: current satellite positions (limited count)
def api_satellites(request):
    limit = int(request.GET.get('limit', 200))
    tles = fetch_tles(limit=limit)
    out = []
    for name, l1, l2 in tles:
        try:
            sat = Satrec.twoline2rv(l1, l2)
            r = sat_ecipos(sat)
            out.append({'name': name, 'x': float(r[0]), 'y': float(r[1]), 'z': float(r[2])})
        except Exception:
            continue
    return JsonResponse(out, safe=False)

# API: simple proximity alerts (pairwise check for this snapshot)
def api_alerts(request):
    # distance threshold in km (default 5 km)
    threshold = float(request.GET.get('th', 5.0))
    limit = int(request.GET.get('limit', 200))
    tles = fetch_tles(limit=limit)
    sats = []
    for name, l1, l2 in tles:
        try:
            sat = Satrec.twoline2rv(l1, l2)
            r = sat_ecipos(sat)
            sats.append((name, r))
        except Exception:
            continue

    alerts = []
    # naive O(n^2) check — fine for a few hundred objects
    for i in range(len(sats)):
        for j in range(i+1, len(sats)):
            d = np.linalg.norm(sats[i][1] - sats[j][1])
            if d <= threshold:
                alerts.append({'sat1': sats[i][0], 'sat2': sats[j][0], 'distance_km': float(round(d, 3))})
    return JsonResponse(alerts, safe=False)
