# RandomShrubs
Own python implementation of Random Forest classification algorithm

```
usage: run.py [-h] [--sample_frac] [--n_of_attrs] [--n_of_shrubs]
              train_set classify_set class_col

positional arguments:
    train_set             training csv file with headers
    classify_set          unclassified csv file with headers
    class_col             class column header

optional arguments:
    --sample_frac         training data fraction per shrub (default .67)
    --n_of_attrs          number of attributes per shrub (default min(4, total number of attributes))
    --n_of_shrubs         number of shrubs (default 10)
  ```
