BackGammon
==========

First python project - a curses backgammon game

Mainly aimed at learning python. 

Currently supports human v human, human v computer and computer v computer. The computer AI is pretty simple with attempts to favour sequences of doubles, avoid isolated pieces and some other metrics in place.

To run:

python3 main.py


* select H C or T for human computer or testing
* enter a valid move with:
 * &lt;source pip&gt; &lt;dest pip&gt;
 * EG:
 * 12 14

Issues 26/6/2014
* computer logic when figuring out a double is very slow
* random crashes remain
* computer "logic" is pretty dumb, basically doing little more than picking a move at random
