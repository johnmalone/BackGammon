import curses, curses.panel
import logging

logging.basicConfig(filename='/tmp/curses.log',level=logging.DEBUG)

class CursesBoard () :
    boardState = False
    homeState = False
    jailState = False

    pips = []
    checkers = []
    jail = []
    home = []

    def __init__(self,stdscr):
        self.stdscr = stdscr
        self.windowWidth = 70
        self.windowHeight = 24
        self.playPanelWidth = 28
        self.playPanelHeight = 15
        self.checkers.insert(0,None)
        self.checkers.insert(1,curses.ACS_CKBOARD)
        self.checkers.insert(2,curses.ACS_DIAMOND)
        self.jail.insert(0,None)
        self.home.insert(0,None)
        self.diceValue1 = '?'
        self.diceValue2 = '?'
        self.promptText = False
        self.errorMessage = ''

    def make_panel(self, h,l, y,x, str, box = True):
        win = curses.newwin(h,l, y,x)
        win.erase()
        if box : win.box()

        panel = curses.panel.new_panel(win)
        return win, panel

    def addPromptText(self, text):
        self.promptText = text

    def getUserInput(self):
        curses.echo()
        curses.curs_set(True)
        userInput = self.prompt.getstr()
        curses.curs_set(False)
        curses.noecho()
        return userInput

    def getTokenForPlayer(self,player):
        return self.checkers[player]

    def returnViewPlayerFromBoardPlayer(self,boardPlayer):
        logging.debug('boardPlayer {0}'.format(boardPlayer))
        if boardPlayer > 0 :
            return 1
        else:
            return 2

    def addErrorMessage(self, msg):
        self.errorMessage = msg

    def addState(self, state):
        self.boardState = state

    def addBoardObj(self,board):
        self.boardObj = board

    def draw_pip(self, pipDict) :
        pipDict['win'].addch(pipDict['y'], pipDict['x'], curses.ACS_VLINE)

    def draw_prompt(self, activePlayer) :
        if self.promptText:
            self.prompt.addstr(1,0,self.promptText)
        else:
            start = 'Player '
            end = '\'s turn>'
            self.prompt.addstr(1,0,start)
            self.prompt.addch(1,len(start),self.checkers[activePlayer])
            self.prompt.addstr(1,len(start) + 1, end)

    def draw_error_msg(self) :
        if self.errorMessage:
            self.errors.addstr(1,0,self.errorMessage)

    def draw_numbers_under_pips(self, win):

        for pipNum,pipDict in enumerate(self.pipMap):
            if pipNum > 5 and pipNum < 18 :
                x = 1 + pipDict['x']
            elif pipNum < 6 :
                x = 2 + pipDict['x'] + (self.playPanelWidth)
            else :
                x = 1 + pipDict['x'] + (self.playPanelWidth)
            if pipNum > 11 :
                y = 1
            else :
                y = self.windowHeight-7
            win.addstr(y, x, str(pipNum+1))

    def setActiveDice(self,dice):
        self.activeDice = dice

    def addDice(self, dice):
        self.diceValue1 = dice[0]
        self.diceValue2 = dice[1]

    def draw_dice(self):
        # if theres a dupicate in the list a double was rolled
        if self.diceValue1 == self.diceValue2:
            if self.diceValue1 in self.activeDice:
            # todo: make 3rd type work for doubles. A_UNDERLINE
                if len(self.activeDice) == 4:
                    self.dice1.addstr(1,1, str(self.diceValue1), curses.A_STANDOUT)
                    self.dice2.addstr(1,1, str(self.diceValue2), curses.A_STANDOUT)
                elif len(self.activeDice) == 3:
                    self.dice1.addstr(1,1, str(self.diceValue1), curses.A_STANDOUT)
                    self.dice2.addstr(1,1, str(self.diceValue2), curses.A_UNDERLINE)
                elif len(self.activeDice) == 2:
                    self.dice1.addstr(1,1, str(self.diceValue1), curses.A_STANDOUT)
                    self.dice2.addstr(1,1, str(self.diceValue2), curses.A_DIM)
                else :
                    self.dice1.addstr(1,1, str(self.diceValue1), curses.A_UNDERLINE)
                    self.dice2.addstr(1,1, str(self.diceValue2), curses.A_DIM)
        else:
            if self.diceValue1 in self.activeDice:
                self.dice1.addstr(1,1, str(self.diceValue1), curses.A_STANDOUT)
            else:
                self.dice1.addstr(1,1, str(self.diceValue1), curses.A_DIM)

            if self.diceValue2 in self.activeDice:
                self.dice2.addstr(1,1, str(self.diceValue2), curses.A_STANDOUT)
            else:
                self.dice2.addstr(1,1, str(self.diceValue2), curses.A_DIM)

    def draw_checkers_at_pip(self, count, player, pip) :
        if not count :
            return True

        pipInfo = self.pipMap[pip]
        if pip < 6 or pip > 17:
            for i in range(0, count) :
                if i > 4 :
                    if count < 9:
                        char = str(count)
                    else: 
                        char = '*'
                    add = 5
                else :
                    char = self.checkers[player]
                    add = i

                if pipInfo['y'] == 0 :
                    y = ((pipInfo['y']) + 1) + add
                else :
                    y = ((pipInfo['y']) - 1) - add
                pipInfo['win'].addch(y, pipInfo['x'],char)

        if pip > 5 or pip < 18:
            for i in range(0, count) :
                if i > 4 :
                    if count < 9:
                        char = str(count)
                    else:
                        char = '*'
                    add = 5
                else :
                    char = self.checkers[player]
                    add = i

                if pipInfo['y'] == 0 :
                    y = ((pipInfo['y']) + 1) + add
                else :
                    y = ((pipInfo['y']) - 1) - add
                pipInfo['win'].addch(y, pipInfo['x'], char)

    def draw_board_state(self):
        self.boardObj.resetView()
        for i in range(24):
            tokens = self.boardObj.getPipAtIdx(i)
            if tokens > 0 :
                player = 1
            else: # means pips with no players are -1, but thats fine
                player = -1
            self.draw_checkers_at_pip(abs(tokens),player, i)
        self.draw_checkers_in_jail()
        self.draw_checkers_in_home()
        self.draw_dice()


    def draw_checkers_in_jail(self) :
        for player in [-1,1]:
            jailCount = self.boardObj.getJailCountForPlayer(player)
            if not jailCount:
                return False
            win = self.jail[player]
            for l in range(jailCount+1):
                char = self.checkers[player]
                if player == 1:
                    win.addch(l+1,1,char)
                else :
                    win.addch(((self.playPanelHeight//2)-2) - l, 1, char)

    def draw_checkers_in_home(self) :
        for player in [-1,1]:
            homeCount = self.boardObj.getHomeCountForPlayer(player)
            if not homeCount:
                continue

            win = self.home[player]
            m = 0;
            n = 1;
            for l in range(homeCount+1):
                if m < 5 :
                   m += 1
                else:
                    m = 1
                    n += 1
                win.addch(n,m,self.checkers[player])

    def createBoard(self, activePlayer):
        try:
            curses.curs_set(0)
        except:
            pass
        self.boardObj.setBoardForPlayer(1)
        activePlayer = self.returnViewPlayerFromBoardPlayer(activePlayer)
        homePanelWidth = (self.windowWidth - ((self.playPanelWidth*2)+7))
        win1, panel1 = self.make_panel(self.windowHeight, self.windowWidth, 0, 0, "Main Board")
        self.mainBoard = win1

        win2, panel2 = self.make_panel(self.playPanelHeight, self.playPanelWidth, 2, 1, "")
        win3, panel3 = self.make_panel(self.playPanelHeight, self.playPanelWidth, 2, self.playPanelWidth+2, "")

        win4, panel4 = self.make_panel((self.playPanelHeight//2) - 2, homePanelWidth, 2, (self.windowWidth - (homePanelWidth+3)), "")
        win5, panel5 = self.make_panel((self.playPanelHeight//2) - 2, homePanelWidth, 5+(self.playPanelHeight//2), (self.windowWidth - (homePanelWidth+3)), "")

        win6, panel6 = self.make_panel((self.playPanelHeight//2), 2, 2, self.playPanelWidth, "", False)
        win7, panel7 = self.make_panel((self.playPanelHeight//2), 2, self.playPanelHeight//2+1, self.playPanelWidth, "", False)

        win8, panel8 = self.make_panel(3, self.windowWidth - 3, self.windowHeight - 4, 1, "", False)
        win9, panel9 = self.make_panel(3, self.windowWidth - 3, self.windowHeight-6, 1, "", False)

        self.prompt = win8
        self.errors = win9

        panel2.top()
        panel3.top()
        panel8.top()

        self.dice1,panel10 = self.make_panel(3,3, (self.playPanelHeight//2)+1, (self.windowWidth - (homePanelWidth+3)), "2")
        self.dice2,panel11 = self.make_panel(3,3, (self.playPanelHeight//2)+1, (self.windowWidth - (homePanelWidth-1)), "2")

        self.pipMap = []
        for pos in range(0,6) :
            coord = int((self.playPanelWidth / 7) * (6-pos))
            onePip = {'y': self.playPanelHeight-1,'x': coord, 'win': win3}
            self.pipMap.append(onePip)

        for pos in range(6,12) :
            coord = int((self.playPanelWidth / 7) * (12-pos))
            onePip = {'y': self.playPanelHeight-1,'x': coord, 'win': win2}
            self.pipMap.append(onePip)

        for pos in range(12,18):
            coord = int((self.playPanelWidth / 7) * (pos-11))
            onePip = {'y': 0,'x': coord, 'win': win2}
            self.pipMap.append(onePip)

        for pos in range(18,24):
            coord = int((self.playPanelWidth / 7) * (pos-17))
            onePip = {'y': 0,'x': coord, 'win': win3}
            self.pipMap.append(onePip)

        self.jail.insert(2,win6)
        self.jail.insert(1,win7)

        self.home.insert(2,win4)
        self.home.insert(1,win5)

        self.draw_prompt(activePlayer)

        self.draw_error_msg()

        for i,pipStruct in enumerate(self.pipMap):
            self.draw_pip(pipStruct)

        self.draw_numbers_under_pips(self.mainBoard)

        self.draw_board_state()

        curses.panel.update_panels()
        self.stdscr.refresh()


def bgBoard(stdscr) :
    board = CursesBoard(stdscr)
    return board


if __name__ == '__main__':
    curses.wrapper(bgBoard)

