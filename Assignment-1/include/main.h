#include "stdafx.h"
#define BUF_SIZE 256
#define MY_SIGTERM 15

void init(void);
void promptUser(bool isBatch);
void printError(void);
int parseInput(char* input, char* splitWords[BUF_SIZE]);
char* redirectCommand(char* special, char* line, bool* isRedirect, char* tokens[BUF_SIZE], char* outputTokens[BUF_SIZE]);
char* executeCommand(char* cmd, bool* isRedirect, char* tokens[BUF_SIZE], char* outputTokens[BUF_SIZE],  bool* isExits);
char getLetter(char* str, int index);
bool exitProgram(char* tokens[BUF_SIZE], int numTokens);
void launchProcesses(char* tokens[BUF_SIZE], int numTokens, bool isRedirect);
void changeDirectories(char* tokens[BUF_SIZE], int numTokens);
void getHelp(char* tokens[BUF_SIZE], int numTokens);
int parseCommand(char* command, char* parameters[BUF_SIZE]);
int readCommands(char* command, char* parameters[BUF_SIZE], FILE* in);
void removeChars(char* str, char c);
