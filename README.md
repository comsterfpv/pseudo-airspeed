# pseudo-airspeed
Some analysis of flight data to infer a pseudo airspeed

## Purpose
This contains a csv with sample flight data scraped from the OSD in a YouTube video as well
as python code to model the airspeed based on the flight data

## Reference
Flight data is from https://www.youtube.com/watch?v=_2XDyqGhHI0

This video was automatically processed to generate the included flight data. Many fixes and manual adjustments
were necessary to make it usable, and it surely has many inaccuracies compared to the original video.

## Example
You can use the example script to generate plots with these instructions, so long as you
have a functioning Python 3.x with the pandas package.

1. Change to the src directory
2. Run the example script with the local directory added to your path like this in a bash shell.

PYTHONPATH=${PYTHONPATH}:. python ../examples/example.py --write --columns airspeed pseudo angle --right angle

3. Find your output png name out.png
