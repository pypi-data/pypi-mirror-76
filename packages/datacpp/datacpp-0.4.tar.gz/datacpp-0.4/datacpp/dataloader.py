import datacpp.pipeline as pipeline
import datacpp.libdatacpp as data

class data_batch:
    def __init__(self,label_type,heatmap):
        batch_size=32
        file_name="D:/datasets/VOC/VOCdevkit/VOC2012/ImageSets/Main/train.txt"
        label_name="D:/datasets/VOC/VOCdevkit/class.txt"
        image_dir="D:/datasets/VOC/VOCdevkit/VOC2012/JPEGImages/"
        label_dir="D:/datasets/VOC/VOCdevkit/VOC2012/Annotations/"
        self.label_type=label_type
        self.heatmap=False
        self.pipe=pipeline.pipeline(batch_size,file_name,label_name,image_dir,label_dir,self.label_type,heatmap=self.heatmap)
    def init_batch(self):
        self.pipe.producer()
    def next_batch(self,i):
        return self.pipe.consumer(i)