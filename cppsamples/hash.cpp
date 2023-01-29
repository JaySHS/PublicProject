#include <iostream>
#include <list>
#include <unordered_map>

struct Name;
class Hashfunction;

typedef std::unordered_map<Name, int, Hashfunction> hashmap;

struct Name{
    std::string name;

    Name(std::string s){
        name = s;
    }

    bool operator==(const Name& n) const{
        return name == n.name;
    }
};

class Hashfunction{
    public:
        size_t operator()(const Name& n) const{
            return std::hash<std::string>{}(n.name);
        }
};

int main(){
    hashmap mymap;

    Name n1("A");
    Name n2("B");
    Name n3("C");

    mymap[n1] = 1;
    mymap[n2] = 2;
    mymap[n3] = 3;

    for(auto x : mymap){
        std::cout << x.first.name << " " << x.second << std::endl;
    }

    hashmap::hasher fn = mymap.hash_function();

    std::cout << mymap.find(n2)->second << std::endl;
    std::cout << fn(n1) << std::endl;

    return 0;
}