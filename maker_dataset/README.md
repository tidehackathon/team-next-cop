# Maker Dataset

#### Code for creating dataset from drone video. Result: drone image == image from satellite map

File `log_reader` - parse log.file of drone for receive: number of frame with coordinates. Return `dict` 

File `video_reader` - cuts video into frames (you can set the step between frames). For each frame from the drone, it generates a request to `Google api` based on information from the log file (which we get from `log_reader`). Receives in response an image from Google maps. Saves the image

It is also worth noting that for each frame from the drone, the function generates 5 frames from Google maps with an up-down-right-left shift and the original.

## Dependencies
`python 3.10`

`GOOGLE_API_KEY`


## Usage

```python
if __name__ == '__main__':
    path_to_log = "PATH/TO/LOG.SRT"
    log_info = log_proccesing(path_to_log)
    path_to_video = "PATH/TO/VIDEO.MP4"
    path_dron = 'PATH/TO/DRONE_IMAGES/SAVE'
    path_map = 'PATH/TO/MAPS_IMAGES/SAVE'
    apiKey = "GOOGLE_API_KEY"
    video_proccesing(log_info, path_to_video, path_dron, path_map,apiKey)
```


## Run
Clone the project

```bash
  git clone https://github.com/tidehackathon/team-next-cop.git
```

Go to the project directory

```bash
  cd team-next-cop/maker_dataset
```
Create enviroment

```bash
  python3 -m venv env
```

Install dependencies

```bash
  pip install -r req.txt
```

Command for start

```bash
  python video_reader.py
```

