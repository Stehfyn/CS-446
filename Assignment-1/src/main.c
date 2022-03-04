/* Author: Stephen Foster CS 446 Feb '22
 * 
 *
 *
 */

#include <stdafx.h>
#include <main.h>

#ifndef TEST

    int main(int argc, char* argv[])
    {

        FILE* fin = NULL;
        FILE* fout = NULL;
        FILE* fredirect = NULL;

        bool isRedirect = false;
        bool isBatch = false;
        bool isExits = false;

        if(argc > 2)
        {
            printError();
            return 1;
        }

        if(argc == 2)
        {
            isBatch = true;

            fin = fopen( argv[1], "r") ;

            if( fin == NULL )
            {
                printError();
                return 1;
            }

            else
            {
                char command[BUF_SIZE];
                char* arguments[BUF_SIZE];
                char* outputTokens[BUF_SIZE];
        
                for (int i = 0; i < BUF_SIZE; i++)
                    arguments[i] = (char*)malloc(BUF_SIZE * sizeof(char));
                for (int i = 0; i < BUF_SIZE; i++)
                    outputTokens[i] = (char*)malloc(BUF_SIZE * sizeof(char));

                while(readCommands(command, arguments, fin) != 0)
                {
                    printf("\n%s\n", command);
                    char* ret = executeCommand(command, &isRedirect, arguments, outputTokens, &isExits);
                    //handle redirect

                    if(isExits)
                    {
                        
                        break;
                    }
                    if(isRedirect)
                    {
                        
                        fredirect = fopen(ret, "w");
                        if(fredirect == NULL)
                        {
                            printError();
                        }
                        else
                        {
                            for(int i = 0; outputTokens[i]!=NULL; i++)
                            {
                                fprintf(fredirect, "%s", outputTokens[i]);
                                //printf("%d: %s\n", i, outputTokens[i]);
                            }
                            fclose(fredirect);
                            fredirect = NULL;
                            isRedirect = false;
                        }
                        free(ret);
                    }
                    for(int i = 0; i < BUF_SIZE; i++)
                    {
                        free(arguments[i]); //arguments[i] = NULL;
                        free(outputTokens[i]); //outputTokens[i] = NULL;
                    }

                    for (int i = 0; i < BUF_SIZE; i++)
                        arguments[i] = (char*)malloc(BUF_SIZE * sizeof(char));
                    for (int i = 0; i < BUF_SIZE; i++)
                        outputTokens[i] = (char*)malloc(BUF_SIZE * sizeof(char));

                    
                }
                for(int i = 0; i < BUF_SIZE; i++)
                {
                    free(arguments[i]); //arguments[i] = NULL;
                    free(outputTokens[i]); //outputTokens[i] = NULL;
                }
                if(isExits)
                    kill(getpid(), 15);
                else
                    return 0;
            }
        }

        init();
        fin = stdin;

        while(!isExits)
        {
            char command[BUF_SIZE];
            char* arguments[BUF_SIZE];
            char* outputTokens[BUF_SIZE];
    
            for (int i = 0; i < BUF_SIZE; i++)
                arguments[i] = (char*)malloc(BUF_SIZE * sizeof(char));
            for (int i = 0; i < BUF_SIZE; i++)
                outputTokens[i] = (char*)malloc(BUF_SIZE * sizeof(char));
            
            promptUser(false);

            int x = readCommands(command, arguments, fin);

            //printf("%s", command);

            char* ret = executeCommand(command, &isRedirect, arguments, outputTokens, &isExits);

            //handle redirect
            if(isRedirect)
            {
                
                fredirect = fopen(ret, "w");
                if(fredirect == NULL)
                {
                    printError();
                }
                else
                {
                    for(int i = 0; outputTokens[i]!=NULL; i++)
                    {
                        fprintf(fredirect, "%s", outputTokens[i]);
                        //printf("%d: %s\n", i, outputTokens[i]);
                    }
                    fclose(fredirect);
                    fredirect = NULL;
                    isRedirect = false;
                }
                free(ret);
            }
            
            for(int i = 0; i < BUF_SIZE; i++)
            {
                free(arguments[i]);
                free(outputTokens[i]);
            }
            
        }
        
        kill(getpid(), 15);
    }

