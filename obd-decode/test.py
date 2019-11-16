import datetime
import subprocess

timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
outfilename="output-2019-11-15_17-36-47.h264"
encoded_filename="output-"+timestamp+".mp4"
subprocess.run(["MP4Box", "-add", outfilename, "-fps", "40", encoded_filename])

