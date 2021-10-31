import csv #csvモジュールの読み込み(1)
import math

file = '20211027164608.csv' #ファイルのパスを指定(2)
ofile = 'output.csv'

with open(file,'r',encoding='UTF-8') as f: #ファイルをオープン(3)
    reader = csv.reader(f) #ファイルからデータを読み込み(4)
    line = [row for row in reader]


tline = [list(x) for x in zip(*line)]

frame = len(tline[0])-2

print('frame : '+str(frame))

nameConv = {'SPINE_NAVAL':'上半身','PELVIS':'下半身','HEAD':'頭','NECK':'首','SPINE_CHEST':'上半身2','CLAVICLE_LEFT':'左肩','SHOULDER_LEFT':'左腕','ELBOW_LEFT':'左ひじ','WRIST_LEFT':'左手首','CLAVICLE_RIGHT':'右肩','SHOULDER_RIGHT':'右腕','ELBOW_RIGHT':'右ひじ','WRIST_RIGHT':'右手首','HIP_LEFT':'左足','KNEE_LEFT':'左ひざ','ANKLE_LEFT':'左足首','FOOT_LEFT':'左つま先','HIP_RIGHT':'右足','KNEE_RIGHT':'右ひざ','ANKLE_RIGHT':'右足首','FOOT_RIGHT':'右つま先','THUMB_LEFT':'左親指2','THUMB_RIGHT':'右親指2','HANDTIP_LEFT':'左人指3','HANDTIP_RIGHT':'右人指3','EYE_LEFT':'左目','EYE_RIGHT':'右目','HAND_LEFT':'左手先','HAND_RIGHT':'右手先'}

nameConv2 = {'ANKLE_LEFT':'左足ＩＫ','ANKLE_RIGHT':'右足ＩＫ','SPINE_NAVAL':'センター','FOOT_LEFT':'左つま先ＩＫ','FOOT_RIGHT':'右つま先ＩＫ','KNEE_LEFT':'左ひざD','KNEE_RIGHT':'右ひざD','HIP_LEFT':'左足D','HIP_RIGHT':'右足D','CLAVICLE_LEFT':'左肩P','CLAVICLE_RIGHT':'右肩P','SHOULDER_LEFT':'左肩C','SHOULDER_RIGHT':'右肩C'}

nameConv3 = {'SPINE_NAVAL':'グループ','ANKLE_LEFT':'左足首D','ANKLE_RIGHT':'右足首D'}

childDic = {'SPINE_CHEST':'NECK','NECK':'HEAD','CLAVICLE_LEFT':'SHOULDER_LEFT','SHOULDER_LEFT':'ELBOW_LEFT','ELBOW_LEFT':'WRIST_LEFT','WRIST_LEFT':'HAND_LEFT','CLAVICLE_RIGHT':'SHOULDER_RIGHT','SHOULDER_RIGHT':'ELBOW_RIGHT','ELBOW_RIGHT':'WRIST_RIGHT','WRIST_RIGHT':'HAND_RIGHT','HIP_LEFT':'KNEE_LEFT','KNEE_LEFT':'ANKLE_LEFT','ANKLE_LEFT':'FOOT_LEFT','HIP_RIGHT':'KNEE_RIGHT','KNEE_RIGHT':'ANKLE_RIGHT','ANKLE_RIGHT':'FOOT_RIGHT'}

place = {'ANKLE_LEFT':'左足ＩＫ','ANKLE_RIGHT':'右足ＩＫ','FOOT_LEFT':'左つま先ＩＫ','FOOT_RIGHT':'右つま先ＩＫ'}

sizeOfOutput = frame * (len(nameConv)+len(nameConv2)+len(nameConv3))
print('size : '+str(sizeOfOutput))

output = [[0 for i in range(9)] for j in range(sizeOfOutput+6)]
format(output)

indexOutput = 3

