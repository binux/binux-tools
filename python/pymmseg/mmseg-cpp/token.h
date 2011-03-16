#ifndef _TOKEN_H_
#define _TOKEN_H_

namespace rmmseg
{
    struct Token
    {
        Token(const char *txt, int len, char att='@')
            :text(txt), length(len), attr(att) { }
        // `text' may or may not be nul-terminated, its length
        // should be stored in the `length' field.
        //
        // if length is 0, this is an empty token
        const char *text;
        int length;
        char attr;
    };
}

#endif /* _TOKEN_H_ */
