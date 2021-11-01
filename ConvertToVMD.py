import csv
import math
import struct
import sys

def EulerToQuaternion(roll,pitch,yaw):
    cosRoll = math.cos(roll/2.0)
    sinRoll = math.sin(roll/2.0)
    cosPitch = math.cos(pitch/2.0)
    sinPitch = math.sin(pitch/2.0)
    cosYaw = math.cos(yaw/2.0)
    sinYaw = math.sin(yaw/2.0)

    q0 = cosRoll * cosPitch * cosYaw + sinRoll * sinPitch *sinYaw
    q1 = sinRoll * cosPitch * cosYaw - cosRoll * sinPitch * sinYaw
    q2 = cosRoll * sinPitch * cosYaw + sinRoll * cosPitch * sinYaw
    q3 = cosRoll * cosPitch * sinYaw - sinRoll * sinPitch * cosYaw

    return q0,q1,q2,q3

infile = sys.argv[1]#コマンドライン引数をソースファイルに指定
outfile = sys.argv[1]+'.vmd'#書き出しファイル名を指定

with open(infile,'r',encoding='utf-8') as sf:#ファイルを開く
    reader = csv.reader(sf)#データ読み込み
    line = [row for row in reader]#格納
sf.close()

with open(outfile,mode='wb') as of:#上書きモードでファイルを開く
    pass
of.close()#一度閉じる

with open(outfile,mode='a+b') as of:#追記モードで開く
    header = struct.pack('30s20s','Vocaloid Motion Data 0002'.encode('shift-jis'),'初音ミク'.encode('shift-jis'))
    of.write(header)#headerの書き込み
of.close()

tline = [list(x) for x in zip(*line)]#lineの転置

frame = len(tline[0])-2#モーションの総フレーム数

print(frame)

nameConv = {'SPINE_NAVAL':'上半身','PELVIS':'下半身','HEAD':'頭','NECK':'首','SPINE_CHEST':'上半身2','CLAVICLE_LEFT':'左肩','SHOULDER_LEFT':'左腕','ELBOW_LEFT':'左ひじ','WRIST_LEFT':'左手首','CLAVICLE_RIGHT':'右肩','SHOULDER_RIGHT':'右腕','ELBOW_RIGHT':'右ひじ','WRIST_RIGHT':'右手首','HIP_LEFT':'左足','KNEE_LEFT':'左ひざ','ANKLE_LEFT':'左足首','FOOT_LEFT':'左つま先','HIP_RIGHT':'右足','KNEE_RIGHT':'右ひざ','ANKLE_RIGHT':'右足首','FOOT_RIGHT':'右つま先','THUMB_LEFT':'左親指2','THUMB_RIGHT':'右親指2','HANDTIP_LEFT':'左人指3','HANDTIP_RIGHT':'右人指3','EYE_LEFT':'左目','EYE_RIGHT':'右目','HAND_LEFT':'左手先','HAND_RIGHT':'右手先'}#基本的な名前変換

childDic = {'SPINE_CHEST':'NECK','NECK':'HEAD','CLAVICLE_LEFT':'SHOULDER_LEFT','SHOULDER_LEFT':'ELBOW_LEFT','ELBOW_LEFT':'WRIST_LEFT','WRIST_LEFT':'HAND_LEFT','CLAVICLE_RIGHT':'SHOULDER_RIGHT','SHOULDER_RIGHT':'ELBOW_RIGHT','ELBOW_RIGHT':'WRIST_RIGHT','WRIST_RIGHT':'HAND_RIGHT','HIP_LEFT':'KNEE_LEFT','KNEE_LEFT':'ANKLE_LEFT','ANKLE_LEFT':'FOOT_LEFT','HIP_RIGHT':'KNEE_RIGHT','KNEE_RIGHT':'ANKLE_RIGHT','ANKLE_RIGHT':'FOOT_RIGHT'}#ボーンの親子関係 親:子

movePlace = {'ANKLE_LEFT':'左足ＩＫ','ANKLE_RIGHT':'右足ＩＫ'}#位置情報を入力するボーン