output[0][0] = 'Vocaloid Motion Data 0002'
output[1][0] = '初音ミク'
output[2][0] = sizeOfOutput

ofx = 1000
ofy = 1000
ofz = 1000

for x in range(1,96,3):
    if line[0][x] in childDic.keys():
        print('Found '+line[0][x]+' in childDic.')
        for j in range(frame):
            output[indexOutput][0] = nameConv[line[0][x]]
            output[indexOutput][1] = j+1
            if j < frame-1:
                for k in range(1,96,3):
                    if line[0][k] == childDic[line[0][x]]:
                        break
                ofZ = float(line[j+2][k+2])-float(line[j+2][x+2])
                ofX = float(line[j+2][k])-float(line[j+2][x])
                ofY = float(line[j+2][k+1])-float(line[j+2][x+1])
                distZX = math.sqrt((ofZ*ofZ)+(ofX*ofX))
                distXY = math.sqrt((ofX*ofX)+(ofY*ofY))
                distYZ = math.sqrt((ofY*ofY)+(ofZ*ofZ))
                radX = math.asin(ofZ/distYZ)
                radY = math.asin(ofZ/distZX)
                radZ = math.asin(ofY/distXY)
                if line[j+2][k+1]>line[j+2][x+1]:
                    output[indexOutput][5] = -(math.degrees(radX)+90)
                else:
                    output[indexOutput][5] = (math.degrees(radX)+90)
                if line[j+2][k]<line[j+2][x]:
                    output[indexOutput][6] = -(math.degrees(radY)-90)
                else:
                    output[indexOutput][6] = math.degrees(radY)-90
                #if line[j+2][k+2]>line[j+2][x+2]:
                    #output[indexOutput][7] = -(math.degrees(radZ))
                #else:
                    #output[indexOutput][7] = math.degrees(radZ)
            indexOutput = indexOutput + 1

    if line[0][x] in place.keys():
        print('Found '+line[0][x]+' in place.')
        for j in range(frame):
            output[indexOutput][0] = place[line[0][x]]
            output[indexOutput][1] = j+1
            if j < frame-1:
                output[indexOutput][2] = float(line[j+2][x])/ofx
                output[indexOutput][3] = float(line[j+2][x+2])/ofy
                output[indexOutput][4] = float(line[j+2][x+1])/ofz
                if line[0][x] in childDic.keys():
                    for k in range(1,96,3):
                        if line[0][k] == childDic[line[0][x]]:
                            break
                    ofZ = float(line[j+2][k+2])-float(line[j+2][x+2])
                    ofX = float(line[j+2][k])-float(line[j+2][x])
                    ofY = float(line[j+2][k+1])-float(line[j+2][x+1])
                    distZX = math.sqrt((ofZ*ofZ)+(ofX*ofX))
                    distXY = math.sqrt((ofX*ofX)+(ofY*ofY))
                    distYZ = math.sqrt((ofY*ofY)+(ofZ*ofZ))
                    radX = math.asin(ofZ/distYZ)
                    radY = math.asin(ofZ/distZX)
                    radZ = math.asin(ofY/distXY)
                    if line[j+2][k+1]>line[j+2][x+1]:
                        output[indexOutput][5] = -(math.degrees(radX)+90)
                    else:
                        output[indexOutput][5] = (math.degrees(radX)+90)
                    if line[j+2][k]<line[j+2][x]:
                        output[indexOutput][6] = -(math.degrees(radY)-90)
                    else:
                        output[indexOutput][6] = math.degrees(radY)-90
                    #if line[j+2][k+2]>line[j+2][x+2]:
                        #output[indexOutput][7] = -(math.degrees(radZ))
                    #else:
                        #output[indexOutput][7] = math.degrees(radZ)
            indexOutput = indexOutput + 1



of = open(ofile,'w',newline='',encoding='shift-jis')
writer = csv.writer(of)
writer.writerows(output)



of.close()
f.close() #開いたファイルをクローズ(7)
