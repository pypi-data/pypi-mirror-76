# rescaler
A package that can transform features by scaling each feature to a given range. The input should be (input list, new minimum value, new maximum value). This is more light weight and easy to use than sklearn.preprocessing.MinMaxScaler. This package can simply and quickly rescale each element of the input list into a new value within the range, and generate a new list.

### Parameters
**`rescaler.rescaler.rescale`**

* `input_list` A list.
* `newmin` The minimum value of the new scale.
* `newmax` The maximum value of the new scale.
