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
- Insert values in .env file, for example:
```bash
SENDER_EMAIL=email_sender@mail.com
PASSWORD_SENDER=psw12345678
RECEVER_EMAIL=email_recever@mail.com
DB_NAME=music_db
DB_USERNAME=postgres
```
    To allow the access, we need to set 'Less Secure App Access' settings in the google account. If the two step verification is on, we cannot use the less secure access.

- Run code.
```bash
python main.py
```
