SELECT music_id, count 
FROM (
	SELECT d.id as music_id, IFNULL(m.count,0) AS count 
	FROM (
		SELECT music_id, COUNT(*) AS count 
		FROM musician_download WHERE CAST(download_time AS DATE) = '2016-12-04' 
		GROUP BY music_id
	) AS m 
	RIGHT OUTER JOIN musician_music AS d ON m.music_id=d.id
) AS g 
ORDER BY g.count DESC
