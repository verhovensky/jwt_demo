### JWT Testing project

Features:<br>

* Minimum requirements
* No external packages used for JWT auth
* Access token encoded with HS512 algorithm
* Refresh token passed in cookies with SameSite, secure, HttpOnly params
* Refresh can be made only by corresponding access token
* Refresh token stored as BCRYPT hash in DB **
* Protected endpoint to test against
* Extensible user model
* Async API

### Install
Python >= 3.8
```
pip install -r requirements.txt
```
Rename example.env -> .env <br>
Fill DB details for desired database.<br>
```
source/env/bin activate
python create_models.py
python main.py
```

Refresh and login endpoints:<br>
```
POST http://127.0.0.1:8000/login/
POST http://127.0.0.1:8000/login/refresh
```
Login JSON POST data:<br>
(default user_id = 1)
```json
{"id": "1"}
```

Refresh JSON POST data:<br>
```json
{"id": "1", "refresh_token": "eyJhvmQ..."}
```

Protected user info endpoint:<br>
```
GET http://127.0.0.1:8000/user/<pk:int>
```
<br>
<br>


** This approach contradicts with JWT nature [statelessness](https://jwt.io/introduction/) <br>
Feel free to create an issue or/and pr.