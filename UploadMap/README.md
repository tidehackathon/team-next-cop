# Upload Map

#### Code for uploading map to drone

File `uploadmap` - downloads satellite photos of google maps for mapping and obtaining coordinates from them. using two opposite points of the required area, for example  1st -`50.425386  30.702002`  2nd - `50.426786 30.701002`

It is also worth noting that for each frame from the drone, the function generates 5 frames from Google maps with an up-down-right-left shift and the original.



## Dependencies
`python 3.10`

`GOOGLE_API_KEY`

## Usage

```python
apiKey = "GOOGLE_API_KEY"
```


## Run
Clone the project

```bash
  git clone https://github.com/tidehackathon/team-next-cop.git
```

Go to the project directory

```bash
  cd team-next-cop/UploadMap
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
  python uploadMap.py
```

