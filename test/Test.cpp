
#include "Test.hpp"


using namespace mynamespace;
/**
 * additional comments
 */
void mynamespace::Test::test()
{
    int giveMeSomeSugar;
    bar(0);
}

void Test::bar(int a)
{
    switch (a)
    {
        case 0: //!<do something
            break;
        default: // this should never happen

    }
}