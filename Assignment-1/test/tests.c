#include "../include/stdafx.h"
#include "../include/main.h"
#include "../../vendor/minunit/minunit.h"

MU_TEST(parseInput_pass)
{
    char one[BUF_SIZE] = "     hdhswsda ajjaj   ";
    char two[BUF_SIZE][BUF_SIZE];

    int x = parseInput(one,two);

    mu_assert(x == 2, two);
}

MU_TEST(parseInput_fail)
{
    char one[BUF_SIZE] = "     hdhswsda ajjaj   \n";
    char two[BUF_SIZE][BUF_SIZE];

    int x = parseInput(one,two);

    mu_assert(x != 2, two);
}

MU_TEST(readCommands_pass)
{
    char one[BUF_SIZE] = "ls -l";
    char two[BUF_SIZE][BUF_SIZE];

    int readCommands(one,two,stdin);
}

MU_TEST_SUITE(test_suite)
{
    MU_RUN_TEST(parseInput_pass);
    MU_RUN_TEST(parseInput_fail);
}


int main(int argc, char *argv[])
{
	MU_RUN_SUITE(test_suite);
	MU_REPORT();
	return MU_EXIT_CODE;
}