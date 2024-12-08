#!/usr/bin/python
from collections import deque
import statistics
import sys

if sys.argv[1] == "test":
    MAZE_SIZE = 10 #迷路のサイズ
if sys.argv[1] == "run":
    MAZE_SIZE = 100 #迷路のサイズ

#next関数
def next(x, CL, OL, maze):
    if maze[x[0]-1][x[1]] == '0' and [x[0]-1,x[1]] not in CL: #xの上が通路かつCLに居ないときOLにその座標を追加
        OL.append([x[0]-1,x[1]])
    if maze[x[0]+1][x[1]] == '0' and [x[0]+1,x[1]] not in CL: #xの下が通路かつCLに居ないときOLにその座標を追加
        OL.append([x[0]+1,x[1]])
    if maze[x[0]][x[1]-1] == '0' and [x[0],x[1]-1] not in CL: #xの左が通路かつCLに居ないときOLにその座標を追加
        OL.append([x[0],x[1]-1])
    if maze[x[0]][x[1]+1] == '0' and [x[0],x[1]+1] not in CL: #xの右が通路かつCLに居ないときOLにその座標を追加
        OL.append([x[0],x[1]+1])
    return OL #OLを返却

#迷路探索アルゴリズム
def maze_exploration(filename):
    f = open(filename) #引数に取ったファイルを読み込み

    #迷路データを2次元リストmazeに格納
    maze = list()
    for line in f.read().splitlines():
        ln = list(line)
        maze.append(ln)

    OL = deque() #観測可能な未探索座標
    CL = deque() #探索済みの座標
    x = [] #現在位置の座標（スタート位置は[1,1]に設定）
    count = 0 #計算量
    list_size = 0 #リストサイズ
    OL.append([1,1]) #CLにスタート位置を登録

    #迷路探索部分
    while(x != [MAZE_SIZE-1,MAZE_SIZE-1]):

        #OLが空になった(探索可能領域が消えた)場合は探索失敗とみなし、終了する
        if(OL == []):
            print("FAILED...")
            return
        
        x = OL.pop() #xをOLからポップした座標で更新
        maze[x[0]][x[1]]= '#' #探索済みの領域を'#'に変換
        CL.append(x) #CLに現在位置の座標を格納
        next(x, CL, OL, maze) #関数nextの実行
        
        count += 1 #計算量を1増加
        if list_size < len(OL): #OLの要素数の最大値をリストサイズに格納
            list_size = len(OL)

    maze[x[0]][x[1]]= '#' #探索済みの領域を'#'に変換

    # print("GOAL! 計算量:%d リストサイズ:%d" %(count, list_size)) #ゴールしたこと、計算量、リストサイズを出力
    
    if sys.argv[1] == "test":
        #探索経路を標準出力
        for i in range(MAZE_SIZE+1):
            maze[i] = ''.join(map(str,maze[i]))
        [print(i) for i in maze]

    return count, list_size #計算量とリストサイズを返却

#main
sum_count = [] #各試行における計算量のリスト
sum_list_size = [] #各試行におけるリストサイズのリスト
maze_result = () #関数maze_explorationの返り値

if sys.argv[1] == "test": #テスト用ファイルの実行部分
    maze_exploration("Maze/map1010")

if sys.argv[1] == "run": #実験用ファイルの実行部分
    for i in range(100):
        filename = "Maze/mazedata/map"+str(i) #Maze/mazedata/map'i'(iは100以下の任意の自然数)を開く
        maze_result = maze_exploration(filename)
        sum_count.append(maze_result[0]) #返り値の内、計算量を格納
        sum_list_size.append(maze_result[1]) #返り値の内、リストサイズを格納

    #各種結果の出力
    print("深さ優先探索")
    print("計算量の・・・■平均:%.2f ■分散:%.2f ■最悪値:%d ■最良値:%d" 
        %(statistics.mean(sum_count), statistics.pvariance(sum_count), max(sum_count), min(sum_count)))
    print("リストサイズの・・・■平均:%.2f ■分散:%.2f ■最悪値:%d ■最良値:%d"
        %(statistics.mean(sum_list_size), statistics.pvariance(sum_list_size), max(sum_list_size), min(sum_list_size)))
