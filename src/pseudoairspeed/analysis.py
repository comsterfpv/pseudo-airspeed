import math
import pandas
import enum
from pandas import DataFrame
import matplotlib.pyplot as plt

# Gravitational constant in m/s^2
g = 9.807

class Units(enum.Enum):
    KM_PER_HOUR = enum.auto()
    M_PER_SECOND = enum.auto()

    def mps_factor(self):
        if self is self.KM_PER_HOUR:
            return 3.6 # = 60 * 60 / 1000
        else:
            return 1.

def pseudo(flight_data_df, mass, ke, kd, v0, dt=1./25, release_frame=0, units=Units.KM_PER_HOUR):
    """Return a dataframe of pseudo airspeed and angle given an input dataframe with watts and rise

    Parameters
    ----------
    flight_data_df: pandas.DataFrame
        Must have frame, rise, and watts columns containing int, float, float
    mass: float
        Mass of aircraft in kg
    ke: float
        Constant efficiency factor of drivetrain for converting electrical input to forward motion,
        with perfect efficiency = 1.0
    kd: float
        Drag coefficient, 145 / 10000 seems reasonable for a ~1kg flying wing
    v0: float
        Initial velocity, eg, may be nonzero launched into a headwind
    dt: float
        Timestep between frames in seconds
    release_frame: int
        Frame number for start of free flight, before which velocity is calculated as v0
    units: Units
        Specify units for airspeed columns in return dataframe, with kph as default althgouh mps is natural

    Returns
    -------
    pandas.DataFrame
        An output DataFrame with pseudo and angle columns

    """

    subdf = flight_data_df[['frame', 'rise', 'watts']].copy().dropna(axis=0)
    vser = subdf['frame'] * 0.
    vser.name = 'pseudo'
    vser[subdf.index[0]] = v0
    alpha = vser.copy()
    alpha.name = 'angle'

    v_min = 1.

    for j, j_prev in zip(vser.index[1:], vser.index[:-1]):
        v = vser[j_prev]
        W = subdf.loc[j_prev, 'watts']
        sin_a = min(1, max(-1, subdf.loc[j_prev, 'rise'] / max(v, v_min)))
        f, f_prior = subdf.loc[j, 'frame'], subdf.loc[j_prev, 'frame']
        deltav_over_deltat = 1/mass * (ke * W / max(v_min, v) - kd * v * v) - g * sin_a
        deltat = dt * (f - f_prior)
        vser[j] = max(v + deltav_over_deltat * deltat, v_min) if j > release_frame else v0
        alpha[j] = math.asin(sin_a) * 180 / math.pi
    return DataFrame([vser * units.mps_factor(), alpha]).T

def load(csv_filename):
    """

    Parameters
    ----------
    csv_filename : str
        Name of flight data csv in filesystem. Must have voltage, amps, rise, frame columns

    Returns
    -------
    df : pandas.DataFrame
        Loaded flight data

    """
    df = pandas.read_csv(csv_filename)
    for col in ['amps', 'rise']:
        df[col] = pandas.to_numeric(df[col], errors='coerce')
    df['watts'] = df['amps'] * df['voltage']    
    df['throttle'] = df['amps'] / df['amps'].max()
    return df
