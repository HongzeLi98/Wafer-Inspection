# coding=utf-8

from core.pt_mrcnn_inference import TagMRCNNDetection as TagAlg
import itertools

class MrcnnAlg:
    def __init__(self, **kwargs):
        self._alg_core = TagAlg(**kwargs)
        self.visualize = kwargs.get('visualize', False)


    def close(self):
        self._alg_core.close()


    def run(self, images_data, **kwargs):
        '''
        批量预测需要用到config中的参数，如batch_size_inference，所以数据放到_alg_core中处理
        :param images_data:
        :param kwargs:
        :return:
        '''
        image_num = len(images_data)
        if image_num == 0:
            return []
        # batch inference
        result = self._alg_core.run(images_data, **kwargs) # result 与images_data一一对应

        if self.visualize:
            return result
        # [[标签,顶点1列像素位置,顶点1行像素位置,顶点2列像素位置,顶点2行像素位置,...], ['ok',x1,y1,x2,y2,...], ...]
        # ([第一张照片IPTC格式],[第二张照片IPTC格式], ...)
        # [
        # {'image_info': {'width': 537, 'height': 483},
        # 'bboxes': [[117.81317901611328, 71.67876434326172, 145.26840209960938, 105.46537017822266], [33.48183822631836, 373.7084045410156, 49.63480758666992, 399.57379150390625], [31.799047470092773, 396.99407958984375, 51.65535354614258, 411.7847900390625]],
        # 'polygons': [[[124, 72], [123, 73], [122, 74], [121, 75], [121, 76], [120, 77], [120, 78], [119, 79], [119, 80], [119, 81], [119, 82], [118, 83], [118, 84], [118, 85], [118, 86], [119, 87], [36, 397], [35, 397]]],
        #  'labels': ['ng_color', 'ng_color', 'ng_color'],
        # 'scores': [0.999810516834259, 0.9894576668739319, 0.656844973564148]},
        all_result = []
        for one_info in result: # one image
            #bboxes = one_info['bboxes']
            polygons = one_info['polygons']
            labels = one_info['labels']
            num = len(one_info['scores'])
            one_result = []
            for idx in range(num): # one object
                polygon = polygons[idx]
                if isinstance(polygon, int): # don't do it
                    continue
                #bbox = bboxes[idx]
                if not isinstance(polygon[0], (list, tuple)):
                    polygon = [polygon]
                polygon = list(itertools.chain.from_iterable(polygon)) # int error
                label = labels[idx]
                polygon.insert(0, label)
                one_result.append(polygon)
            all_result.append(one_result)
        all_result = tuple(all_result)
        # if None all_result = ([],)
        return all_result
