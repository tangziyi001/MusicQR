#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <stdexcept>
/* uncomment for applications that use vectors */
/*#include <vector>*/

#include "mysql_connection.h"

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>
#include <cppconn/prepared_statement.h>

#define EXAMPLE_HOST "localhost"
#define EXAMPLE_USER "root"
#define EXAMPLE_PASS "tzy@202326"
#define EXAMPLE_DB "world"

using namespace std;

int main(int argc, const char **argv)
{
  string url(argc >= 2 ? argv[1] : EXAMPLE_HOST);
  const string user(argc >= 3 ? argv[2] : EXAMPLE_USER);
  const string pass(argc >= 4 ? argv[3] : EXAMPLE_PASS);
  const string database(argc >= 5 ? argv[4] : EXAMPLE_DB);

  cout << "Connector/C++ tutorial framework..." << endl;
  cout << endl;

  try {

    /* INSERT TUTORIAL CODE HERE! */
    
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

