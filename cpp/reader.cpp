// This program only executes if a certain file exists.

#include <sys/stat.h>
#include <unistd.h>

#include <iostream>

using namespace std;

const char* FILENAME = "/opt/tritonserver/DEPLOYED";

inline bool deployed(const char* deployed_file) {
  struct stat buffer;
  return (stat(deployed_file, &buffer) == 0);
}

int main() {
  cout << "Ready to be deployed" << endl;
  while (!deployed(FILENAME)) {
    cout << "Waiting for deployment..." << endl;
    sleep(1);
  }
  cout << "Deployed!" << endl;

  return 0;
}