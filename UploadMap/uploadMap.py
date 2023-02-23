import requests
import io
import os
from alive_progress import alive_bar


def generate_point(coordinate_x: list, coordinate_y: list, step: float):
    lat_x, lon_x = coordinate_x[0], coordinate_x[1]
    lat_y, lon_y = coordinate_y[0], coordinate_y[1]
    round_value = len(str(lat_x).split('.')[1])
    lat_points = list()
    lon_points = list()
    full_points_list = list()
    # Generete all lat point
    if lat_x > lat_y:
        while lat_x > lat_y:
            lat_x = round(lat_x - step, round_value)
            lat_points.append(lat_x)
    else:
        while lat_x < lat_y:
            lat_y = round(lat_y - step, round_value)
            lat_points.append(lat_y)

    # Generete all lon point
    if lon_x > lon_y:
        while lon_x > lon_y:
            lon_x = round(lon_x - step, round_value)
            lon_points.append(lon_x)
    else:
        while lon_x < lon_y:
            lon_y = round(lon_y - step, round_value)
            lon_points.append(lon_y)

    for i in lat_points:
        for j in lon_points:
            full_points_list.append([i, j])

    return full_points_list


if __name__ == '__main__':
    # # PointOne PontTo Step

    # First point
    lat_x = 50.433218
    lat_y = 50.411217

    # Second point
    lon_x = 30.672181
    lon_y = 30.726325


    # Step
    step = 0.0005

    

    answer = generate_point(coordinate_x=[lat_x, lon_x], coordinate_y=[lat_y, lon_y], step=step)
    apiKey = "AIzaSyBGeJsMbrNEkYTbSaLkSS6K84xk-TO_8ys"
    os.makedirs('./MAP', exist_ok=True)

    with alive_bar(len(answer), dual_line=True, title='AIRAI') as bar:
        # geting fotoo for map
        for geo in answer:
            lat = geo[0]
            lon = geo[1]
            reqLink = f'https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&scale=2&format=png&zoom=17&size=640x360&maptype=satellite&key={apiKey}'
            img_data = requests.get(reqLink).content
            with io.open(f'MAP/{lat}-{lon}.png', 'wb') as handler:
                handler.write(img_data)
            bar.text = f'-> Download file: {lat} - {lon}, please wait... '
            bar()
