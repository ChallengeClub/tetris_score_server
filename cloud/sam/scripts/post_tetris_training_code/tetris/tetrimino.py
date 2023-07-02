#####################################
#####################################
# テトリミノ形状
# Shape manager
#####################################
#####################################
class Shape(object):
    shapeNone = 0
    shapeI = 1
    shapeL = 2
    shapeJ = 3
    shapeT = 4
    shapeO = 5
    shapeS = 6
    shapeZ = 7

    # shape1 : ****
    #          ----
    #          ----
    #
    # shape2 : -*--
    #          -*--
    #          -**-
    #
    # shape3 : --*-
    #          --*-
    #          -**-
    #
    # shape4 : -*--
    #          -**-
    #          -*--
    #
    # shape5 : -**-
    #          -**-
    #          ----
    #
    # shape6 : -**-
    #          **--
    #          ----
    #
    # shape7 : **--
    #          -**-
    #          ----
    #
    #テトリミノ形状座標タプル
    shapeCoord = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((0, -1), (0, 0), (0, 1), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (-1, 1)),
        ((0, -1), (0, 0), (0, 1), (1, 0)),
        ((0, 0), (0, -1), (1, 0), (1, -1)),
        ((0, 0), (0, -1), (-1, 0), (1, -1)),
        ((0, 0), (0, -1), (1, 0), (-1, -1))
    )

    def __init__(self, shape=0):
        self.shape = shape

    ##############################
    # テトリミノ形状を回転した座標を返す
    # direction: テトリミノ回転方向
    ##############################
    def getRotatedOffsets(self, direction):
        # テトリミノ形状座標タプルを取得
        tmpCoords = Shape.shapeCoord[self.shape]
        # 方向によってテトリミノ形状座標タプルを回転させる
        if direction == 0 or self.shape == Shape.shapeO:
            return ((x, y) for x, y in tmpCoords)

        if direction == 1:
            return ((-y, x) for x, y in tmpCoords)

        if direction == 2:
            if self.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
                return ((x, y) for x, y in tmpCoords)
            else:
                return ((-x, -y) for x, y in tmpCoords)

        if direction == 3:
            if self.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
                return ((-y, x) for x, y in tmpCoords)
            else:
                return ((y, -x) for x, y in tmpCoords)

    ###################
    # direction (回転状態)のテトリミノ座標配列を取得し、それをx,yに配置した場合の座標配列を返す
    ###################
    def getCoords(self, direction, x, y):
        return ((x + xx, y + yy) for xx, yy in self.getRotatedOffsets(direction))

    ###################
    # テトリミノが原点から x,y 両方向に最大何マス占有するのか返す
    ###################
    def getBoundingOffsets(self, direction):
        # テトリミノ形状を回転した座標を返す
        tmpCoords = self.getRotatedOffsets(direction)
        # 
        minX, maxX, minY, maxY = 0, 0, 0, 0
        for x, y in tmpCoords:
            if minX > x:
                minX = x
            if maxX < x:
                maxX = x
            if minY > y:
                minY = y
            if maxY < y:
                maxY = y
        return (minX, maxX, minY, maxY)

