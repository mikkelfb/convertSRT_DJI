from pickle import TRUE
import re
import string
from datetime import datetime
import csv

from numpy import append


def extract_time_us(time):
    splitted_time = re.split(":", time)
    hour = int(splitted_time[0])
    minutes = int(splitted_time[1])
    comma_part = re.split(",", splitted_time[2])

    if(len(comma_part) > 2):
        seconds = comma_part[0] + '.'
        for dec in comma_part[1:]:
            seconds = seconds + dec
        seconds = float(seconds)
    else:
        seconds = float(re.sub(",", ".", splitted_time[2]))
    seconds_us = int(seconds * 1e6)
    minuts_us = int(minutes * 60 * 1e6)
    hour_us = int(hour * 60 * 60 * 1e6)
    time_us = seconds_us + minuts_us + hour_us
    return time_us


def convertSRT(inFile, outFile, debug=False):
    with open(inFile) as f:
        lines = f.read().splitlines()

    counter = 0

    sampleNR = []
    timeRelt1 = []
    timeRelt2 = []
    FramCNT = []
    diffTime = []
    posixDate = []  # saves the date and time of day in POSIX timeformat in micro seconds
    da = []  # saves the date in normal ISO standard string time format
    timeDate = []  # saves the time of the day in normal ISO standard string time format
    color_md = []
    latitude = []
    longtitude = []
    rel_alt = []
    abs_alt = []
    drone_yaw = []
    drone_Pitch = []
    drone_Roll = []

    for line in lines[0:10]:
        counter = counter + 1
        if counter == 1:
            sampleNR.append(line)
        elif counter == 2:
            times = re.split(" --> ", line)
            timeRelt1.append(extract_time_us(times[0]))
            timeRelt2.append(extract_time_us(times[1]))
        elif counter == 3:
            l3 = re.split(", ", line[16:])
            FramCNT.append(int(re.findall(r'\d+', l3[0])[0]))
            if(l3[1][-1:] == "ms"):
                diffTime.append(int(re.findall(r'\d+', l3[1])[0]) * 1e3)
            elif(l3[1][-1:] == "us"):
                diffTime.append(int(re.findall(r'\d+', l3[1])[0]))
            elif(l3[1][-1:] == "s"):
                diffTime.append(int(re.findall(r'\d+', l3[1])[0]) * 1e3)

        elif counter == 4:
            l4 = re.split(" ", line)
            print(l4)
            dato = datetime.fromisoformat(l4[0])
            dato_posix_us = dato.timestamp() * 1e6
            time_posix_us = extract_time_us(l4[1])
            total_posix_us = dato_posix_us + time_posix_us
            posixDate.append(total_posix_us)
            da.append(l4[0])
            timeDate.append(l4[1])
        elif counter == 5:
            l5 = re.findall('\\[.*?\\]', line)
            color_md.append(re.split(": ", l5[0])[1][:-1])
            latitude.append(float(re.findall('\\d*\\.?\\d+', l5[1])[0]))
            longtitude.append(float(re.findall('\\d*\\.?\\d+', l5[2])[0]))
            rel_alt.append(float(re.findall('\\d*\\.?\\d+', l5[3])[0]))
            abs_alt.append(float(re.findall('\\d*\\.?\\d+', l5[3])[1]))
            drone_yaw.append(
                float(
                    re.findall(
                        r'[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?',
                        l5[4])[0]))
            drone_Pitch.append(
                float(
                    re.findall(
                        r'[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?',
                        l5[4])[1]))
            drone_Roll.append(
                float(
                    re.findall(
                        r'[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?',
                        l5[4])[2]))
        elif counter == 6:
            counter = 0

    with open(outFile, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        for n in range(len(sampleNR)):
            # alter the order of the csv stuff in this line:
            row = [
                FramCNT[n],
                timeRelt1[n],
                timeRelt2[n],
                diffTime[n],
                posixDate[n],
                color_md[n],
                latitude[n],
                longtitude[n],
                rel_alt[n],
                abs_alt[n],
                drone_yaw[n],
                drone_Pitch[n],
                drone_Roll[n]
            ]
            writer.writerow(row)

    if(debug == TRUE):
        print('ReltimeT1', timeRelt1)
        print('ReltimeT2', timeRelt2)
        print('FramCNT', FramCNT)
        print('diffTime', diffTime)
        print('da', da)
        print('timeDate', timeDate)
        print('posixDate', posixDate)
        print('color_md', color_md)
        print('latitude', latitude)
        print('longtitude', longtitude)
        print('rel_alt', rel_alt)
        print('abs_alt', abs_alt)
        print('drone_yaw', drone_yaw)
        print('drone_Pitch', drone_Pitch)
        print('drone_Roll', drone_Roll)


infile = "DJI_0781.SRT"
convertSRT(infile, "test", TRUE)
