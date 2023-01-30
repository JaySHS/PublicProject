#include<algorithm>
#include<iostream>
#include<string>
#include<thread>
#include<vector>

#include<sqlite3.h>

std::string str_toupper(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(), 
                   [](unsigned char c){ return std::toupper(c); }
                  );
    return s;
}

class Table{
    std::string tablename;
    std::vector<std::string> column;
    std::vector<std::string> type;
    std::vector<bool> IsPrimary;
    std::vector<bool> IsNotNULL;

    public:
        Table(std::string name){tablename = str_toupper(name);}
        void addcolumn(std::string, std::string, bool, bool);
        std::string tablegenerate();

};

void Table::addcolumn(std::string cname, std::string ctype, bool cIsNotNULL = false, bool cIsPrimary = false){
    column.push_back(str_toupper(cname));
    type.push_back(str_toupper(ctype));
    IsPrimary.push_back(cIsPrimary);
    IsNotNULL.push_back(cIsNotNULL);
}

std::string Table::tablegenerate(){
    std::string generator = tablename + " (";

    for(int i=0; i < column.size(); i++){
        generator.append(" "+column[i]);
        generator.append(" "+type[i]);
        if(IsPrimary[i])
            generator.append(" PRIMARY KEY");
        if(IsNotNULL[i])
            generator.append(" NOT NULL");
        generator.append(",");
    }
    generator.pop_back();
    generator.append(" );");

    return generator;
}

class SQLDB{
    sqlite3 *DB;
    std::vector<Table*> DBtablelist;
    std::string dbname;
    int exit = 0;

    public:
        SQLDB(std::string name){
            dbname = name;
        }

        void SQL_OPEN();
        void SQL_CLOSE();
        void SQL_CREATE(Table*);
};

void SQLDB::SQL_OPEN(){
    exit = sqlite3_open(dbname.c_str(), &DB);

    if (exit) {
        std::cerr << "Error open DB " << sqlite3_errmsg(DB) << std::endl;
    }
    else
        std::cout << "Opened Database Successfully!" << std::endl;
}

void SQLDB::SQL_CLOSE(){
    sqlite3_close(DB);
}

void SQLDB::SQL_CREATE(Table *table){
    DBtablelist.push_back(table);
    std::string sql = "CREATE TABLE " + table->tablegenerate();
    exit = sqlite3_open(dbname.c_str(), &DB);
    char* messaggeError;
    exit = sqlite3_exec(DB, sql.c_str(), NULL, 0, &messaggeError);
  
    if (exit != SQLITE_OK) {
        std::cerr << "Error Create Table" << std::endl;
        sqlite3_free(messaggeError);
    }
    else
        std::cout << "Table created Successfully" << std::endl;
}

int main() {
    std::string name = "test.sqlite";
    Table *table1 = new Table("sample");
    Table *table2 = new Table("sample2");
    SQLDB DB(name);

    table1->addcolumn("id", "int", true, true);
    table1->addcolumn("name", "text", true);
    table1->addcolumn("grade", "real");
    table2->addcolumn("id", "int", true, true);
    table2->addcolumn("name", "text", true);
    table2->addcolumn("grade", "real");

    DB.SQL_OPEN();
    DB.SQL_CREATE(table1);
    DB.SQL_CREATE(table2);

    // std::vector<std::thread> threads;
    // for (auto &th : threads) {
    //     th.join();
    // }

    DB.SQL_CLOSE();
    return 0;
}