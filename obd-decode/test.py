import subprocess
outfilename="output-2019-10-25_20-29-38.h264"
encoded_filename="output_test2.mp4"
subprocess.run(["MP4Box", "-add", outfilename, "-fps", "40", encoded_filename])

