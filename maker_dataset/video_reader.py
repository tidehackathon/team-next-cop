# import requests
import cv2
import requests
from log_reader import log_proccesing


def video_proccesing(log_info, path_to_video, path_dron, path_map):
    cam = cv2.VideoCapture(path_to_video)

    # frame
    currentframe = 1

    while (True):
        # reading from frame
        ret, frame = cam.read()
        if currentframe % 100 == 0:

            if ret:
                # if video is still left continue creating images
                name = f'{path_dron}dron_{str(currentframe)}.png'
                print('Creating...' + name)

                # writing the extracted images
                cv2.imwrite(name, frame)
            
                # Getting google map pic
                latitude = log_info[str(currentframe)]['latitude']
                longitude = log_info[str(currentframe)]['longitude']
                for i in range(5):
                    if i == 0:
                        lat = latitude
                        lon = longitude
                    if i == 1:
                        lat = float(latitude) + 0.00001
                        lon = float(longitude)
                    elif i == 2:
                        lat = float(latitude) - 0.00001
                        lon = float(longitude)
                    elif i == 3:
                        lat = float(latitude)
                        lon = float(longitude) - 0.00001
                    elif i == 4:
                        lat = float(latitude)
                        lon = float(longitude) + 0.00001
                    apiKey = "AIzaSyBGeJsMbrNEkYTbSaLkSS6K84xk-TO_8ys"

                    reqLink = f'https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&scale=2&format=png&zoom=17&size=640x360&maptype=satellite&key={apiKey}'
                    img_data = requests.get(reqLink).content
                    with open(f'{path_map}map_{str(currentframe)}_{i}.png', 'wb') as handler:
                        handler.write(img_data)

                currentframe += 1
            else:
                break
        currentframe += 1


    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    path_to_log = "D:\\100MEDIA\\DJI_0006.SRT"
    log_info = log_proccesing(path_to_log)
    path_to_video = "D:\\100MEDIA\\DJI_0006.MP4"
    path_dron = 'D:\\DronPic\\'
    path_map = 'D:\\MapPic\\'
    video_proccesing(log_info, path_to_video, path_dron, path_map)