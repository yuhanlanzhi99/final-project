#coding:gbk


import codecs
import jieba.posseg as pseg
import jieba

names = {}#  ���������Ϊ�������ƣ�ֵΪ��������ȫ���г��ֵĴ���
relationships = {}#���������ϵ������ߣ���Ϊ����ߵ���㣬ֵΪһ���ֵ� edge ��edge �ļ�Ϊ����ߵ��յ㣬ֵ������ߵ�Ȩֵ
lineNames = []# ��������������ÿһ�ηִʵõ���ǰ���г��ֵ���������

jieba.load_userdict("names.txt")#���������
f2=open("names.txt", "r", encoding='utf-8').read()
#file2=f2.read()
with codecs.open("���������Ľֵ�.txt", 'r', 'utf8') as f:
    for line in f.readlines():
        poss = pseg.cut(line)  # �ִʣ����ش���
        lineNames.append([])  # Ϊ��������һ�������б�
        for w in poss:
            if len(w.word) < 2 or w.word not in f2:
                continue  # ���ִʳ���С��2��ôʴ��Բ�Ϊnr��������ʱ��Ϊ�ôʲ�Ϊ����
            lineNames[-1].append(w.word)  # Ϊ��ǰ�εĻ�������һ������
            if names.get(w.word) is None:  # ���ĳ���w.word�����������ֵ���
                names[w.word] = 0
                relationships[w.word] = {}
            names[w.word] += 1
            # ���������ִ���ͳ�ƽ��
for name, times in names.items():
    print(name, times)

# ���� lineNames ��ÿһ�У�����Ϊ�����г��ֵ������������������������������֮����δ�б߽��������½��ı�Ȩֵ��Ϊ 1��
# �����Ѵ��ڵıߵ�Ȩֵ�� 1�����ַ����������ܶ������ߣ���Щ����߽��������
for line in lineNames:
    for name1 in line:
        for name2 in line:
            if name1 == name2:
                continue
            if relationships[name1].get(name2) is None:
                relationships[name1][name2] = 1
            else:
                relationships[name1][name2] = relationships[name1][name2] + 1
                # ���ڷִʵĲ�׼ȷ����ֺܶ಻�������ġ����������Ӷ����³��ֺܶ�����ߣ�
                # Ϊ�˿�������ֵΪ10�������߳���10����������Ϊ��������
with codecs.open("People_node.txt", "w", "utf8") as f:
    f.write("ID Label Interval\r\n")
    for name, times in names.items():
        if times > 6:
            f.write(name + " " + name + " " + str(times) + "\r\n")
with codecs.open("People_edge.txt", "w", "utf8") as f:
    f.write("Source Target Weight\r\n")
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 6:
                f.write(name + " " + v + " " + str(w) + "\r\n")
