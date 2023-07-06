Dataset **Teeth Segmentation on dental X-ray images** can be downloaded in Supervisely format:

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/3/y/0I/zI4eYfkm5ypz68IafUsRwbgl44j0X1Sakzk1LFrN2FLwj937CwFbkV50RZaXek1DSVkV1t63aIBRoD9SXSwFqmqpWJZU6jhxzcWz0pquU6RYgQdJhCDUgXnR1kKH.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Teeth Segmentation on dental X-ray images', dst_path='~/dtools/datasets/Teeth Segmentation on dental X-ray images.tar')
```
The data in original format can be 🔗[downloaded here](https://www.kaggle.com/datasets/humansintheloop/teeth-segmentation-on-dental-x-ray-images)