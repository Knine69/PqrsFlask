
use pqrs;

-- Patch Table SP

DELIMITER //

CREATE PROCEDURE PatchRecordsInTable(IN tableName VARCHAR(255), IN recordId INT, IN patchData JSON)
BEGIN
    DECLARE updateStatement VARCHAR(1000);
    DECLARE columnList VARCHAR(1000);
    DECLARE columnValue VARCHAR(255);

    SELECT GROUP_CONCAT(
        COLUMN_NAME, ' = ', 
        CASE 
            WHEN DATA_TYPE IN ('INT', 'DECIMAL', 'DOUBLE') THEN JSON_UNQUOTE(JSON_EXTRACT(patchData, CONCAT('$.', COLUMN_NAME)))
            ELSE CONCAT('''', JSON_UNQUOTE(JSON_EXTRACT(patchData, CONCAT('$.', COLUMN_NAME))), '''')
        END
    ) INTO columnList
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = tableName;

    SET updateStatement = CONCAT('UPDATE ', tableName, ' SET ', columnList, ' WHERE ', tableName, '_id = ?');
    SET @recordId = recordId;
    SET @updateStatement = updateStatement;
    
    PREPARE stmt FROM @updateStatement;
    EXECUTE stmt USING @recordId;
    DEALLOCATE PREPARE stmt;
    
    SET @tableName = tableName;
	SET @idColumn = CONCAT(@tableName, '_id');

	SET @query = CONCAT('SELECT * FROM ', @tableName, ' WHERE ', @idColumn, ' = ', @recordId);
	PREPARE stmt FROM @query;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
END //

DELIMITER ;

CALL PatchRecordsInTable('person', 1, '{"password": ""}');

-- Get Category by Name

DELIMITER //
CREATE PROCEDURE GetCategoryByName (IN categoryName VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT * FROM category WHERE name LIKE \'%', categoryName, '%\'');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetRoleByName (IN roleName VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT * FROM role WHERE name LIKE \'%', roleName, '%\'');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetPositionByName (IN positionName VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT * FROM position WHERE name LIKE \'%', positionName, '%\'');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE GetDepartmentByName (IN departmentName VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT * FROM department WHERE name LIKE \'%', departmentName, '%\'');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;


-- Get Person By DocumentId

DELIMITER //
CREATE PROCEDURE GetPersonByDocumentId (IN documentId VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT * FROM person WHERE document_id = ', documentId);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- Get State by Id
DELIMITER //
CREATE PROCEDURE GetStateById (IN stateId INT)
BEGIN

	SET @query = CONCAT('SELECT * FROM state WHERE state_id = ', stateId);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;


-- Get Person by Id
DELIMITER //
CREATE PROCEDURE GetPersonById (IN personId INT)
BEGIN

	SET @query = CONCAT('SELECT * FROM person WHERE person_id = ', personId);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- Get Role name by ID

DELIMITER //
CREATE PROCEDURE GetRoleById (IN roleId VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT name FROM role WHERE role_id = ', roleId);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- Get Position name by ID

DELIMITER //
CREATE PROCEDURE GetPositionById (IN positionId VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT name FROM position WHERE position_id = ', positionId);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetEntriesRelatedToPersonById (IN tableName VARCHAR(100), IN personId INT)
BEGIN
	SET @personId = personId;
	SET @query = CONCAT('SELECT p.name as person, p.document_id, p.email, n.name FROM ', tableName, ' n INNER JOIN person p ON p.', tableName, '_id = n.', tableName, '_id and p.person_id = ?');
    PREPARE stmt FROM @query;
    EXECUTE stmt USING @personId;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- Get Category by Name

DELIMITER //
CREATE PROCEDURE GetCategoryByName (IN categoryName VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT * FROM category WHERE name LIKE \'%', categoryName, '%\'');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetRoleByName (IN roleName VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT * FROM role WHERE name LIKE \'%', roleName, '%\'');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetPositionByName (IN positionName VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT * FROM position WHERE name LIKE \'%', positionName, '%\'');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE GetDepartmentByName (IN departmentName VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT * FROM department WHERE name LIKE \'%', departmentName, '%\'');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;


-- Get Person By DocumentId

DELIMITER //
CREATE PROCEDURE GetPersonByDocumentId (IN documentId VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT * FROM person WHERE document_id = ', documentId);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- Get State by Id
DELIMITER //
CREATE PROCEDURE GetStateById (IN stateId INT)
BEGIN

	SET @query = CONCAT('SELECT * FROM state WHERE state_id = ', stateId);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;


-- Get Person by Id
DELIMITER //
CREATE PROCEDURE GetPersonById (IN personId INT)
BEGIN

	SET @query = CONCAT('SELECT * FROM person WHERE person_id = ', personId);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- Get Role name by ID

DELIMITER //
CREATE PROCEDURE GetRoleById (IN roleId VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT name FROM role WHERE role_id = ', roleId);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;

-- Get Position name by ID

DELIMITER //
CREATE PROCEDURE GetPositionById (IN positionId VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT name FROM position WHERE position_id = ', positionId);
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE GetEntriesRelatedToPersonById (IN tableName VARCHAR(100), IN personId INT)
BEGIN
	SET @personId = personId;
	SET @query = CONCAT('SELECT p.name as person, p.document_id, p.email, n.name FROM ', tableName, ' n INNER JOIN person p ON p.', tableName, '_id = n.', tableName, '_id and p.person_id = ?');
    PREPARE stmt FROM @query;
    EXECUTE stmt USING @personId;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;