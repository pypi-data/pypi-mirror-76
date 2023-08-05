"""
Class for combine multiple prediction nodes based on the output of a main detector model.
The regions output of the detector are passed on other nodes (Classification or detection)
based some rules.

Cascade Prediction Node
 - Get predictions from a main detector
 - Results are passed to specialized classifiers/detector

All the predictions are obtained from other nodes
Classifiers are run in a concurrent requests
Inputs are:
    - Detector node direction
    - Subregion to be cropped from detector result
    - Subregions dict (detector-output : classifier-node)

EXAMPLE
conf:{
    'max_concur_req': 10,
    'main_model':{
        'model': AbcModel
    }
     'sub_models':
        {
            'person':

                [
                    {
                        'model': AbcModel,
                        'weights': (0,0,1,1),
                        'conditions':['square_h']

                    },
                ],
            ...
        }
}
Use *all* for pass all the subregions in a classifier

ROI
    The roi inside the located class by the detector is defined by weights
    Each weight from 0-1 of the values: (xi, yi, w, h)
    Where 0 -> xi | 1 -> xi+W
    Example:
        "roi_weights": (0.1, 1, 0.5, 1),
        "roi_conditions": ["center_x", ],

    - Conditions:
        * center_x: center x direction
        * center_y: center y direction
        * square_w: square to width (after weighted)
        * square_h: square to height (after weighted)


JCA
Vaico
"""
import json
import logging


from MLcommon.PredictionStrategies.auxfunc.cropper import crop_rect


class Cascade:
    """
    Cascade strategy of passing the input for several models to build a final prediction.
    Usually general prediction is returned by a Detector and specialized Classifiers
    run on the output of the detector.
    Instantiate outside lambda_function.
    """
    def __init__(self, conf):
        """
        :param conf: dict with loaded models and crop image configuration
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info('Instantiating Cascade prediction strategy')
        self.conf = conf
    def predict(self, frame):
        # Run detector
        self.logger.info('Predicting with main model on Cascade')
        areas = self.conf['main_model']['model'].predict(frame)

        # Queue prediction: one prediction run after the other
        self.logger.info('Predicting {} areas with {} sub-models'.format(len(areas), len(self.conf['sub_models'])))
        for roi in areas:
            if roi.label in self.conf['sub_models']:
                roi.subobject = []
                for model in self.conf['sub_models'][roi.label]:
                    area = {
                        'xmin': roi.geometry.xmin,
                        'ymin': roi.geometry.ymin,
                        'xmax': roi.geometry.xmax,
                        'ymax': roi.geometry.ymax,
                    }

                    im_crop = crop_rect(
                        frame, 
                        area,
                        model['weights'],
                        model['conditions']
                    )
                    self.logger.debug('Predicting region with: {}'.format(model['model']))
                    roi.subobject.append(model['model'].predict(im_crop))
        self.logger.info('Returning prediction of {} objects'.format(len(areas)))
        return areas
