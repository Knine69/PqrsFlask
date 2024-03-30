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

DELIMITER //
CREATE PROCEDURE GetCategoryByName (IN categoryName VARCHAR(100))
BEGIN

	SET @query = CONCAT('SELECT * FROM category WHERE name LIKE \'%', categoryName, '%\'');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;
