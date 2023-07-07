#!/usr/bin/python3
# -*- coding: utf-8 -*-
import copy
from tetrimino import Shape

#####################################################################
#####################################################################
# board manager
#####################################################################
#####################################################################
BOARD_WIDTH=10
BOARD_HEIGHT=22

class BoardData(object):

    width = BOARD_WIDTH
    height = BOARD_HEIGHT

    #######################################
    ##  board manager 初期化
    #######################################
    def __init__(self, block_list: list, initial_board:list=[0]*BOARD_WIDTH*BOARD_HEIGHT):
        self.backBoard = initial_board
        self.currentX = -1
        self.currentY = -1
        self.currentDirection = 0
        self.currentShape = Shape() # initial current shape data
        self.nextShape = None
        self.holdShape = None
        self.shape_info_stat = [0] * 8
        self.nextShapeIndexCnt = 0
        self.nextShapeIndexList = block_list
        self.nextShapeIndexListDXY = [[0,0,1] for _ in range(len(self.nextShapeIndexList))] # for art DXY config data
        self.tryMoveNextCnt = 0
        self.ShapeListMax = 6
        # ShapeList
        #  ShapeNumber 0: currentShape
        #  ShapeNumber 1: nextShape
        #  ShapeNumber 2: next nextShape
        #  ...
        self.ShapeList = []

    #######################################
    ## 画面ボードデータを返す
    #######################################
    def getData(self):
        return self.backBoard[:]

    #######################################
    ## 画面ボードデータコピーし動いているテトリミノデータを付加
    #######################################
    def getDataWithCurrentBlock(self):
        # 動いているテトリミノ以外の画面ボード状態取得
        tmp_backboard = copy.deepcopy(self.backBoard)
        # テトリミノの現状形状取得
        Shape_class = self.currentShape
        # テトリミノの回転状態取得
        direction = self.currentDirection
        # 現状のテトリミノ中心位置取得
        x = self.currentX
        y = self.currentY
        # x,y 座標に回転されたテトリミノを置いた場合の座標配列を取得する
        coordArray = Shape_class.getCoords(direction, x, y)
        # 上記配列に従って画面ボードに動いているテトリミノのデータを書き込んでいく
        for _x, _y in coordArray:
            tmp_backboard[_y * self.width + _x] = Shape_class.shape
        return tmp_backboard[:]

    #######################################
    ## 画面ボード上のテトリミノを返す
    #######################################
    def getValue(self, x, y):
        return self.backBoard[x + y * BoardData.width]

    #######################################
    ## 予告テトリミノ配列の長さを返す
    #######################################
    def getShapeListLength(self):
        length = len(self.ShapeList)
        return length

    ################################
    # テトリミノクラスデータ, テトリミノ座標配列、テトリミノ回転種類を返す
    # ShapeClass ... shape のオブジェクト
    ################################
    def getShapeDataFromShapeClass(self, ShapeClass):

        if ShapeClass == None:
            return None, None, None

        #ShapeClass = self.ShapeList[ShapeNumber]
        ShapeIdx = ShapeClass.shape
        ShapeRange = (0, 1, 2, 3)
        if ShapeIdx in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            ShapeRange = (0, 1)
        elif ShapeIdx == Shape.shapeO:
            ShapeRange = (0,)
        else:
            ShapeRange = (0, 1, 2, 3)

        return ShapeClass, ShapeIdx, ShapeRange

    ################################
    # 予告テトリミノ配列番号から shape オブジェクトを返す
    # ShapeNumber ... 予告テトリミノ配列番号　
    ################################
    def getShapeData(self, ShapeNumber):
        ShapeClass = self.ShapeList[ShapeNumber]
        return self.getShapeDataFromShapeClass(ShapeClass)

    ################################
    # ホールド shape オブジェクトを返す
    ################################
    def getholdShapeData(self):
        return self.getShapeDataFromShapeClass(self.holdShape)

    ################################
    # nextShapeIndexListDXYを返す
    ################################
    def getnextShapeIndexListDXY(self, index):
        index = index % len(self.nextShapeIndexListDXY)
        d = self.nextShapeIndexListDXY[index][0]
        x = self.nextShapeIndexListDXY[index][1]
        y = self.nextShapeIndexListDXY[index][2]
        return d,x,y

    #################################################
    # direction (回転状態)のテトリミノ座標配列を取得し、それをx,yに配置した場合の座標配列を返す
    #################################################
    def getCurrentShapeCoord(self):
        return self.currentShape.getCoords(self.currentDirection, self.currentX, self.currentY)

    #################################################
    # 次のテトリミノの取得
    #################################################
    def getNewShapeIndex(self):
        # static value
        nextShapeIndex = self.nextShapeIndexList[self.nextShapeIndexCnt]
        self.nextShapeIndexCnt += 1
        if self.nextShapeIndexCnt >= len(self.nextShapeIndexList):
            self.nextShapeIndexCnt = 0
        return nextShapeIndex

    #####################################
    ## 新しい予告テトリミノ配列作成
    ####################################
    def createNewPiece(self):
        if self.nextShape == None:
            self.ShapeList.append(0)
            ## 次のテトリミノデータ作成
            # initialize next shape data
            for i in range(self.ShapeListMax-1):
                self.ShapeList.append(Shape(self.getNewShapeIndex()))
            self.nextShape = self.ShapeList[1]

        # テトリミノが原点から x,y 両方向に最大何マス占有するのか取得
        minX, maxX, minY, maxY = self.nextShape.getBoundingOffsets(0)
        result = False

        # check if nextShape can appear
        if self.tryMoveNext(0, 5, -minY):
            self.currentX = 5
            self.currentY = -minY
            self.currentDirection = 0
            # get nextShape
            self.ShapeList.pop(0)
            self.ShapeList.append(Shape(self.getNewShapeIndex()))
            self.currentShape = self.ShapeList[0]
            self.nextShape = self.ShapeList[1]
            result = True
        else:
            # cannnot appear
            self.currentShape = Shape()
            self.currentX = -1
            self.currentY = -1
            self.currentDirection = 0
            result = False
        self.shape_info_stat[self.currentShape.shape] += 1
        return result

    #####################################
    ## 動かせるかどうか確認する
    # 動かせない場合 False を返す
    #####################################
    def tryMoveCurrent(self, direction, x, y):
        return self.tryMove(self.currentShape, direction, x, y)

    #####################################
    ## 初期位置へ2回配置して動かせなかったら Reset
    #####################################
    def tryMoveNext(self, direction, x, y):
        ret = self.tryMove(self.nextShape, direction, x, y)
        if ret == False:
            # if tryMove returns False 2 times, do reset.
            self.tryMoveNextCnt += 1
            if self.tryMoveNextCnt >= 2:
                self.tryMoveNextCnt = 0
                ret = True
            else:
                ret = False
        return ret

    #####################################
    # direction (回転状態)のテトリミノ座標配列を取得し、それをx,yに配置可能か判定する
    # 配置できない場合 False を返す
    ######################################
    def tryMove(self, shape, direction, x, y):
        # direction (回転状態)のテトリミノ座標配列を取得し、それをx,yに配置した場合の座標配列を繰り返す
        for x, y in shape.getCoords(direction, x, y):
            # 画面ボード外なので false
            if x >= BoardData.width or x < 0 or y >= BoardData.height or y < 0:
                return False
            # その位置にすでに他のブロックがあるので false
            if self.backBoard[x + y * BoardData.width] > 0:
                return False
        return True

    #####################################
    ## テノリミノを1つ落とし消去ラインとテトリミノ落下数を返す
    #####################################
    def moveDown(self):
        # move piece, 1 block
        # and return the number of lines which is removed in this function.
        removedlines = 0
        moveDownlines = 0
        # 動かせるか確認
        if self.tryMoveCurrent(self.currentDirection, self.currentX, self.currentY + 1):
            self.currentY += 1
            moveDownlines += 1
        # 動かせなくなったら確定
        else:
            ##画面ボードに固着したテトリミノを書き込む
            self.mergePiece()
            ## 画面ボードの消去できるラインを探して消去し、画面ボードを更新、そして消した Line を返す
            removedlines = self.removeFullLines()
            ## 新しい予告テトリミノ配列作成
            self.createNewPiece()
            
        return removedlines, moveDownlines

    #####################################
    ## テトリミノを一番下まで落とし消去ラインとテトリミノ落下数を返す
    #####################################
    def dropDown(self):
        # drop piece, immediately
        # and return the number of lines which is removed in this function.
        dropdownlines = 0
        while self.tryMoveCurrent(self.currentDirection, self.currentX, self.currentY + 1):
            self.currentY += 1
            dropdownlines += 1

        ##画面ボードに固着したテトリミノを書き込む
        self.mergePiece()
        ## 画面ボードの消去できるラインを探して消去し、画面ボードを更新、そして消した Line を返す
        removedlines = self.removeFullLines()
        ## 新しい予告テトリミノ配列作成
        self.createNewPiece()
        return removedlines, dropdownlines

    #####################################
    ## 左へテトリミノを1つ動かす
    ## 失敗したら Falase を返す
    #####################################
    def moveLeft(self):
        if self.tryMoveCurrent(self.currentDirection, self.currentX - 1, self.currentY):
            self.currentX -= 1
        else:
            return False
        return True

    #####################################
    ## 右へテトリミノを1つ動かす
    ## 失敗したら Falase を返す
    #####################################
    def moveRight(self):
        if self.tryMoveCurrent(self.currentDirection, self.currentX + 1, self.currentY):
            self.currentX += 1
        else:
            return False
        return True

    #####################################
    ## 右回転させる
    #####################################
    def rotateRight(self):
        if self.tryMoveCurrent((self.currentDirection + 1) % 4, self.currentX, self.currentY):
            self.currentDirection += 1
            self.currentDirection %= 4
        else:
            return False
        return True

    #####################################
    ## 左回転させる
    #####################################
    def rotateLeft(self):
        if self.tryMoveCurrent((self.currentDirection - 1) % 4, self.currentX, self.currentY):
            self.currentDirection -= 1
            self.currentDirection %= 4
        else:
            return False
        return True

    #####################################
    ## ホールド入れ替え
    #####################################
    def exchangeholdShape(self):
        if self.holdShape == None:
            # if holdShape not exists, set holdShape
            self.holdShape = self.currentShape
            self.createNewPiece()
            return False
        else:
            # if holdShape exists, exchange shapes
            self.holdShape,self.currentShape = self.currentShape,self.holdShape
            # init current X,Y,Direction
            minX, maxX, minY, maxY = self.nextShape.getBoundingOffsets(0)
            self.currentX = 5
            self.currentY = -minY
            self.currentDirection = 0
        return True

    #####################################
    ## 画面ボードの消去できるラインを探して消去し、画面ボードを更新、そして消した Line を返す
    #####################################
    def removeFullLines(self):
        newBackBoard = [0] * BoardData.width * BoardData.height
        newY = BoardData.height - 1
        # 消去ライン0
        lines = 0
        # 最下段行から探索
        for y in range(BoardData.height - 1, -1, -1):
            # y行のブロック数を数える
            blockCount = sum([1 if self.backBoard[x + y * BoardData.width] > 0 else 0 for x in range(BoardData.width)])
            # y行のブロック数が幅より少ない
            if blockCount < BoardData.width:
                # そのままコピー
                for x in range(BoardData.width):
                    newBackBoard[x + newY * BoardData.width] = self.backBoard[x + y * BoardData.width]
                newY -= 1
            # y行のブロックがうまっている
            else:
                # 消去ラインカウント+1
                lines += 1
        if lines > 0:
            self.backBoard = newBackBoard
        return lines


    #####################################
    ##画面ボードに固着したテトリミノを書き込む
    #####################################
    def mergePiece(self):
        # direction (回転状態)のテトリミノ座標配列を取得し、それをx,yに配置した場合の座標配列で繰り返す
        for x, y in self.currentShape.getCoords(self.currentDirection, self.currentX, self.currentY):
            # 画面ボードに書き込む
            self.backBoard[x + y * BoardData.width] = self.currentShape.shape

        # 現テトリミノ情報を初期化
        self.currentX = -1
        self.currentY = -1
        self.currentDirection = 0
        self.currentShape = Shape()

    #####################################
    ##画面ボードと現テトリミノ情報をクリア
    #####################################
    def clear(self):
        self.currentX = -1
        self.currentY = -1
        self.currentDirection = 0
        self.currentShape = Shape()
        self.backBoard = [0] * BoardData.width * BoardData.height

    def getSearchXRange(self, Shape_class, direction):
        # get x range from shape direction.
        width = self.width
        minX, maxX, _, _ = Shape_class.getBoundingOffsets(direction) # get shape x offsets[minX,maxX] as relative value.
        xMin = -1 * minX
        xMax = width - maxX
        return xMin, xMax

    def getShapeCoordArray(self, Shape_class, direction, x, y):
        # get coordinate array by given shape.
        coordArray = Shape_class.getCoords(direction, x, y) # get array from shape direction, x, y.
        return coordArray

    def getBoard(self, board_backboard, Shape_class, direction, x):
        # get new board.
        # copy backboard data to make new board.
        # if not, original backboard data will be updated later.
        board = copy.deepcopy(board_backboard)
        return self.dropDownOnBoard(board, Shape_class, direction, x)

    def dropDownOnBoard(self, board, Shape_class, direction, x):
        # internal function of getBoard.
        # -- drop down the shape on the board.
        width = self.width
        height = self.height
        dy = 22 - 1
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        # update dy
        for _x, _y in coordArray:
            _yy = 0
            while _yy + _y < height and (_yy + _y < 0 or board[(_y + _yy) * width + _x] == 0):
                _yy += 1
            _yy -= 1
            if _yy < dy:
                dy = _yy
        # get new board
        _board = self.dropDownWithDy(board, Shape_class, direction, x, dy)
        return _board

    def dropDownWithDy(self, board, Shape_class, direction, x, dy):
        # internal function of dropDown.
        width = self.width
        _board = board
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        for _x, _y in coordArray:
            _board[(_y + dy) * width + _x] = Shape_class.shape
        return _board