#else

    extern int main(int argc, char* argv[]); // test/tests.c

#endif

void init(void)
{
    setbuf(stdout, NULL);
    printf("%s", VT_BOLD);
}

int parseInput(char* input, char* splitWords[])
{
      int wordInd = 0;
      splitWords[0] = strtok(input, " ");
      while(splitWords[wordInd] != NULL)
      {
          splitWords[++wordInd] = strtok(NULL, " ");
      }
      return wordInd;
}

void printError(void)
{
    printf("Shell Program Error Encountered\n");

    #if 0
        printf("%s\n", strerror(errno));
    #endif
}

void promptUser(bool isBatch)
{
    //display username, machine hostname, and cwd if not batch job
    if( !isBatch )
    {
        char* cwd;
        char* username;
        char hostname[ BUF_SIZE ];

        username = getenv( "USER" );
        int ret = gethostname( hostname, BUF_SIZE );
        cwd = getcwd( NULL, 0 );

        printf( "%s", VT_BOLD );
        printf( "%s%s%s@%s%s%s", VT_BG_WHITE, VT_FG_BLUE, username, hostname, VT_BG_DEFAULT, VT_FG_WHITE );
        printf( ":%s%s%s%s$%s ", VT_FG_PURPLE, VT_FG_WHITE, cwd, VT_FG_PURPLE, VT_FG_WHITE );
        printf( "%s", VT_RESET );

        free( cwd );
    }
}

char getLetter(char* str, int index)
{
    int i = 0;
    while(str[i]!='\0'){ i++; }

    if(index > i)
        return NULL;
    else
        return str[i];
}

int readCommands(char* command, char* arguments[BUF_SIZE], FILE* in)
{
    int count = 0;
    char input[BUF_SIZE];
    char* tokens[BUF_SIZE];
    
    if( fgets(input,BUF_SIZE,in) != NULL )
    {
        //printf("before parse\n");
        sprintf(command, "%s", input);
        int x = parseInput(input, tokens);

        //printf("before fix1\n");
        tokens[x-1][strlen(tokens[x-1])-1] = '\0'; //lol newline go brrr
        //printf("before strcpy\n");
        //printf("before loop\n");

        for(int i = 0; i < x; i++)
        {
            //printf("loop: %d", count);
            strcpy(arguments[i], tokens[i]);
            count++;
        }

        //printf("before NULL\n");
        arguments[count] = NULL;
    }
    return count;
}

char* executeCommand(char* cmd, bool* isRedirect, char* tokens[BUF_SIZE], char* outputTokens[BUF_SIZE],  bool* isExits)
{
    char* out_file = "";
    char* special = strchr(cmd, '>');
    //printf("works1\n");

    if(special != NULL)
    {
        out_file = redirectCommand(special, cmd, isRedirect, tokens, outputTokens);
    }
    else
    {
        int x = getTokenCount(tokens);
        //printf("token count: %d\n", x);

        if ( x == 0 )
        {
            return out_file;
        }

        else if( exitProgram( tokens, x ) )
        {
            *isExits = true;
            return out_file;
        }

        else
        {
            changeDirectories(tokens, x);
            getHelp(tokens, x);
            launchProcesses(tokens, x, *isRedirect);
        }
    }

    return out_file;
}

