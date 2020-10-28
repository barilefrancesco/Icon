# Music Advisor

* [What is Music Advisor?](#What-is-Music-Advisor?)
* [Tools](#tools)
* [Use cases](#use-cases)
* [Requirements](#requirements)
* [Developer Setup](#developer-setup)

## What is Music Advisor?
- The advanced system allows to generate similar artists'charts and playlists based on the user's musical preferences, defined by their most listened artists and albums, through studying the genres of the latters, all by synchronising their spotify account.

---

### Tools:
- Python
- PostgreSQL

---

### Use cases:
- Request the addition of an artist in the database via email.
- Request the addition of an album in the database via email.
- Get similar artist list.
- Get playlist based on prefer genres.
- Get playlists based on preferred genres.
- Export playlists to Spotify account.

---

### Requirements:
- Python 3.7
- PIP 
- PostgreSQL

---

### Developer Setup:
- Fork this repository, and cd into it.
```bash
git clone https://github.com/barilefrancesco/icon.git
cd icon/
```
- Create and activate your virtual environment.
    - MacOS/Linux:
    ```bash
    virtualenv --no-site-packages env
    source env/bin/activate
    ```
    - Windows:
    ```
    virtualenv env
    .\env\Scripts\activate
    ```
- Install requisite python packages and modules.
```bash
pip install -r requirements.txt
```
- Run code.
```bash
python main.py
```
