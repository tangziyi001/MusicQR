import datetime
import mysql.connector

def retrieve_rank(musicID, target_date):
    cnx = mysql.connector.connect(user='ubuntu', password='largescaleproject', host='tangdb.cyocc9onn55j.us-west-2.rds.amazonaws.com', database='backend')
    cursor = cnx.cursor()
    query = ("SELECT MusicID, Count, Rank, Date "
  	     "FROM ranking "
     	     "WHERE MusicID = %s AND Date = %s")
    cursor.execute(query, (musicID, target_date))
    result = (0,0,0,"");
    for (music_id, count, rank, date) in cursor:
        print("Query Response: {}, {}, {}, in  {:%d %b %Y}".format( music_id, count, rank, date))
        result =  (music_id, count, rank, date)
    cursor.close()
    cnx.close()
    return result;

if __name__ == '__main__':
    retrieve_rank(1,'2016-12-04')
