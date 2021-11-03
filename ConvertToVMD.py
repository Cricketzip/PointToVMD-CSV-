import csv
import math
import struct
import sys
import time

t1 = time.time()

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

with open(outfile,'w') as of:
    pass

with open(outfile,mode='ab') as of:#追記モードで開く

    header = struct.pack('30s20s','Vocaloid Motion Data 0002'.encode('shift-jis'),'Original'.encode('shift-jis'))
    of.write(header)#headerの書き込み

    tline = [list(x) for x in zip(*line)]#lineの転置

    frame = len(tline[0])-2#モーションの総フレーム数

    nameConv = {'SPINE_NAVAL':'上半身','PELVIS':'下半身','HEAD':'頭','NECK':'首','SPINE_CHEST':'上半身2','CLAVICLE_LEFT':'左肩','SHOULDER_LEFT':'左腕','ELBOW_LEFT':'左ひじ','WRIST_LEFT':'左手首','CLAVICLE_RIGHT':'右肩','SHOULDER_RIGHT':'右腕','ELBOW_RIGHT':'右ひじ','WRIST_RIGHT':'右手首','HIP_LEFT':'左足','KNEE_LEFT':'左ひざ','ANKLE_LEFT':'左足首','FOOT_LEFT':'左つま先','HIP_RIGHT':'右足','KNEE_RIGHT':'右ひざ','ANKLE_RIGHT':'右足首','FOOT_RIGHT':'右つま先','THUMB_LEFT':'左親指2','THUMB_RIGHT':'右親指2','HANDTIP_LEFT':'左人指3','HANDTIP_RIGHT':'右人指3','EYE_LEFT':'左目','EYE_RIGHT':'右目','HAND_LEFT':'左手先','HAND_RIGHT':'右手先'}#基本的な名前変換

    childDic = {'SPINE_NAVAL':'SPINE_CHEST','SPINE_CHEST':'NECK','NECK':'HEAD','CLAVICLE_LEFT':'SHOULDER_LEFT','SHOULDER_LEFT':'ELBOW_LEFT','ELBOW_LEFT':'WRIST_LEFT','WRIST_LEFT':'HAND_LEFT','CLAVICLE_RIGHT':'SHOULDER_RIGHT','SHOULDER_RIGHT':'ELBOW_RIGHT','ELBOW_RIGHT':'WRIST_RIGHT','WRIST_RIGHT':'HAND_RIGHT','HIP_LEFT':'KNEE_LEFT','KNEE_LEFT':'ANKLE_LEFT','ANKLE_LEFT':'FOOT_LEFT','HIP_RIGHT':'KNEE_RIGHT','KNEE_RIGHT':'ANKLE_RIGHT','ANKLE_RIGHT':'FOOT_RIGHT'}#ボーンの親子関係 親:子

    movePlace = {'ANKLE_LEFT':'左足IK','ANKLE_RIGHT':'右足IK','PELVIS':'センター'}#位置情報を入力するボーン

    sizeOfOutput = frame * (len(childDic)+len(movePlace))
    bsizeout = struct.pack('i',sizeOfOutput)
    of.write(bsizeout)#モーションデータ数の書き込み


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
                    radX = math.atan2(ofZ,ofY)+135
                    radY = math.atan2(ofZ,ofX)+90
                    radZ = 45#math.atan2(ofY,ofX)-90
                    #クォータニオンに変換
                    q0,q1,q2,q3 = EulerToQuaternion(radX,radY,radZ)
                    bnameout = struct.pack('15s',nameConv[line[0][x]].encode('shift-jis'))
                    bframeout = struct.pack('i',j+1)
                    bposout = struct.pack('fff',0,0,0)
                    bquaout = struct.pack('ffff',q1,q2,q3,q0)
                    bfillout = struct.pack('64p',b'0')
                    of.write(bnameout+bframeout+bposout+bquaout+bfillout)
                    #of.write(bframeout)
                    #of.write(bposout)
                    #of.write(bquaout)
                    #of.write(bfillout)
                    #モーションデータ数の書き込み



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
                        radX = math.atan2(ofZ,ofY)+135
                        radY = math.atan2(ofZ,ofX)+90
                        radZ = 45#math.atan2(ofY,ofX)+90
                        #クォータニオンに変換
                        q0,q1,q2,q3 = EulerToQuaternion(radX,radY,radZ)
                        bnameout = struct.pack('15s',movePlace[line[0][x]].encode('shift-jis'))
                        bframeout = struct.pack('i',j+1)
                        bposout = struct.pack('fff',float(line[j+2][x])/ofx,float(line[j+2][x+2])/ofy,float(line[j+2][x+1])/ofz)
                        bquaout = struct.pack('ffff',q1,q2,q3,q0)
                        bfillout = struct.pack('64p',b'0')
                        of.write(bnameout+bframeout+bposout+bquaout+bfillout)
                        #of.write(bframeout)
                        #of.write(bposout)
                        #of.write(bquaout)
                        #of.write(bfillout)
                        #モーションデータ数の書き込み

    numberOfotherdata = struct.pack('iiii',0,0,0,0)
    of.write(numberOfotherdata)

t2 = time.time()
print("Elapsed time："+str(t2-t1))
