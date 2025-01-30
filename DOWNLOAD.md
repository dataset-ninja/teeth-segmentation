Dataset **Teeth Segmentation on Dental X-ray Images** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzE1OThfVGVldGggU2VnbWVudGF0aW9uIG9uIERlbnRhbCBYLXJheSBJbWFnZXMvdGVldGgtc2VnbWVudGF0aW9uLW9uLWRlbnRhbC14LXJheS1pbWFnZXMtRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiRzlCdW93eXkvbnNLbGRkLzI2QVBEbC9DNnNSRklQMUFTN3hucFNUYTJ0OD0ifQ==)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Teeth Segmentation on Dental X-ray Images', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/humansintheloop/teeth-segmentation-on-dental-x-ray-images/download?datasetVersionNumber=1).