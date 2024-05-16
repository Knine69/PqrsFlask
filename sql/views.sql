-- Request Information View 

CREATE OR REPLACE VIEW LookUpRequestInfo AS
SELECT 
r.request_id,
r.summary,
r.generated_at AS 'Timestamp',
c.name AS 'Category',
q.name AS 'Requester',
s.name AS 'Solver',
t.name AS 'StateName'
FROM
request r INNER JOIN category c on r.category_id = c.category_id
INNER JOIN person q ON q.person_id = r.requester_id
INNER JOIN person s ON s.person_id = r.solver_id
INNER JOIN state t ON t.state_id = r.state_id
WHERE r.request_id = get_request_id();

SELECT s.* FROM (select @request_id:=1 p) parm, LookUpRequestInfo s;

-- LookUp Person Information View

CREATE OR REPLACE VIEW LookUpPersonInformation AS
SELECT 
p.person_id,
p.name AS 'PersonName',
p.document_id,
p.email,
o.name AS 'PositionName',
r.name AS 'RoleName',
d.name as 'DepartmentName' 
FROM person p INNER JOIN position o ON p.position_id = o.position_id
INNER JOIN role r ON p.role_id = r.role_id
INNER JOIN department d ON d.department_id = p.department_id
WHERE p.person_id = get_person_id();

-- LookUp Person Requests View

CREATE OR REPLACE VIEW LookUpPersonRequests AS
SELECT 
r.request_id as 'RequestId',
r.generated_at as 'Timestamp',
r.summary as 'Summary',
c.name AS 'Category',
s.name as 'State',
q.name as 'Solver'
FROM person p INNER JOIN request r ON r.requester_id = p.person_id
INNER JOIN state s ON r.state_id = s.state_id
INNER JOIN person q ON r.solver_id = q.person_id
INNER JOIN category c on r.category_id = c.category_id
WHERE p.person_id = get_person_id() 
ORDER BY r.generated_at;

SELECT s.* FROM (select @person_id:=1 p) parm , LookUpPersonRequests s;
