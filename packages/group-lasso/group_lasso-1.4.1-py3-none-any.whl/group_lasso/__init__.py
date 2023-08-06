"""Group lasso regularised linear models.
"""


__version__ = "1.4.1"
__author__ = "Yngve Mardal Moe"
__email__ = "yngve.m.moe@gmail.com"


from group_lasso._group_lasso import (BaseGroupLasso, GroupLasso,
                                      LogisticGroupLasso)

MultinomialGroupLasso = LogisticGroupLasso
