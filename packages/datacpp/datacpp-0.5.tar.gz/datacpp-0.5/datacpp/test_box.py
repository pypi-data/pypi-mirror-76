import datacpp.dataloader as dataloader
import datacpp.libdatacpp as data
import numpy as np
import cv2
import time

if __name__=="__main__":
    label_type=data.LABEL_TYPE.DETECTION
    batch=dataloader.data_batch(label_type,False)
    batch.init_batch()
    for i in range(100):
        start=time.time()
        batch_data=batch.next_batch()
        end=time.time()
        print("time:{}--{}".format(i,end-start))
        if batch_data is None:
            batch.init_batch()
            continue
        images=batch_data[0]
        labels=batch_data[1]
        for i in range(len(images)):
            height,width,_=images[i].shape
            for j in range(len(labels[i])):
                box=labels[i][j]
                for t in range(4):
                    if t%2==0:
                        box[t]=int(box[t]*width)
                    else:
                        box[t]=int(box[t]*height)
                cv2.rectangle(images[i],(box[0],box[1]),(box[2],box[3]),(255,0,0),thickness=1)
                cv2.putText(images[i],str(box[4]),(box[0],box[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))
            cv2.imshow("images:",images[i])
            cv2.waitKey(0)