
DELIMITER //

CREATE TRIGGER AssignSolverToRequest 
BEFORE INSERT ON request 
FOR EACH ROW
BEGIN 
	IF NEW.solver_id IS NULL THEN
		SET NEW.solver_id = 
        (
			SELECT p.person_id
			FROM person p LEFT JOIN request q ON p.person_id = q.solver_id INNER JOIN role r ON r.role_id = p.role_id AND r.role_id = 1
			GROUP BY p.person_id
			ORDER BY COALESCE(count(q.solver_id), 0) ASC
			LIMIT 1
        );
	END IF;
END //
