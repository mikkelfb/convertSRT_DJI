from pickle import FALSE
import srtConverter
infile = "DJI_0781.SRT"
outfile = "test.csv"

srtConverter.convertSRT(infile, outfile, debug=FALSE)
