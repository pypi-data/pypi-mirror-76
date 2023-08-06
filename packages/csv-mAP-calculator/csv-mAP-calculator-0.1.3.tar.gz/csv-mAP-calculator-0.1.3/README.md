Function to calculate mean average precision (mAP) in CSV format for post detection prediction calculation.

# Requirements

python 3.*, numpy, pandas, cython(optinal), pyximport(optional)

# Installation

```
pip install CSV-mAP-calculator
pip install CSV-mAP-calculator -i https://pypi.python.org/simple
```

## Usage example:

Path to CSV-files:

```python
from CSV_mAP_calculator import get_csv_mAP

gt_file = 'csvs/gt.csv'
predict_file = 'csvs/predictions.csv'
mean_ap, average_precisions = get_csv_mAP(gt_file, predict_file, iou_threshold=0.5)
```

Or numpy arrays of shapes **(N, 6)** and **(M, 7)**. 

```python
from CSV_mAP_calculator import get_csv_mAP
import pandas as pd

gt = pd.read_csv('csvs/gt.csv', header=None, names=['img_path', 'x1', 'y1', 'x2', 'y2','conf', 'label']).values
pred = pd.read_csv('csvs/predictions.csv', header=None, names=['img_path', 'x1', 'y1', 'x2', 'y2', 'label']).values
mean_ap, average_precisions = get_csv_mAP(gt, pred)
```


## Input files format


* Annotation CSV-file:

```csv
'img_path','x1','y1','x2','y2','label'
path/imgname1.jpg,0,0,511,511,cat1
path/imgname2.jpg,122,247,666,799,cat2
...
```

* Detection CSV-file:

```csv
'img_path','x1','y1','x2','y2','conf','label'
path/imgname1.jpg,0,0,511,511,0.8958333,cat1
path/imgname1.jpg,121,32,511,242.5,0.9998,cat2
path/imgname2.jpg,0,0,511,511,0.8958333,cat3
...
```

* Return should be like:

```python
Number of files in annotations: 7283
Number of files in predictions: 7282
Unique classes: 3
Detections length: 7282
Annotations length: 7283
cat1                 | 0.917434 |    2445
cat2                 | 0.861768 |    2400
cat3                 | 0.930730 |    2438
mAP: 0.903311
0.903310916116078
```

