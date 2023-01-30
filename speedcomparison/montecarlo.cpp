#include <iostream>
#include <chrono>

int main(){
    auto started = std::chrono::high_resolution_clock::now();
    int num = 10000000;
    int cnt = 0;
    srand((unsigned)time(NULL));

    for(int i = 0; i < num; i++){
        float x = (float) rand()/RAND_MAX;
        float y = (float) rand()/RAND_MAX;
        if((x*x)+(y*y) <= 1)
            cnt++;
    }

    float pi = cnt/(num*0.25);
    auto finished = std::chrono::high_resolution_clock::now();
    std::cout << "Estimated Pi Value: " << pi << std::endl;
    std::cout << "Total runtime(ms): " << std::chrono::duration_cast<std::chrono::milliseconds>(finished-started).count();
    return 0;
}