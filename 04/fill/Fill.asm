// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// @SCREEN ou 16354 ou 0x4000 ~ 0x5FFF
// @KBD ou 24576 ou 0x6000

(LOOP)
@KBD
D = M
@PAINT_WHITE
D; JEQ

(PAINT_BLACK)
@SCREEN
D = A
@IDX_PIXEL
M = D
(BLACK)
@IDX_PIXEL
A = M
M = -1 // RAM[RAM[IDX_PIXEL]] = 0xFFFF
@IDX_PIXEL
M = M + 1 // RAM[IDX_PIXEL]++
D = M
@KBD
D = A - D
@BLACK
D; JGT

@LOOP
0; JMP

(PAINT_WHITE)
@SCREEN
D = A
@IDX_PIXEL
M = D
(WHITE)
@IDX_PIXEL
A = M
M = 0 // RAM[RAM[IDX_PIXEL]] = 0x0000
@IDX_PIXEL
M = M + 1 // RAM[IDX_PIXEL]++
D = M
@KBD
D = A - D
@WHITE
D; JGT

@LOOP
0; JMP




