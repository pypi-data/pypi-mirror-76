# ALNLP

This package repacks some sub-modules from [AllenNLP](https://github.com/allenai/allennlp) into a seperate, lightweight package. `alnlp`=`allennlp`-`len`, which means `alnlp` is a reduced-length version of `allennlp` .

Modification:

- `allennlp.training.metrics` renamed to `alnlp.metrics`
- `conditional_random_field.py` moved to  `alnlp.modules`
- `chu_liu_edmonds.py` moved to  `alnlp.algorithms`
- Unrelated dependencies removed
- Other sub-modules are not included

This package is provided "AS IS" without warranty of any kind. If you find any bugs, please try the original  [AllenNLP](https://github.com/allenai/allennlp) , which is up-to-date and well maintained.

## Licence

This package adopts the same [Apache License 2.0](https://github.com/allenai/allennlp/blob/master/LICENSE) from AllenNLP. 

All credit goes to AllenNLP team. 

