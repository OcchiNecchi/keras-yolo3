import xml.etree.ElementTree as ET
from os import getcwd
import sys,os
sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["blousonjacket","coat","pants","parker","polo_shirt","shoes","t_shirt","tailoredjacket","tie","y_shirt"]

# 一応引数でもタグを指定できる。
if len(sys.argv) > 1:
    classes = sys.argv[1:]

with open('model_data/voc_classes.txt','w') as f:
    f.write('\n'.join(classes))

def convert_annotation(year, image_id, list_file):
    image_id = image_id.split('.')
    in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id[0]))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), 
            int(float(xmlbox.find('ymin').text)), 
            int(float(xmlbox.find('xmax').text)), 
            int(float(xmlbox.find('ymax').text)))
        
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()

for year, image_set in sets:
    image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    list_file = open('model_data/%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        if image_id == '1': continue
        if image_id == '-1': continue
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg'%(wd, year, image_id))
        convert_annotation(year, image_id, list_file)
        list_file.write('\n')
    list_file.close()