char* redirectCommand(char* special, char* line, bool* isRedirect, char* tokens[BUF_SIZE], char* outputTokens[BUF_SIZE])
{
    FILE* f1 = NULL;
    
    if (strchr(line, ">>") != NULL)
    {
        return "";
    }

    char files[BUF_SIZE][BUF_SIZE];
    
    int i = 0;
    while ((line = strtok(line, ">")) != NULL)
    {
        strcpy(files[i], line);
        line = NULL;
        i++;
    }

    if(i == 2)
    {
        removeChars(files[0], ' ');
        removeChars(files[1], ' ');
        removeChars(files[1], '\n');
        //printf("-%s-%s-", files[0], files[1]);

        //open file1
        f1 = fopen(files[0], "r");
        if(f1 == NULL)
        {
            printError();
            return "";
        }
        else
        {
            int index = 0;
            while(fgets(outputTokens[index], BUF_SIZE, f1)!= NULL)
            {
                index++;
            }
            outputTokens[index] = NULL;
            *isRedirect = true;
            char * ret = malloc(strlen(files[1]+1));
            strcpy(ret, files[1]);
            fclose(f1);
            return ret;
        }
    }
    else
    {
        printError();
        return "";
    }

}

bool exitProgram(char* tokens[BUF_SIZE], int numTokens)
{
    if(strcmp(tokens[0], "exit") == 0)
    {
        if (numTokens == 1)
        {
            return true;
        }
        else
        {
            printError();
        }
    }
    return false;
}

void launchProcesses(char* tokens[BUF_SIZE], int numTokens, bool isRedirect)
{
    if(!isRedirect)
    {
        if(fork() != 0)
        {
            int status = 0;
            //parent code
            waitpid(-1, &status, 0);
        }
        else
        {
            char check[BUF_SIZE];
            strcpy(check, tokens[0]);

            if((strcmp(check,"exit") != 0) && (strcmp(check, "cd") !=0 ) && ( strcmp(check, "help") != 0))
            {
                int x = execvp(tokens[0], tokens);

                if(x == -1) 
                {   
                    printError();
                    exit(1); //signals parent on fail
                }
            }
        }
    }
}

void changeDirectories(char* tokens[BUF_SIZE], int numTokens)
{
    if(strcmp(tokens[0], "cd") == 0)
    {
        if (numTokens == 1)
        {
            char* home = getenv( "HOME" );
            chdir(home);
            return;
        }

        else if (numTokens == 2)
        {
            struct stat sb;
            if( ( stat( tokens[1], &sb ) == 0 ) && S_ISDIR( sb.st_mode ) )
            {
                chdir(tokens[1]);
                return;
            }
            else
            {
                printError();
            }
        }

        else
        {
            printError();
        }
    }
}

void getHelp(char* tokens[BUF_SIZE], int numTokens)
{
    if(strcmp(tokens[0], "help") == 0)
    {
        if (numTokens == 1)
        {
            printf("Stephen's example linux shell.\n");
            printf("These shell commands are defined internally.\n");
            printf("help -printd this screen so you can see available shell commands.\n");
            printf("cd -changes directories to specified path; if not given, defaults to home.\n");
            printf("exit -closes the example shell.\n");
            printf("[input] > [output] -pipes input file into output file\n");
            printf("\nAnd more! If it's not explicitly defined here (or in the documentation for the assignment) ");
            printf("then the command should try to be executed by launchProcesses.\n");
            printf("That's how we get ls -la to work here!\n\n");
        }
        else
        {
            printError();
        }
    }
}

void clearStr(char* str)
{
    printf("%d\n", strlen(str));
    for(int i = 0; i < strlen(str); i++)
    {
        str[i] = '\0';
    }
}

void clearStr2D(char* strs[BUF_SIZE])
{
    for(int i = 0; i < BUF_SIZE; i++)
    {
        clearStr(strs[i]);
    }
}

int getTokenCount(char* tokens[BUF_SIZE])
{
    int count = 0;
    for(int i =0; tokens[i]!=NULL;i++)
    {
        count++;
    }
    return count;
}
void removeChars(char* str, char c) 
{
    char *pr = str, *pw = str;
    while (*pr) {
        *pw = *pr++;
        pw += (*pw != c);
    }
    *pw = '\0';
}
