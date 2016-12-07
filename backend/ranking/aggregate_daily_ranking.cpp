#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <cstring>
#include <string>
#include <iomanip>
#include <ctime>
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
#include <cppconn/prepared_statement.h>

// Defined for test purposes.
#define HOST "tangdb.cyocc9onn55j.us-west-2.rds.amazonaws.com"
#define USER "ubuntu"
#define PASSWORD "largescaleproject"
#define DB "backend"

using namespace std;

string curDate(){
    time_t t = std::time(nullptr);
    // Aggregate yesterday's result
    t -= (24*60*60);
    auto tm = *std::localtime(&t);
    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y-%m-%d");
    auto str = oss.str();
    return str;
}
int main(int argc, const char **argv)
{
  string url(argc >= 2 ? argv[1] : HOST);
  const string user(argc >= 3 ? argv[2] : USER);
  const string pass(argc >= 4 ? argv[3] : PASSWORD);
  const string database(argc >= 5 ? argv[4] : DB);
  try {
      sql::Driver *driver;
      sql::Connection *con;
      /* Retrieve Download Data*/
      sql::Statement *stmt;
      sql::ResultSet *res;
      /* Create a connection */
      driver = get_driver_instance();
      con = driver->connect(HOST, USER, PASSWORD);
      /* Connect to the MySQL musician database */
      con->setSchema("musician");
      stmt = con->createStatement();
      /* Get Data After Grouping */
      string com = "SELECT music_id, count FROM (SELECT d.id as music_id, IFNULL(m.count,0) AS count FROM (SELECT music_id, COUNT(*) AS count FROM musician_download WHERE CAST(download_time AS DATE) = '"+curDate()+"' GROUP BY music_id) AS m RIGHT OUTER JOIN musician_music AS d ON m.music_id=d.id) AS g ORDER BY g.count DESC"; 
      res = stmt->executeQuery(com);
      /* Ranking */
      vector<vector<int> > all;
      int tmpVal = -1;
      int tmpRank = 0;
      int tmpCul = 0;
      while (res->next()) {
          vector<int> now;
	  tmpCul++;
          int music_id = res->getInt("music_id");
	  int count = res->getInt("count");
          int rank = tmpCul;
          if(count == tmpVal) {
	      rank = tmpRank;
          }
	  tmpRank = rank;
          tmpVal = count;
	  now.push_back(music_id);
	  now.push_back(count);
          now.push_back(rank);
	  all.push_back(now);
      }
      delete res;
      delete stmt;
      /* Store Data In Ranking Table */
      con->setSchema("backend");
      sql::PreparedStatement  *prep_stmt  = con->prepareStatement("INSERT IGNORE INTO ranking (MusicID, Count, Rank, Date) VALUES (?, ?, ?, ?)");
      for(vector<int>& row : all){
          prep_stmt->setInt(1, row[0]);
          prep_stmt->setInt(2, row[1]);
	  prep_stmt->setInt(3, row[2]);
          prep_stmt->setString(4, curDate());
	  prep_stmt->execute();
      }
      delete prep_stmt;
      delete con;
  } catch (sql::SQLException &e) {
    /*
      MySQL Connector/C++ throws three different exceptions:

      - sql::MethodNotImplementedException (derived from sql::SQLException)
      - sql::InvalidArgumentException (derived from sql::SQLException)
      - sql::SQLException (derived from std::runtime_error)
    */
    cout << "# ERR: SQLException in " << __FILE__;
    cout << "(" << __FUNCTION__ << ") on line " << __LINE__ << endl;
    /* what() (derived from std::runtime_error) fetches error message */
    cout << "# ERR: " << e.what();
    cout << " (MySQL error code: " << e.getErrorCode();
    cout << ", SQLState: " << e.getSQLState() << " )" << endl;

    return EXIT_FAILURE;
  }

  cout << "Done." << endl;
  return EXIT_SUCCESS;
}

