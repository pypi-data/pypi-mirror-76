import pandas as pd
from mlworks.engineering import Blueprint


def test_blueprint_plan():

    data = pd.DataFrame()
    bpr = Blueprint(data)
    bpr.create_plan()

    bpr.keep_original_feature(['var1']).\
        impute_missing_as_category(['var2', 'var3']).\
        impute_missing_as_inf(['var4', 'var5']).\
        impute_missing_as_zero(['var6', 'var7']).\
        impute_missing_as_number(['var8', 'var9'], [8, 9]).\
        binning_number_one_threshold(['var10', 'var11'], [10, 11]).\
        binning_class_one_vs_all(["var12"], ["categoria12"]).\
        binning_one_hot_encoding(["var13", "var14", "var15"]).\
        binning_add_extra_class(["var16"], ["extra16"]).\
        binning_custom_classes("var17", [["class1", "class2"], ["class3", "class4", "class6"]]).\
        transform_category_to_order(["var18"], [["catA", "catB", "catC"]]).\
        transform_linear(["var19"], [-2000])

    plan_correct = {
        "keep_original_feature": [
            "var1"
        ],
        "impute_missing_as_category": [
            "var2",
            "var3"
        ],
        "impute_missing_as_inf": [
            "var4",
            "var5"
        ],
        "impute_missing_as_zero": [
            "var6",
            "var7"
        ],
        "impute_missing_as_number": {
            "var8": 8,
            "var9": 9
        },
        "binning_number_one_threshold": {
            "var10": 10,
            "var11": 11
        },
        "binning_class_one_vs_all": {
            "var12": "categoria12"
        },
        "binning_one_hot_encoding": [
            "var13",
            "var14",
            "var15"
        ],
        "binning_add_extra_class": {
            "var16": "extra16"
        },
        "binning_custom_classes": {
            "var17": {
                "class0": [
                    "class1",
                    "class2"
                ],
                "class1": [
                    "class3",
                    "class4",
                    "class6"
                ]
            }
        },
        "transform_category_to_order": {
            "var18": {
                "order": [
                    "catA",
                    "catB",
                    "catC"
                ],
                "grade": [
                    2,
                    1,
                    0
                ]
            }
        },
        "transform_linear": {
            "var19": -2000
        }
    }
    assert bpr.plan == plan_correct
