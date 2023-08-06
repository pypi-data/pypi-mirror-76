import datacpp.pipeline as pipeline
import datacpp.libdatacpp as data

class data_batch:
    def __init__(self,file_name,label_name,image_dir,label_dir,batch_size,label_type,heatmap=False):
        self.pipe=pipeline.pipeline(batch_size,file_name,label_name,image_dir,label_dir,self.label_type,heatmap=self.heatmap)
    def init_batch(self):
        self.pipe.producer()
    def next_batch(self,i):
        return self.pipe.consumer(i)