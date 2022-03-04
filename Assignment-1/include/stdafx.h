#ifndef STDAFX_H_
#define STDAFX_H_

    #include <stdio.h>
    #include <string.h>
    #include <stdlib.h>
    #include <sys/wait.h>
    #include <sys/types.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <errno.h>
    #include <sys/stat.h>
    #include <stdbool.h>

    #include "vt.h"

    int gethostname(char*, size_t); //<unistd.h>

#endif // STDAFX_H_