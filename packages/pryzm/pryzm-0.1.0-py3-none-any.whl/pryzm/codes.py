text_attributes = {
    '_off':       0,
    '_bold':      1,
    '_dim':       2,
    '_italic':    3,
    '_under':     4,
    '_blink':     5,
    '_reverse':   6,
    '_hide':      8,

    'black':     30,
    'red':       31,
    'green':     32,
    'yellow':    33,
    'blue':      34,
    'magenta':   35,
    'cyan':      36,
    'white':     37,

    'BLACK':     40,
    'RED':       41,
    'GREEN':     42,
    'YELLOW':    43,
    'BLUE':      44,
    'MAGENTA':   45,
    'CYAN':      46,
    'WHITE':     47,
}

clear = {
    'clear_screen': '2J',
    'clear_screen_to_end': '0J',
    'clear_screen_to_start': '1J',
    'clear_line': '2K',
    'clear_line_to_end': '0K',
    'clear_line_to_start': '1K',
}

cursor = {
    'move_up': 'A',
    'move_down': 'B',
    'move_right': 'C',
    'move_left': 'D',
    'move_next_line': 'E',
    'move_prev_line': 'F',
    'move_column': 'G'
}