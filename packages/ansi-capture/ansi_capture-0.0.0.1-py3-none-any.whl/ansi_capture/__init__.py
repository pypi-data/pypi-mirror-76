from enum import Enum
import re


class Tile:
    """Represents a single tile in the terminal"""

    def __init__(self):
        self.color = self.glyph = None
        self.reset()

    def reset(self):
        """Resets the tile to a white-on-black space"""
        self.color = {
            'fg': 37, 'bg': 40,
            'reverse': False,
            'bold': False,
        }
        self.glyph = ' '

    def set(self, glyph, color):
        self.glyph = glyph
        self.color['fg'] = color['fg']
        self.color['bg'] = color['bg']
        self.color['reverse'] = color['reverse']
        self.color['bold'] = color['bold']

class AnsiTerm:
    # TODO: Add support for EscO commands (two letters), number-only
    _escape_parser = re.compile(r"^\x1b([\[\(\)\#/]?)(\??)([\d;]*)([\w=><])")
    class Command(Enum):
        RAW = ""
        CSI_SEQ = "["
        CHAR_SET1 = "("
        CHAR_SET2 = ")"
        CHAR_ALIGN = "#"
        RESPONSE = "/"


    def __init__(self, rows, cols):
        """Initializes the AnsiTerm with rows*cols white-on-black spaces"""
        self.rows = rows
        self.cols = cols
        self.tiles = [Tile() for _ in range(rows * cols)]
        self.cursor = {
            'x': 0,
            'y': 0,
        }
        self.color = {
            'fg': 37, 'bg': 40,
            'bold': False,
            'reverse': False,
        }

    def get_string(self, from_, to):
        """Returns the character of a section of the screen"""
        return ''.join([tile.glyph for tile in self.get_tiles(from_, to)])

    def get_tiles(self, from_, to):
        """Returns the tileset of a section of the screen"""
        return [tile for tile in self.tiles[from_:to]]

    def get_cursor(self):
        """Returns the current position of the curser"""
        return self.cursor.copy()

    def _parse_sgr(self, params):
        """Handles <escape code>n[;k]m, which changes the graphic rendition"""
        param = params.pop(0)

        if param == 0:
            self.color['fg'] = 37
            self.color['bg'] = 40
            self.color['bold'] = False
            self.color['reverse'] = False
        elif param == 1:
            self.color['bold'] = True
        elif param == 7:
            self.color['reverse'] = True
        # Special text decoration; could be supported in a future version potentially.
        elif param > 7 and param < 30:
            pass
        elif param >= 30 and param <= 37:
            self.color['fg'] = param
        # Extended foreground color set command
        elif param == 38:
            subtype = params.pop(0)
            # Colors in T.416; implement later? See https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
            if subtype == 5:
                color_code = params.pop(0)
            # 24-bit colors; implement later? See https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
            elif subtype == 2:
                red, green, blue = params[0:3]
                del param[:3]
        elif param == 39:
            self.color['fg'] = 37

        elif param >= 40 and param <= 47:
            self.color['bg'] = param
        # Extended foreground color set command
        elif param == 48:
            subtype = params.pop(0)
            # Colors in T.416; implement later? See https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
            if subtype == 5:
                color_code = params.pop(0)
            # 24-bit colors; implement later? See https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
            elif subtype == 2:
                red, green, blue = params[0:3]
                del param[:3]
        elif param == 49:
            self.color['bg'] = 40

        # Additional docorative codes
        elif param > 49 and param < 56:
            pass
        # Additional docorative codes / color codes
        elif param > 57 and param < 66:
            pass
        # Superscript / subscript codes
        elif param == 73 or param == 74:
            pass
        # Bright foreground colors
        elif param > 89 and param < 98:
            pass
        # Bright background colors
        elif param > 99 and param < 108:
            pass
        # Unknown mode code
        else:
            pass

        return params

    def _fix_cursor(self):
        """
        Makes sure the cursor are within the boundaries of the current terminal
        size.
        """
        while self.cursor['x'] >= self.cols:
            self.cursor['y'] += 1
            self.cursor['x'] = self.cursor['x'] - self.cols

        if self.cursor['y'] >= self.rows:
            self.cursor['y'] = self.rows - 1

    def _parse_sequence(self, data):
        """
        This method parses the input into the numeric arguments and
        the type of sequence. If no numeric arguments are supplied,
        we manually insert a 0 or a 1 depending on the sequence type,
        because different types have different default values.

        Example 1: \x1b[1;37;40m -> numbers=[1, 37, 40] char=m
        Example 2: \x1b[m = numbers=[0] char=m
        """
        if data[0] != '\x1b':
            return None, data

        match = AnsiTerm._escape_parser.match(data)
        if not match:
            raise Exception('Invalid escape sequence, data[:20]=%r' % data[:20])

        # Catch whether the escape code is marked as a private type
        seq_type, priv, args, char = match.groups()
        is_private = True if priv == '?' else False

        # If arguments are omitted, add the default argument for this sequence.
        if not args:
            if char in 'ABCDEFSTf':
                numbers = [1]
            elif char == 'H':
                numbers = [1, 1]
            else:
                numbers = [0]
        else:
            numbers = list(map(int, args.split(';')))

        return (AnsiTerm.Command(seq_type), is_private, char, numbers), data[match.end() :]

    def get_cursor_idx(self):
        return self.cursor['y'] * self.cols + self.cursor['x']

    def _evaluate_sequence(self, seq_type, is_private, char, numbers, data):
        """
        Evaluates a sequence (i.e., this changes the state of the terminal).
        Is meant to be called with the return values from _parse_sequence as arguments.
        """
        # Translate the cursor into an index into our 1-dimensional tileset.
        curidx = self.get_cursor_idx()

        # If this is a private escape sequence, ignore it. (In the future these couldbe parsed.)
        if is_private:
            pass
        # A catch for non-raw / non-CSI sequences; in the future this could be filled out.
        elif seq_type != AnsiTerm.Command.CSI_SEQ and seq_type != AnsiTerm.Command.RAW: # CHAR_SET1, CHAR_SET2, CHAR_ALIGN, RESPONSE
            pass

        # Sets cursor position
        elif char == 'H':
            self.cursor['y'] = numbers[0] - 1 # 1-based indexes
            self.cursor['x'] = numbers[1] - 1 #
        # Sets color/boldness
        elif char == 'm' or char == 'M':
            while numbers:
                numbers = self._parse_sgr(numbers)
        # Clears (parts of) the screen.
        elif char == 'J':
            # From cursor to end of screen
            if numbers[0] == 0:
                range_ = (curidx, self.cols - self.cursor['x'] - 1)
            # From beginning to cursor
            elif numbers[0] == 1:
                range_ = (0, curidx)
            # The whole screen
            elif numbers[0] == 2:
                range_ = (0, self.cols * self.rows - 1)
            else:
                raise Exception('Unknown argument for J parameter: %s (data=%r)' % (numbers, data[:20]))
            for i in range(*range_):
                self.tiles[i].reset()
        # Clears (parts of) the line
        elif char == 'K':
            # From cursor to end of line
            if numbers[0] == 0:
                range_ = (curidx, curidx + self.cols - self.cursor['x'] - 1)
            # From beginning of line to cursor
            elif numbers[0] == 1:
                range_ = (curidx % self.cols, curidx)
            # The whole line
            elif numbers[0] == 2:
                range_ = (curidx % self.cols, curidx % self.cols + self.cols)
            else:
                raise Exception('Unknown argument for K parameter: %s (data=%r)' % (numbers, data[:20]))
            for i in range(*range_):
                self.tiles[i].reset()
        # Move cursor up
        elif char == 'A':
            self.cursor['y'] -= numbers[0]
        # Move cursor down
        elif char == 'B':
            self.cursor['y'] += numbers[0]
        # Move cursor right
        elif char == 'C':
            self.cursor['x'] += numbers[0]
        # Move cursor left
        elif char == 'D':
            self.cursor['x'] -= numbers[0]
        # Toggle between special / normal character set; we will probably need to implement eventually.
        elif char in 'FG':
            pass
        elif char == 'r' or char == 'l': # TODO
            pass
        # Save / restore xterm icon; we can ignore this.
        elif char == 't':
            pass
        # Keypad modes; we can ignore these.
        elif char in '=<>':
            pass
        else:
            raise Exception('Unknown escape code: char=%r numbers=%r data=%r' % (char, numbers, data[:20]))

    def feed(self, data):
        """Feeds the terminal with input."""
        while data:
            # If the data starts with \x1b, try to parse end evaluate a
            # sequence.
            parsed, data = self._parse_sequence(data)
            if parsed:
                self._evaluate_sequence(*parsed, data)
            else:
                # If we end up here, the character should should just be
                # added to the current tile and the cursor should be updated.
                # Some characters such as \r, \n will only affect the cursor.
                # TODO: Find out exactly what should be accepted here.
                #       Only ASCII-7 perhaps?
                a = data[0]
                if a == '\r':
                    self.cursor['x'] = 0
                elif a == '\b':
                    self.cursor['x'] -= 1
                elif a == '\n':
                    self.cursor['y'] += 1
                elif a == '\x0f' or a == '\x00':
                    pass
                else:
                    print("WRITE: [%s] at (%d,%d), index %d " % (a, self.cursor['x'], self.cursor['y'], self.get_cursor_idx()))
                    self.tiles[self.get_cursor_idx()].set(a, self.color)
                    self.cursor['x'] += 1

                data = data[1:]
        self._fix_cursor()
