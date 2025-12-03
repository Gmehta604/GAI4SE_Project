#include <iostream>
#include <list>

using namespace std;

void action(list<int> data)
{
    list<int>::iterator i;
    cout << "The list contains: ";
    for (i = data.begin(); i != data.end(); i++)
    {
        if (*i)
        {
            cout << " " << *i;
        }
    }
    cout << endl;
}