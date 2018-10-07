import cv2
import os  
os.environ['GLOG_minloglevel'] = '3'
import caffe
import numpy as np
import time

import sys
sys.path.append('./mtcnn')
from mtcnn.Detection.MtcnnDetector import MtcnnDetector
from mtcnn.Detection.detector import Detector
from mtcnn.Detection.fcn_detector import FcnDetector
from mtcnn.train_models.mtcnn_model import P_Net, R_Net, O_Net
from mtcnn.prepare_data.loader import TestLoader

class FaceEntry:
    def __init__(self, model='final', gpu=True, min_face_size = 24):
        # for detector
        thresh = [0.9, 0.6, 0.7]
        stride = 2
        slide_window = False
        shuffle = False
        detectors = [None, None, None]
        prefix = ['mtcnn/data/MTCNN_model/PNet_landmark/PNet', 'mtcnn/data/MTCNN_model/RNet_landmark/RNet', 'mtcnn/data/MTCNN_model/ONet_landmark/ONet']
        epoch = [18, 14, 16]
        batch_size = [2048, 256, 16]
        model_path = ['%s-%s' % (x, y) for x, y in zip(prefix, epoch)]
        # load pnet model
        if slide_window:
            PNet = Detector(P_Net, 12, batch_size[0], model_path[0])
        else:
            PNet = FcnDetector(P_Net, model_path[0])
        detectors[0] = PNet

        RNet = Detector(R_Net, 24, batch_size[1], model_path[1])
        detectors[1] = RNet

        ONet = Detector(O_Net, 48, batch_size[2], model_path[2])
        detectors[2] = ONet

        self.mtcnn_detector = MtcnnDetector(detectors=detectors, min_face_size=min_face_size,
                               stride=stride, threshold=thresh, slide_window=slide_window)

        # for aligner
        if not gpu:
            caffe.set_mode_cpu()
        else:
            caffe.set_mode_gpu()
            caffe.set_device(0)
        self.model = model
        if (model == 'final'):
            self.net = caffe.Net('lab/models/WFLW/WFLW_final/rel.prototxt', 'lab/models/WFLW/WFLW_final/model.bin', caffe.TEST)
        else:
            self.net = caffe.Net('lab/models/WFLW/WFLW_wo_mp/rel.prototxt', 'lab/models/WFLW/WFLW_wo_mp/model.bin', caffe.TEST)

    def process_image(self, img_name):
        im = cv2.imread(img_name)
        test_data = TestLoader([img_name])
        t0 = time.time()
        all_boxes,landmarks = self.mtcnn_detector.detect_face(test_data)
        print('detect:', time.time() - t0)
        boxes = all_boxes[0]
        num_boxes = len(boxes)
        res_boxes = []
        res_lands = []
        res_paths = []
        for i in range(num_boxes):
            if boxes[i, 4] > 0.6:
                scale = im.shape[1] * 1.0 / 200
                box = np.copy(boxes[i]) * scale
                #print('org box', box)
                toffset = 0.05 * (box[3] - box[1])
                boffset = 0.2 * (box[3] - box[1])
                loffset = 0.15 * (box[2] - box[0])
                roffset = 0.15 * (box[2] - box[0])
                box[1] = box[1] + toffset
                box[3] = box[3] + boffset
                box[0] = box[0] - loffset
                box[2] = box[2] + roffset
                box = [max(0, box[0]), max(0, box[1]), min(im.shape[1], box[2]), min(im.shape[0], box[3])]
                length = max(box[2] - box[0], box[3] - box[1])
                if length < 120:
                    print(img_name, ' face too small')
                    continue
                center = [(box[0] + box[2]) / 2, (box[1] + box[3]) / 2]
                #print('center=', center, 'length=', length)
                length = min(min(center[0], min(center[1], min(im.shape[1] - center[0], im.shape[0] - center[1]))) - 1, length / 2) * 2
                rbox = np.array([center[0] - length / 2, center[1] - length / 2, center[0] + length / 2, center[1] + length / 2], dtype=int)
                #print('rbox', rbox)
                rimg = im[rbox[1]:rbox[3], rbox[0]:rbox[2]]
                gim = cv2.resize(rimg, (256, 256))
                gim = cv2.cvtColor(gim, cv2.COLOR_BGR2GRAY)
                gim = np.float32(gim)
                nim = self._normalize_image(gim)
                self.net.blobs['data'].data[...] = nim
                t0 = time.time()
                out = self.net.forward()['result'][0].reshape((-1, 2))
                print('align:', time.time() - t0)
                nout = np.array(out, dtype=float)
                nout[:, 0] = nout[:, 0] * length / 256 + rbox[0]
                nout[:, 1] = nout[:, 1] * length / 256 + rbox[1]
                vim = np.copy(im)
                cv2.line(vim, (rbox[0], rbox[1]), (rbox[2], rbox[1]), (0, 255, 255), 2)
                cv2.line(vim, (rbox[2], rbox[1]), (rbox[2], rbox[3]), (0, 255, 255), 2)
                cv2.line(vim, (rbox[2], rbox[3]), (rbox[0], rbox[3]), (0, 255, 255), 2)
                cv2.line(vim, (rbox[0], rbox[3]), (rbox[0], rbox[1]), (0, 255, 255), 2)
                for pt in nout:
                    cv2.circle(vim, ((int)(pt[0]), (int)(pt[1])), 1, (255, 255, 0), -1)
                res_path = '/static/res/res_' + str(time.time()) + '_' + str(i) + '.jpg'
                cv2.imwrite('/var/www/demoapp' + res_path, vim)
                res_boxes.append(rbox)
                res_lands.append(nout)
                res_paths.append(res_path)
        return np.array(res_boxes), np.array(res_lands), res_paths

    def _normalize_image(self, im):
        mean, std = cv2.meanStdDev(im)
        if std[0, 0] < 1e-6:
            std[0, 0] = 1
        # nim = cv2.convertScaleAbs(im, cv2.CV_32F, 1.0/std[0, 0], -1*mean[0, 0]/std[0, 0])
        nim = im * 1.0/std[0, 0] - 1*mean[0, 0]/std[0, 0]
        # print(1.0/std[0, 0], -1*mean[0, 0]/std[0, 0])
        return nim
facer = FaceEntry()
if __name__ == '__main__':
    face = FaceEntry()
    t0 = time.time()
    face.process_image('test.jpg')
    print(time.time() - t0)
    t0 = time.time()
    face.process_image('test.jpg')
    print(time.time() - t0)
