
#include "Test.hpp"


using namespace mynamespace;
/**
 * additional comments
 */
void mynamespace::Test::test()
{
    int giveMeSomeSugar;
    std::string bob;
    test(0, bob);

    test(giveMeSomeSugar, "");
    Other o;
    o.callMeForDistances();
}

void Test::test(int a, std::string name)
{
    switch (a)
    {
        case 0: //!<do something
            break;
        default: // this should never happen

    }
}