import re

path_to_video = "D:\\100MEDIA\\DJI_0006.SRT"
re_id = r"[\d]"
cadr_id = 0
coordinate = dict()

def log_proccesing(path):
    with open(path, 'r') as f:
        while True:
            line = f.readline()
            if len(line)==0:
                break
            
            line = line.replace('\n', '')
            if len(re.findall(re_id,line)) == len(line) and len(line) != 0:
                cadr_id = line
            if 'latitude' in line:
                latitude = line.split('latitude: ')[1].split(']')[0]
                longitude = line.split('longitude: ')[1].split(']')[0]
                altitude = line.split('altitude: ')[1].split(']')[0]
                coordinate.update({cadr_id : {'latitude': latitude, 'longitude': longitude, 'altitude': altitude}})

        return coordinate

