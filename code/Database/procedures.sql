USE car_rental;

DELIMITER $
DROP PROCEDURE IF EXISTS login$
CREATE PROCEDURE login(IN name VARCHAR(50), IN pass VARCHAR(50), OUT type VARCHAR(50))
BEGIN 
    DECLARE user_count INT;
	DECLARE admin_count INT;
    
    SELECT COUNT(*)
    INTO user_count
    FROM user
    WHERE name = username AND pass = password;
    
    SELECT COUNT(*)
    INTO admin_count
    FROM admin
    WHERE name = username AND pass = password;

	IF (user_count > 0) THEN
		SET type = 'user';
	END IF;
    
	IF (admin_count > 0) THEN
		SET type = 'admin';
	END IF;
    
	IF (user_count = 0 AND admin_count = 0) THEN
		SET type = 'none';
	END IF;
END$
DELIMITER ;
