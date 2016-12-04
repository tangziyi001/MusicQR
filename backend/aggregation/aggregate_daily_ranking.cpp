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
    auto t = std::time(nullptr);
    auto tm = *std::localtime(&t);
    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y-%m-%d");
    auto str = oss.str();
    std::cout << str << std::endl;
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
      sql::Statement *stmt;
      sql::ResultSet *res;
      /* Create a connection */
      driver = get_driver_instance();
      con = driver->connect(HOST, USER, PASSWORD);
      /* Connect to the MySQL musician database */
      con->setSchema("musician");
      stmt = con->createStatement();
      com = "SELECT music_id, COUNT(*) FROM musician_download GROUP BY music_id HAVING 'Date' = " + curDate() + " ORDER BY COUNT(*) DESC;";
      res = stmt->executeQuery(AGGREGATE);
      while (res->next()) {
          cout << res->getInt("MusicID") << endl;
	  cout << res->getInt("Rank") << endl;
      }
      delete res;
      delete stmt;
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

