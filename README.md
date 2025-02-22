# Python Backend API

This is a simple Python Backend API that provides user management functionalities like listing the users, searching, sorting the users by the age and showing the details in the paginated form.

## 1. Setup Instructions

```
git clone https://github.com/HarisBalaji/Python_Backend_API
cd Python_Backend
```

## 2. Install Dependencies
```
pip install -r requirements.txt
```

## 3. Run the application

### Run the Flask Server
```
export FLASK_APP=app.py
flask run
```
The API will be running at [http://127.0.0.1:5000](http://127.0.0.1:5000)

### For POST method, open another terminal and run the following command,
```
curl -X POST -F "file=@users.json" http://127.0.0.1:5000/api/users  
```
This will make post request by sending the users.json file and save the details to the database.

### For GET method,
* To list all users, add the */api/users* endpoint to the link [http://127.0.0.1:5000](http://127.0.0.1:5000) at the end. URL look like [http://127.0.0.1:5000/api/users](http://127.0.0.1:5000/api/users)
* To search for a specific user, append the user_id to the url. URL look like [http://127.0.0.1:5000/api/users/1](http://127.0.0.1:5000/api/users/1)

### For updating the user (PUT method), run this command
```
curl -X PUT http://127.0.0.1:5000/api/users/10 \
    -H "Content-Type: application/json" \
    -d '{"id":"10", "first_name":"Vijaya", "last_name":"Ragavan", "company_name":"HPE", "city":"Los Angeles", "state":"KA", "zip":"45090", "email":"vijayaragav@gmail.com",       
    "web":"http://www.vijayr.com", "age":25}'
```
### For partially updating the user (PATCH method), run the following command
```
curl -X PATCH http://127.0.0.1:5000/api/users/1 \-H "Content-Type: application/json" \-d '{"state":"LA","city":"San Jose"}'
```

### For deleting the user (DELETE method), run the following command
```
curl -X DELETE http://127.0.0.1:5000/api/users/500  <!-- Here 500 indicates the id of the user which we want to delete -->
```

### For getting the user summary,
Type the url [http://127.0.0.1:5000/api/users/summary](http://127.0.0.1:5000/api/users/summary) into the browser to see the results.




