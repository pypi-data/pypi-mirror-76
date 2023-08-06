from datetime import datetime, timedelta, timezone
from .orbitalpass import OrbitalPass
from skyfield.api import Topos, \
                         Loader, \
                         EarthSatellite


VALIDATE_TIME_TOLERENCE_S = 5.0


def overlap(pass_b, pass_a):
    """
    Check to see if two passes overlap.

    Parameters
    ----------
    pass_a : OrbitalPass
        A OrbitalPass objects to check.
    pass_b : OrbitalPass
        A OrbitalPass objects to check.

    Returns
    -------
    bool
        True if passes overlaps or False if no overlap
    """
    ret = False

    if (pass_a.aos_utc <= pass_b.aos_utc
            and pass_a.los_utc >= pass_b.aos_utc)\
            or (pass_a.aos_utc <= pass_b.los_utc
                and pass_a.los_utc >= pass_b.los_utc):
        ret = True

    return ret


def pass_overlap(new_pass: OrbitalPass,
                 approved_passes: [OrbitalPass]) -> bool:
    """Checks to see if the possible pass will overlap with an existing
    approved pass.

    Parameters
    ----------
    new_passes : OrbitalPass
        The new OrbitalPass objects to check.
    approved_passes : [OrbitalPass]
        List of existing approved OrbitalPass objects to check against.

    Returns
    -------
    bool
        True if pass overlaps with an existing approved pass or False if no
        overlap
    """

    available = False

    if approved_passes is None:
        return available  # nothing to check

    for ap in approved_passes:
        """
        Check to see if the end of the possible pass overlaps with start of
        the approved pass and also check to if the start of the possible pass
        overlaps with end of the approved pass
        """
        if (new_pass.aos_utc <= ap.aos_utc and
                new_pass.los_utc >= ap.aos_utc)\
                or (new_pass.aos_utc <= ap.los_utc
                    and new_pass.los_utc >= ap.los_utc):
            available = True  # pass overlap with an approved pass
            break  # no reason to check against any other approved passes

    return available


def get_all_passes(tle: [str],
                   lat_deg: float,
                   long_deg: float,
                   start_datetime_utc: datetime,
                   end_datetime_utc: datetime,
                   approved_passes: [OrbitalPass] = None,
                   elev_m: float = 0.0,
                   horizon_deg: float = 0.0,
                   min_duration_s: int = 0) -> [OrbitalPass]:
    """
    Get a list of all passes for a satellite and location for a time span.

    Wrapper for Skyfield TLE ground station pass functions that produces an
    OrbitalPass object list of possible passes.

    Parameters
    ----------
    tle : [str]
        Can be [tle_line1, tle_line2] or [tle_header, tle_line1, tle_line2]
    lat_deg : float
        latitude of ground station in degrees
    long_deg : float
        longitude of ground station in degrees
    start_datetime_utc : datetime
        The start datetime wanted.
    end_datetime_utc : datetime
        The end datetime wanted.
    approved_passes : [OrbitalPass]
        A list of OrbitalPass objects for existing approved passes.
    elev_m : float
        elevation of ground station in meters
    horizon_deg : float
        Minimum horizon degrees
    min_duration_s : int
        Minimum duration wanted

    Raises
    ------
    ValueError
        If the tle list is incorrect.

    Returns
    -------
    [OrbitalPass]
        A list of OrbitalPass.
    """

    pass_list = []

    load = Loader('/tmp', verbose=False)
    ts = load.timescale()
    t0 = ts.utc(start_datetime_utc.replace(tzinfo=timezone.utc))
    t1 = ts.utc(end_datetime_utc.replace(tzinfo=timezone.utc))

    # make topocentric object
    loc = Topos(lat_deg, long_deg, elev_m)
    loc = Topos(latitude_degrees=lat_deg,
                longitude_degrees=long_deg,
                elevation_m=elev_m)

    # make satellite object from TLE
    if len(tle) == 2:
        satellite = EarthSatellite(tle[0], tle[1], "", ts)
    elif len(tle) == 3:
        satellite = EarthSatellite(tle[1], tle[2], tle[0], ts)
    else:
        raise ValueError("Invalid tle string list\n")

    # find all events
    t, events = satellite.find_events(loc, t0, t1, horizon_deg)

    # make a list of datetimes for passes
    for x in range(0, len(events)-3, 3):
        aos_utc = t[x].utc_datetime()
        los_utc = t[x+2].utc_datetime()
        duration_s = (los_utc - aos_utc).total_seconds()

        if duration_s > min_duration_s:

            new_pass = OrbitalPass(gs_latitude_deg=lat_deg,
                                   gs_longitude_deg=long_deg,
                                   aos_utc=aos_utc.replace(tzinfo=None),
                                   los_utc=los_utc.replace(tzinfo=None),
                                   gs_elevation_m=elev_m,
                                   horizon_deg=horizon_deg)

            if not pass_overlap(new_pass, approved_passes):
                pass_list.append(new_pass)  # add pass to list
    return pass_list


def validate_pass(tle: [str], orbital_pass: OrbitalPass) -> bool:
    """
    Checks to see if all data in the OrbitalPass args is valid pass.

    Parameters
    ----------
    tle : [str]
        Can be [tle_line1, tle_line2] or [tle_header, tle_line1, tle_line2]
    orbital_pass : OrbitalPass
        The pass to validate.

    Returns
    -------
    bool
        True if valid and False if invalid.
    """

    # Add a decent buffer so skyfeild can run.
    aos_utc_tolerence = orbital_pass.aos_utc - timedelta(hours=2)
    los_utc_tolerence = orbital_pass.los_utc + timedelta(hours=2)

    pass_list = get_all_passes(tle,
                               orbital_pass.gs_latitude_deg,
                               orbital_pass.gs_longitude_deg,
                               aos_utc_tolerence,
                               los_utc_tolerence,
                               elev_m=orbital_pass.gs_elevation_m,
                               horizon_deg=orbital_pass.horizon_deg)

    for p in pass_list:
        aos_diff_s = abs((p.aos_utc - orbital_pass.aos_utc).total_seconds())
        los_diff_s = abs((p.los_utc - orbital_pass.los_utc).total_seconds())

        if aos_diff_s < VALIDATE_TIME_TOLERENCE_S and \
                los_diff_s < VALIDATE_TIME_TOLERENCE_S:
            return True  # valid pass
    return False  # invalid pass
