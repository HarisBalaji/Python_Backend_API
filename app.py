from flask import Flask, json, jsonify, request, render_template
import psycopg2

app = Flask(__name__)
@app.route('/')
def home_page():
    return 'Employee Details'

DB_HOST = 'localhost'
DB_NAME = 'movie_db'
DB_USER = 'postgres'
DB_PASSWORD = 'Haris'

#Saving the details from Json file to the DB and creating the users
@app.route('/api/users', methods=['POST'])
def create_employee():
    try:
        if 'file' not in request.files:
            return jsonify({"error":"No file uploaded"}),400
        file=request.files['file']
        record = json.load(file)

        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        
        for employee in record:
            cursor.execute("""insert into employees (id, first_name, last_name, company_name, city, state, zip, email, web, age) 
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id, first_name, last_name""", 
                        (employee['id'], employee['first_name'], employee['last_name'], employee['company_name'], employee['city'], 
                         employee['state'], employee['zip'], employee['email'], employee['web'], employee['age']))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({
            "message": "Employees created successfully", 
        }), 201


#Listing all the users
@app.route('/api/users', methods=['GET'])
def retrieve_employees():
    try:
        page = int(request.args.get('page', 1)) 
        limit = int(request.args.get('limit', 5))
        search = request.args.get("search","").strip()
        sort = request.args.get("sort","")
        sort_order = "ASC"
        if sort.startswith("-"):
            sort_order="DESC"
            sort=sort[1:]
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute("SELECT id, first_name, last_name, company_name, age FROM employees order by id asc;")
        employees = cursor.fetchall()
        start_idx = (page-1) * limit
        end_idx = start_idx + limit
        employees = employees[start_idx:end_idx]
        employee_list = []
        if search:
            result=[]
            for employee in employees:
                if employee[1].lower()==search.lower() or employee[2].lower()==search.lower():
                    result.append(employee)
            for data in result:
                employee_list.append({
                    "id": data[0],
                    "first_name": data[1],
                    "last_name": data[2],
                    "company_name":data[3],
                    "age":data[4]
                })
            return jsonify({"User Details": employee_list}),200
        elif sort:
            if sort_order=="ASC":
                sorted_employees = sorted(employees, key=lambda x: x[4])
            else:
                sorted_employees = sorted(employees, key=lambda x: x[4], reverse=True)
            for data in sorted_employees:
                employee_list.append({
                    "id": data[0],
                    "first_name": data[1],
                    "last_name": data[2],
                    "company_name":data[3],
                    "age":data[4]
                })
            return jsonify({"User Details": employee_list}),200
        else:
            for data in employees:
                employee_list.append({
                    "id": data[0],
                    "first_name": data[1],
                    "last_name": data[2],
                    "company_name":data[3],
                    "age":data[4]
                })
            return jsonify({"User Details": employee_list}),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Updating the user details
@app.route('/api/users/<int:id>', methods=['PUT'])
def update_employee(id):
    employee_data = request.get_json()
    first_name = employee_data.get('first_name')
    last_name = employee_data.get('last_name')
    company = employee_data.get('company_name')
    city = employee_data.get('city')
    state = employee_data.get('state')
    zip = employee_data.get('zip')
    email = employee_data.get('email')
    web = employee_data.get('web')
    age = employee_data.get('age')

    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
 
        cursor.execute("""
                       UPDATE employees SET first_name=%s, last_name=%s, company_name=%s, city=%s, state=%s, zip=%s, email=%s, web=%s, age=%s
                        WHERE id=%s returning company_name,state;
                       """,(first_name, last_name, company, city, state, zip, email, web, age, id))
        connection.commit()
        cursor.close()
        connection.close()
 
        return jsonify({
            "message": "Employee updated successfully"
        }), 201
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#Display the user with specific user id
@app.route('/api/users/<int:id>', methods=['GET'])
def fetch_employee(id):
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
 
        cursor.execute("SELECT * FROM employees where id=%s;",(id,))
        employee_detail = cursor.fetchone()
        if not employee_detail:
            return jsonify({"message": "No employee found"}), 404
        data=list(employee_detail)
        
        employee_list = []
        employee_list.append({
            "id": data[0],
            "first_name": data[1],
            "last_name": data[2],
            "company_name":data[3],
            "city":data[4],
            "state":data[5],
            "zip":data[6],
            "email": data[7],
            "web":data[8],
            "age":data[9]
        })
        cursor.close()
        connection.close()
 
        return jsonify(employee_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#Delete the user with respect to the given id    
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
 
        cursor.execute("DELETE FROM employees where id=%s;",(id,))
        connection.commit()
        cursor.close()
        connection.close()
 
        return jsonify({"message":"Employee deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#Partially updating the user
@app.route('/api/users/<int:id>', methods=['PATCH'])
def patch_employee(id):
    try:
        data = request.get_json()
        state = data.get('state')
        city = data.get('city')
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute("UPDATE employees SET state=%s, city=%s where id=%s RETURNING id;",(state,city,id))
        updated_user = cursor.fetchone()
        if not updated_user:
            return jsonify({"message":"Employee not found"}),404
 
        connection.commit()
        cursor.close()
        connection.close()
 
        return jsonify({"message":"Employee updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

#Display the overall summary of the user
@app.route('/api/users/summary',methods=['GET'])
def get_user_summary():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*),AVG(age) from employees;")
        total_users, average_age = cursor.fetchone()
        cursor.execute("select city,count(*) from employees group by city;")
        #users_by_city={city:count for city,count in cursor.fetchall()}
        connection.close()
        return jsonify({
            "total_users":total_users,
            "average_age":round(average_age,2) if average_age else None
            #"users_by_city":users_by_city
        }),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500