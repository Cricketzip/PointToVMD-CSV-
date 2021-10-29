import csv #csvモジュールの読み込み(1)

file = '20211027164608.csv' #ファイルのパスを指定(2)
ofile = 'output.csv'

with open(file,'r',encoding='UTF-8') as f: #ファイルをオープン(3)
    reader = csv.reader(f) #ファイルからデータを読み込み(4)
    line = [row for row in reader]




print(line[0])

tline = [list(x) for x in zip(*line)]

print(tline[0])

frame = len(tline[0])-2

nameConv = {'SPINE_NAVAL':'上半身','PELVIS':'下半身','HEAD':'頭','NECK':'首','SPINE_CHEST':'上半身2','CLAVICLE_LEFT':'左肩','SHOULDER_LEFT':'左腕','ELBOW_LEFT':'左ひじ','WRIST_LEFT':'左手首','CLAVICLE_RIGHT':'右肩','SHOULDER_RIGHT':'右腕','ELBOW_RIGHT':'右ひじ','WRIST_RIGHT':'右手首','HIP_LEFT':'左足','KNEE_LEFT':'左ひざ','ANKLE_LEFT':'左足首','HIP_RIGHT':'右足','KNEE_RIGHT':'右ひざ','ANKLE_RIGHT':'右足首','THUMB_LEFT':'左親指2','THUMB_RIGHT':'右親指2','HANDTIP_LEFT':'左人指3','HANDTIP_RIGHT':'右人指3'}

sizeOfOutput = frame * 24
print(sizeOfOutput)

output = [[0 for i in range(9)] for j in range(sizeOfOutput+6)]
format(output)

indexOutput = 3

output[0][0] = 'Vocaloid Motion Data 0002'
output[1][0] = '初音ミク'
output[2][0] = sizeOfOutput

for x in range(1,96,3):
    if line[0][x] in nameConv.keys():
        for j in range(frame):
            output[indexOutput][0] = nameConv[line[0][x]]
            output[indexOutput][1] = j+1
            if j < frame-1:
                output[indexOutput][2] = float(line[j+2][x+1])/1000
                output[indexOutput][3] = float(line[j+2][x+2])/1000
                output[indexOutput][4] = float(line[j+2][x])/1000
            indexOutput = indexOutput + 1


of = open(ofile,'w',newline='',encoding='shift-jis')
writer = csv.writer(of)
writer.writerows(output)



of.close()
f.close() #開いたファイルをクローズ(7)
