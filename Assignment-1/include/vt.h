#ifndef VT_H_
#define VT_H_

    // ANSI Color Escape Sequence
    // \033[38;2;<r>;<g>;<b>m     #Select RGB foreground color
    // \033[48;2;<r>;<g>;<b>m     #Select RGB background color

    #define VT_BOLD "\033[1m"
    #define VT_RESET "\033[0m"

    #define VT_FG_DEFAULT "\033[39m"
    #define VT_FG_WHITE "\033[38;2;255;255;255m"
    #define VT_FG_BLUE "\033[38;2;0;0;204m"
    #define VT_FG_PURPLE "\033[38;2;255;0;255m"

    #define VT_BG_DEFAULT "\033[49m"
    #define VT_BG_WHITE "\033[48;2;255;255;255m"

#endif // VT_H_