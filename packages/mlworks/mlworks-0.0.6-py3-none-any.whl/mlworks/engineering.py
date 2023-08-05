class Blueprint:

    def __init__(self, data):
        self.data = data

    def create_plan(self):
        self.plan = dict()

    def __include_on_list(self, plan, key, features):

        if plan.get(key, True) is True:
            plan[key] = features
        else:
            plan[key] = plan[key] + features
        return plan

    def __include_on_pairwise_list(self, plan, key, features, value):

        if plan.get(key, True) is True:
            plan[key] = {}
            if len(value) == 1:
                value = value * len(features)
        for var_index in range(len(features)):
            plan[key][features[var_index]] = features[var_index]
            plan[key][features[var_index]] = value[var_index]
        return plan

    def __include_on_custom_list(self, plan, key, feature, classes):

        if plan.get(key, True) is True:
            plan[key] = {}
        plan[key][feature] = {}
        for var_index in range(len(classes)):
            plan[key][feature]["class" + str(var_index)] = classes[var_index]
        return plan

    def __include_on_order_list(self, plan, key, features, order, grade=None):

        if plan.get(key, True) is True:
            plan[key] = {}
        for var_index in range(len(features)):
            plan[key][features[var_index]] = {}
            plan[key][features[var_index]]["order"] = order[var_index]
            if grade is None:
                gradeOrder = list(reversed(list(range(len(order[var_index])))))
            else:
                gradeOrder = grade[var_index]
            plan[key][features[var_index]]["grade"] = gradeOrder
        return plan

    def __include_on_operation_list(self, key, feature, operation):
        return None

    # Original Feature

    def keep_original_feature(self, features):
        key = "keep_original_feature"
        self.plan = self.__include_on_list(self.plan, key, features)
        return self

    # Imputation methods

    def impute_missing_as_category(self, features):
        key = "impute_missing_as_category"
        self.plan = self.__include_on_list(self.plan, key, features)
        return self

    def impute_missing_as_inf(self, features):
        key = "impute_missing_as_inf"
        self.plan = self.__include_on_list(self.plan, key, features)
        return self

    def impute_missing_as_zero(self, features):
        key = "impute_missing_as_zero"
        self.plan = self.__include_on_list(self.plan, key, features)
        return self

    def impute_missing_as_number(self, features, number):
        key = "impute_missing_as_number"
        self.plan = self.__include_on_pairwise_list(self.plan, key, features, number)
        return self

    # Binning

    def binning_number_one_threshold(self, features, thresholds):
        key = "binning_number_one_threshold"
        self.plan = self.__include_on_pairwise_list(self.plan, key, features, thresholds)
        return self

    def binning_class_one_vs_all(self, features, hot_class):
        key = "binning_class_one_vs_all"
        self.plan = self.__include_on_pairwise_list(self.plan, key, features, hot_class)
        return self

    def binning_one_hot_encoding(self, features):
        key = "binning_one_hot_encoding"
        self.plan = self.__include_on_list(self.plan, key, features)
        return self

    def binning_add_extra_class(self, features, extra_class):
        key = "binning_add_extra_class"
        self.plan = self.__include_on_pairwise_list(self.plan, key, features, extra_class)
        return self

    def binning_custom_classes(self, features, extra_class):
        key = "binning_custom_classes"
        self.plan = self.__include_on_custom_list(self.plan, key, features, extra_class)
        return self

    # Transform

    def transform_category_to_order(self, features, order, grade=None):
        key = "transform_category_to_order"
        self.plan = self.__include_on_order_list(self.plan, key, features, order, grade=None)
        return self

    def transform_linear(self, features, number):
        key = "transform_linear"
        self.plan = self.__include_on_pairwise_list(self.plan, key, features, number)
        return self
