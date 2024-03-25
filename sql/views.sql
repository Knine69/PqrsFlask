CREATE OR REPLACE VIEW LookUpRequestInfo AS
SELECT 
r.request_id,
r.summary,
r.generated_at AS 'Timestamp',
c.name AS 'Category',
c.category_id,
q.name AS 'Requester',
q.person_id AS 'Requester ID',
s.name AS 'Solver',
s.person_id AS 'Solver ID'
FROM
request r INNER JOIN category c on r.category_id = c.category_id
INNER JOIN person q ON q.person_id = r.requester_id
INNER JOIN person s ON s.person_id = r.solver_id
WHERE r.request_id = get_request_id();

CREATE OR REPLACE VIEW LookUpPersonInformation AS
SELECT 
p.person_id,
p.name AS 'Person Name',
p.document_id,
p.email,
o.position_id,
o.name AS 'Role Name',
d.department_id,
d.name as 'Department Name' 
FROM person p INNER JOIN position o ON p.position_id = o.position_id
INNER JOIN role r ON p.role_id = r.role_id
INNER JOIN department d ON d.department_id = p.department_id
WHERE p.person_id = get_person_id();