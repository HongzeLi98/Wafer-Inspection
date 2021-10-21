#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from kernel import xx_inference


class XXAlg(object):
    def __init__(self, **kwargs):

        self._alg_core = xx_inference.TagXXXX(**kwargs)

    def close(self):

        self._alg_core.close()

    def run(self, images_data, **kwargs):

        limit_num = kwargs.get('RUN_batch_num', 1)
        result_bbox = []
        image_num = len(images_data)
        if image_num == 0:
            return result_bbox

        sub_image_list,batch_image_list = [],[]
        for i,image_data in enumerate(images_data):
            sub_image = self._alg_core.image_preproces(image_data)


            sub_image_list.append(sub_image)
            if i % limit_num == limit_num - 1 or i == image_num - 1:
                batch_image_list.append(sub_image_list)
                sub_image_list = []

        result = []
        for i, batch_data in enumerate(batch_image_list):
            run_result = self._alg_core.run(np.array(batch_data), **kwargs)
            result += run_result.tolist()

        return result

