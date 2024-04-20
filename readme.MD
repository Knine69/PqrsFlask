Flask was installed

curls:
    curl -X POST -H "Content-Type: application/json" -d '{"document":"12345", "password":"pwd"}' http://localhost:5000/login/auth

    curl -X POST -H "Content-Type: application/json" -d '{"name": "Jane", "documentId": "987654", "email": "jane@example.com", "positionId": 1, "roleId":1, "departmentId":1, "password":"pass"}' http://localhost:5000/person/new_person

    curl -X PATCH -H "Content-Type: application/json" -d '{"password":"pass"}' http://localhost:5000/person/1