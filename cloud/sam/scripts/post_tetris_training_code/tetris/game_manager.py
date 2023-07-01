#!/usr/bin/python3
# -*- coding: utf-8 -*-

from board_manager import BoardData, Shape

from block_controller import BLOCK_CONTROLLER

import time


#####################################################################
#####################################################################
# Game Manager
#####################################################################
#####################################################################
class GameManager:

    # a[n] = n^2 - n + 1
    LINE_SCORE_1 = 100
    LINE_SCORE_2 = 300
    LINE_SCORE_3 = 700
    LINE_SCORE_4 = 1300
    GAMEOVER_SCORE = -500

    ###############################################
    # 初期化
    ###############################################
    def __init__(self):
        self.tboard = Board(block_list=[1,1,1,1,1,1,1,1,1,1])
        self.nextMove = None
        self.lastShape = Shape.shapeNone
        self.block_index = 0            
        self.start()

    ###############################################
    # 開始
    ###############################################
    def start(self):
        self.tboard.score = 0
        ##画面ボードと現テトリミノ情報をクリア
        self.tboard.board_data.clear()
        ## 新しい予告テトリミノ配列作成
        self.tboard.board_data.createNewPiece()

    ###############################################
    # ゲームリセット (ゲームオーバー)
    ###############################################
    def resetfield(self):
        # self.tboard.score = 0
        self.tboard.reset_cnt += 1
        self.tboard.score += GameManager.GAMEOVER_SCORE
        ##画面ボードと現テトリミノ情報をクリア
        self.tboard.board_data.clear()
        ## 新しい予告テトリミノ配列作成
        self.tboard.board_data.createNewPiece()
        

    ###############################################
    # 画面リセット
    ###############################################
    def reset_all_field(self):
        # reset all field for debug
        # this function is mainly for machine learning
        self.tboard.reset_cnt = 0
        self.tboard.score = 0
        self.tboard.dropdownscore = 0
        self.tboard.linescore = 0
        self.tboard.line = 0
        self.tboard.line_score_stat = [0, 0, 0, 0]
        self.tboard.start_time = time.time()
        ##画面ボードと現テトリミノ情報をクリア
        self.tboard.board_data.clear()
        ## 新しい予告テトリミノ配列作成
        self.tboard.board_data.createNewPiece()

    ###############################################
    # ループイベント
    ###############################################
    def exec(self):
        next_x = 0
        next_y_moveblocknum = 0
        y_operation = -1

        # update CurrentBlockIndex
        if self.tboard.board_data.currentY <= 1:
            self.block_index = self.block_index + 1

        # nextMove data structure
        nextMove = {"strategy":
                        {
                            "direction": "none",    # next shape direction ( 0 - 3 )
                            "x": "none",            # next x position (range: 0 - (witdh-1) )
                            "y_operation": "none",  # movedown or dropdown (0:movedown, 1:dropdown)
                            "y_moveblocknum": "none", # amount of next y movement
                            "use_hold_function": "n", # use hold function (y:yes, n:no)
                        },
                    "option":
                        { "reset_callback_function_addr":None,
                            "reset_all_field": None,
                            "force_reset_field": None,
                        }
                    }
        # get nextMove from GameController
        GameStatus = self.getGameStatus()
        self.nextMove = BLOCK_CONTROLLER.GetNextMove(nextMove, GameStatus)


        #######################
        ## 次の手を動かす
        if self.nextMove:
            # shape direction operation
            next_x = self.nextMove["strategy"]["x"]
            # Move Down 数
            next_y_moveblocknum = self.nextMove["strategy"]["y_moveblocknum"]
            # Drop Down:1, Move Down:0
            y_operation = self.nextMove["strategy"]["y_operation"]
            # テトリミノ回転数
            next_direction = self.nextMove["strategy"]["direction"]
            use_hold_function = self.nextMove["strategy"]["use_hold_function"]

            # if use_hold_function
            if use_hold_function == "y":
                isExchangeHoldShape = self.tboard.board_data.exchangeholdShape()
                if isExchangeHoldShape == False:
                    # if isExchangeHoldShape is False, this means no holdshape exists. 
                    # so it needs to return immediately to use new shape.
                    # init nextMove
                    self.nextMove = None
                    return

            k = 0
            while self.tboard.board_data.currentDirection != next_direction and k < 4:
                ret = self.tboard.board_data.rotateRight()
                if ret == False:
                    #print("cannot rotateRight")
                    break
                k += 1
            # x operation
            k = 0
            while self.tboard.board_data.currentX != next_x and k < 5:
                if self.tboard.board_data.currentX > next_x:
                    ret = self.tboard.board_data.moveLeft()
                    if ret == False:
                        #print("cannot moveLeft")
                        break
                elif self.tboard.board_data.currentX < next_x:
                    ret = self.tboard.board_data.moveRight()
                    if ret == False:
                        #print("cannot moveRight")
                        break
                k += 1

        # dropdown/movedown lines
        dropdownlines = 0
        removedlines = 0
        if y_operation == 1: # dropdown
            ## テトリミノを一番下まで落とす
            removedlines, dropdownlines = self.tboard.board_data.dropDown()
        else: # movedown, with next_y_moveblocknum lines
            k = 0
            # Move down を1つずつ処理
            while True:
                ## テノリミノを1つ落とし消去ラインとテトリミノ落下数を返す
                removedlines, movedownlines = self.tboard.board_data.moveDown()
                # Drop してたら除外 (テトリミノが1つも落下していない場合)
                if movedownlines < 1:
                    # if already dropped
                    break
                k += 1
                if k >= next_y_moveblocknum:
                    # if already movedown next_y_moveblocknum block
                    break

        # 消去ライン数と落下数によりスコア計算
        self.UpdateScore(removedlines, dropdownlines)

        ##############################
        #
        # check reset field
        #if BOARD_DATA.currentY < 1: 
        if self.tboard.board_data.currentY < 1 or self.nextMove["option"]["force_reset_field"] == True:
            # if Piece cannot movedown and stack, reset field
            if self.nextMove["option"]["reset_callback_function_addr"] != None:
                # if necessary, call reset_callback_function
                reset_callback_function = self.nextMove["option"]["reset_callback_function_addr"]
                reset_callback_function()

            if self.nextMove["option"]["reset_all_field"] == True:
                # reset all field if debug option is enabled
                print("reset all field.")
                self.reset_all_field()
            else:
                # ゲームリセット = ゲームオーバー
                self.resetfield()

        # init nextMove
        self.nextMove = None
        return

    def loop(self):
        for _ in range(len(self.tboard.board_data.nextShapeIndexList)):
            self.exec()
        
    ###############################################
    # 消去ライン数と落下数によりスコア計算
    ###############################################
    def UpdateScore(self, removedlines, dropdownlines):
        # calculate and update current score
        # 消去ライン数で計算
        if removedlines == 1:
            linescore = GameManager.LINE_SCORE_1
        elif removedlines == 2:
            linescore = GameManager.LINE_SCORE_2
        elif removedlines == 3:
            linescore = GameManager.LINE_SCORE_3
        elif removedlines == 4:
            linescore = GameManager.LINE_SCORE_4
        else:
            linescore = 0
        # 落下スコア計算
        dropdownscore = dropdownlines
        self.tboard.dropdownscore += dropdownscore
        # 合計計算
        self.tboard.linescore += linescore
        self.tboard.score += ( linescore + dropdownscore )
        self.tboard.line += removedlines
        # 同時消去数をカウント
        if removedlines > 0:
            self.tboard.line_score_stat[removedlines - 1] += 1

    ###############################################
    # ゲーム情報の取得
    ###############################################
    def getGameStatus(self):
        # return current Board status.
        # define status data.
        status = {"field_info":
                      {
                        "width": "none",
                        "height": "none",
                        "backboard": "none",
                        "withblock": "none", # back board with current block
                      },
                  "block_info":
                      {
                        "currentX":"none",
                        "currentY":"none",
                        "currentDirection":"none",
                        "currentShape":{
                           "class":"none",
                           "index":"none",
                           "direction_range":"none",
                        },
                        "nextShape":{
                           "class":"none",
                           "index":"none",
                           "direction_range":"none",
                        },
                        "nextShapeList":{
                        },
                        "holdShape":{
                           "class":"none",
                           "index":"none",
                           "direction_range":"none",
                        },
                      },
                  "judge_info":
                      {
                        "elapsed_time":"none",
                        "game_time":"none",
                        "gameover_count":"none",
                        "score":"none",
                        "line":"none",
                        "block_index":"none",
                        "block_num_max":"none",
                        "mode":"none",
                      },
                  "debug_info":
                      {
                        "dropdownscore":"none",
                        "linescore":"none",
                        "line_score": {
                          "line1":"none",
                          "line2":"none",
                          "line3":"none",
                          "line4":"none",
                          "gameover":"none",
                        },
                        "shape_info": {
                          "shapeNone": {
                             "index" : "none",
                             "color" : "none",
                          },
                          "shapeI": {
                             "index" : "none",
                             "color" : "none",
                          },
                          "shapeL": {
                             "index" : "none",
                             "color" : "none",
                          },
                          "shapeJ": {
                             "index" : "none",
                             "color" : "none",
                          },
                          "shapeT": {
                             "index" : "none",
                             "color" : "none",
                          },
                          "shapeO": {
                             "index" : "none",
                             "color" : "none",
                          },
                          "shapeS": {
                             "index" : "none",
                             "color" : "none",
                          },
                          "shapeZ": {
                             "index" : "none",
                             "color" : "none",
                          },
                        },
                        "line_score_stat":"none",
                        "line_score_stat_len":"none",
                        "shape_info_stat":"none",
                        "random_seed":"none",
                        "obstacle_height":"none",
                        "obstacle_probability":"none"
                      },
                  }
        # update status
        ## board
        status["field_info"]["width"] = self.tboard.board_data.width
        status["field_info"]["height"] = self.tboard.board_data.height
        status["field_info"]["backboard"] = self.tboard.board_data.getData()
        status["field_info"]["withblock"] = self.tboard.board_data.getDataWithCurrentBlock()
        ## shape
        status["block_info"]["currentX"] = self.tboard.board_data.currentX
        status["block_info"]["currentY"] = self.tboard.board_data.currentY
        status["block_info"]["currentDirection"] = self.tboard.board_data.currentDirection
        ### current shape
        currentShapeClass, currentShapeIdx, currentShapeRange = self.tboard.board_data.getShapeData(0)
        status["block_info"]["currentShape"]["class"] = currentShapeClass
        status["block_info"]["currentShape"]["index"] = currentShapeIdx
        status["block_info"]["currentShape"]["direction_range"] = currentShapeRange
        ### next shape
        nextShapeClass, nextShapeIdx, nextShapeRange = self.tboard.board_data.getShapeData(1)
        status["block_info"]["nextShape"]["class"] = nextShapeClass
        status["block_info"]["nextShape"]["index"] = nextShapeIdx
        status["block_info"]["nextShape"]["direction_range"] = nextShapeRange
        ### next shape list
        for i in range(self.tboard.board_data.getShapeListLength()):
            ElementNo="element" + str(i)
            ShapeClass, ShapeIdx, ShapeRange = self.tboard.board_data.getShapeData(i)
            status["block_info"]["nextShapeList"][ElementNo] = {
                "class":ShapeClass,
                "index":ShapeIdx,
                "direction_range":ShapeRange,
            }
        ### hold shape
        holdShapeClass, holdShapeIdx, holdShapeRange = self.tboard.board_data.getholdShapeData()
        status["block_info"]["holdShape"]["class"] = holdShapeClass
        status["block_info"]["holdShape"]["index"] = holdShapeIdx
        status["block_info"]["holdShape"]["direction_range"] = holdShapeRange
        ### next shape
        ## judge_info
        status["judge_info"]["elapsed_time"] = round(time.time() - self.tboard.start_time, 3)
        status["judge_info"]["gameover_count"] = self.tboard.reset_cnt
        status["judge_info"]["score"] = self.tboard.score
        status["judge_info"]["line"] = self.tboard.line
        status["judge_info"]["block_index"] = self.block_index
        ## debug_info
        status["debug_info"]["dropdownscore"] = self.tboard.dropdownscore
        status["debug_info"]["linescore"] = self.tboard.linescore
        status["debug_info"]["line_score_stat"] = self.tboard.line_score_stat
        status["debug_info"]["shape_info_stat"] = self.tboard.board_data.shape_info_stat
        status["debug_info"]["line_score"]["line1"] = GameManager.LINE_SCORE_1
        status["debug_info"]["line_score"]["line2"] = GameManager.LINE_SCORE_2
        status["debug_info"]["line_score"]["line3"] = GameManager.LINE_SCORE_3
        status["debug_info"]["line_score"]["line4"] = GameManager.LINE_SCORE_4
        status["debug_info"]["line_score"]["gameover"] = GameManager.GAMEOVER_SCORE
        status["debug_info"]["shape_info"]["shapeNone"]["index"] = Shape.shapeNone
        status["debug_info"]["shape_info"]["shapeI"]["index"] = Shape.shapeI
        status["debug_info"]["shape_info"]["shapeI"]["color"] = "red"
        status["debug_info"]["shape_info"]["shapeL"]["index"] = Shape.shapeL
        status["debug_info"]["shape_info"]["shapeL"]["color"] = "green"
        status["debug_info"]["shape_info"]["shapeJ"]["index"] = Shape.shapeJ
        status["debug_info"]["shape_info"]["shapeJ"]["color"] = "purple"
        status["debug_info"]["shape_info"]["shapeT"]["index"] = Shape.shapeT
        status["debug_info"]["shape_info"]["shapeT"]["color"] = "gold"
        status["debug_info"]["shape_info"]["shapeO"]["index"] = Shape.shapeO
        status["debug_info"]["shape_info"]["shapeO"]["color"] = "pink"
        status["debug_info"]["shape_info"]["shapeS"]["index"] = Shape.shapeS
        status["debug_info"]["shape_info"]["shapeS"]["color"] = "blue"
        status["debug_info"]["shape_info"]["shapeZ"]["index"] = Shape.shapeZ
        status["debug_info"]["shape_info"]["shapeZ"]["color"] = "yellow"
        if currentShapeIdx == Shape.shapeNone:
            print("warning: current shape is none !!!")

        return status

#####################################################################
#####################################################################
# ボード情報
#####################################################################
#####################################################################
class Board:
    ###############################################
    # 初期化
    ###############################################
    def __init__(self, block_list: list):
        self.score = 0
        self.dropdownscore = 0
        self.linescore = 0
        self.line = 0
        self.line_score_stat = [0, 0, 0, 0]
        self.reset_cnt = 0
        self.start_time = time.time()
        self.board_data = BoardData(block_list)

if __name__ == '__main__':
    GAME_MANEGER = GameManager()
    GAME_MANEGER.loop()
