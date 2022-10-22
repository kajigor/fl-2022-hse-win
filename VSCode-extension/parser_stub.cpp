#include <iostream>
#include <chrono>
#include <thread>
#include <string>

int main(int argc, char *argv[]){
    std::ios_base::sync_with_stdio(false);
    if (argc == 1) {
        return 0;
    }
    // std::this_thread::sleep_for(std::chrono::milliseconds(10));
    if (std::string(argv[1]) == "--warnings"){
        std::cout << "Warning 1 1 2 \"Test_message\"\n";
        std::cout << "Error 2 3 5 \"Oh_no_Error!\"";
    }
    else{
        std::cout << "aba caba ABC G S E adsf";
    }
    return 0;
}
