SELECT DISTINCT
	rc."year"                                       	AS year,
	rs."raceId"                                     	AS race_id,
	rc."name"                                           AS circuit,
	cs."name"    			  						    AS constructor,
	TRIM(dr."forename") || ' ' || TRIM(dr."surname")    AS driver,
	rs."positionOrder"                                  AS position,
	rs."points"                                    	 	AS points,
	st."status"                                     	AS status
FROM 
	results            	       AS rs
	INNER JOIN races    	   AS rc ON rs."raceId" = rc."raceId"
	INNER JOIN status   	   AS st ON rs."statusId" = st."statusId" 
	INNER JOIN constructors    AS cs ON rs."constructorId" = cs."constructorId" 
	INNER JOIN drivers         AS dr ON rs."driverId" = dr."driverId"
ORDER BY
	year, race_id, position