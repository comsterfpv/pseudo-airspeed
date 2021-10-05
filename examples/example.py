from pseudoairspeed.analysis import pseudo, load
import argparse
import os
import pandas

# source: https://www.youtube.com/watch?v=_2XDyqGhHI0
csv_fn = os.path.join('..', 'data', 'flight_pawel_wing_2017.09.csv')

def main():
    p = argparse.ArgumentParser(description='Example function to analyze pseudo airspeed from flight data')
    p.add_argument('input', default=csv_fn, nargs='?', help='Input csv filename')
    p.add_argument('--mass', default=1.3, help='mass of aircraft in kg')
    p.add_argument('--ke', default=0.75, help='coefficient of drivetrain efficiency, max 1')
    p.add_argument('--kd', default=145 / 10000, help='coefficient of drag')
    p.add_argument('--v0', default=0., help='Initial airspeed, eg, nonzero in case of a headwind')
    p.add_argument('--dt', default=1. / 25, help='Time between frames in seconds')
    p.add_argument('--release_frame', default=0, help='Frame number of release for launch')
    p.add_argument('--write', action='store_true')
    p.add_argument('--output', default='out.png', help='name of output plot')
    p.add_argument('--columns', nargs='*', default=['airspeed', 'pseudo'], help='columns to plot')
    p.add_argument('--right', nargs='*', default=[], help='columns to plot with values on right axis')
    p.add_argument('--height', type=float, default=3.)
    p.add_argument('--width', type=float, default=4.)
    args = p.parse_args()

    in_df = load(args.input)
    out_df = pseudo(in_df, mass=args.mass, dt=args.dt, ke=args.ke, kd=args.kd, v0=args.v0, release_frame=args.release_frame)

    if args.write:
        df = pandas.concat([in_df, out_df], axis=1)
        p = df[args.columns].plot(secondary_y=args.right, figsize=(args.width, args.height))
        fig = p.get_figure()
        fig.savefig(args.output)

if __name__ == '__main__':
    main()    