with open(outfile,mode='a+b') as of:#追記モードで開く
    sizeOfOutput = frame * (len(childDic)+len(movePlace))
    bsizeout = struct.pack('i',sizeOfOutput)
    of.write(bsizeout)#モーションデータ数の書き込み
of.close()

ofx = 1000
ofy = 1000
ofz = 1000

for x in range(1,96,3):
    if line[0][x] in childDic.keys():#ソースファイルから親を検索
        print('Found '+line[0][x]+' in childDic.')
        for j in range(frame):#一フレームずつ書き込み
            if j < frame-1:#ごめん、最後のフレームは消えます
                for k in range(1,96,3):#ソースファイルから子を検索
                    if line[0][k] == childDic[line[0][x]]:
                        break
                #2点間の位置から方向を計算
                ofZ = float(line[j+2][k+2])-float(line[j+2][x+2])
                ofX = float(line[j+2][k])-float(line[j+2][x])
                ofY = float(line[j+2][k+1])-float(line[j+2][x+1])
                distZX = math.sqrt((ofZ*ofZ)+(ofX*ofX))
                distXY = math.sqrt((ofX*ofX)+(ofY*ofY))
                distYZ = math.sqrt((ofY*ofY)+(ofZ*ofZ))
                radX = math.atan2(ofZ,ofY)
                radY = math.atan2(ofZ,ofX)
                radZ = math.atan2(ofY,ofX)
                #クォータニオンに変換
                q0,q1,q2,q3 = EulerToQuaternion(radX,radY,radZ)
            with open(outfile,mode='a+b') as of:#追記モードで開く
                bnameout = struct.pack('15s',nameConv[line[0][x]].encode('shift-jis'))
                bframeout = struct.pack('i',j+1)
                bposout = struct.pack('fff',0,0,0)
                bquaout = struct.pack('ffff',q1,q2,q3,q0)
                bfillout = struct.pack('64p',b'0')
                of.write(bnameout)
                of.write(bframeout)
                of.write(bposout)
                of.write(bquaout)
                of.write(bfillout)
                #モーションデータ数の書き込み
            of.close()


    if line[0][x] in movePlace.keys():#ソースファイルから位置を動かすボーンを検索
        print('Found '+line[0][x]+' in place.')
        for j in range(frame):
            if j < frame-1:
                if line[0][x] in childDic.keys():#方向を求めるため子を検索
                    for k in range(1,96,3):
                        if line[0][k] == childDic[line[0][x]]:
                            break
                    #2点間の位置から方向を計算
                    ofZ = float(line[j+2][k+2])-float(line[j+2][x+2])
                    ofX = float(line[j+2][k])-float(line[j+2][x])
                    ofY = float(line[j+2][k+1])-float(line[j+2][x+1])
                    radX = math.atan2(ofZ,ofY)
                    radY = math.atan2(ofZ,ofX)
                    radZ = math.atan2(ofY,ofX)
                    #クォータニオンに変換
                    q0,q1,q2,q3 = EulerToQuaternion(radX,radY,radZ)
                with open(outfile,mode='a+b') as of:#追記モードで開く
                    bnameout = struct.pack('15s',nameConv[line[0][x]].encode('shift-jis'))
                    bframeout = struct.pack('i',j+1)
                    bposout = struct.pack('fff',float(line[j+2][x])/ofx,float(line[j+2][x+2])/ofy,float(line[j+2][x+1])/ofz)
                    bquaout = struct.pack('ffff',q1,q2,q3,q0)
                    bfillout = struct.pack('64p',b'0')
                    of.write(bnameout)
                    of.write(bframeout)
                    of.write(bposout)
                    of.write(bquaout)
                    of.write(bfillout)
                    #モーションデータ数の書き込み
                of.close()

with open(outfile,mode='a+b') as of:#追記モードで開く
    numberOfskindata = struct.pack('i',0)
    of.write(numberOfskindata)
    numberOfcameradata = struct.pack('i',0)
    of.write(numberOfcameradata)
    numberOflightdata = struct.pack('i',0)
    of.write(numberOflightdata)
    numberOfshadowdata = struct.pack('i',0)
    of.write(numberOfshadowdata)
of.close()
