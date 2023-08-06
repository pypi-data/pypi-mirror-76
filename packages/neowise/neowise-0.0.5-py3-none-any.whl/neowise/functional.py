import numpy as np


class Predict:
    """
    Predict
    Used to calculate the predictions of the network based on the activation of the output layer
    of the network for Binary Classification tasks

    Arguments:
        A: Activations of the output layer (nd-array)
        threshold: Value between 0 and 1, above which the prediction is 1 and below which is 0 (default=0.5) (float)
    Returns:
        predictions: Predictions made based on the activations of the output layer (nd-array)
    """
    def __init__(self, A, threshold=0.5):
        self.A = A
        self.threshold = threshold

    def __call__(self):
        predictions = np.zeros((self.A.shape))
        for g in range(0, self.A.shape[1]):
            if self.A[:, g] >= self.threshold:
                predictions[:, g] = 1
        return predictions


class PredictMulti:
    """
    Predict Multi
    Used to calculate the predictions of the network based on the activation of the output layer
    of the network for Multi Class Classification tasks

    Arguments:
        A: Activations of the output layer of the network (nd-array)
    Returns:
        predictions: Predictions made based on the activations of the output layer (nd-array)
    """
    def __init__(self, A):
        self.A = A

    def __call__(self):
        predictions_multi = np.zeros(self.A.shape)
        for v in range(0, self.A.shape[1]):
            temp = max(self.A[:, v])
            for w in range(0, self.A.shape[0]):
                if self.A[w, v] == temp:
                    predictions_multi[w, v] = 1
                else:
                    predictions_multi[w, v] = 0
        return predictions_multi


class Evaluate:
    """
    Evaluate
    Calculates the accuracy of the network, i.e gives the percentage of the ratio between the data that is correctly
    classified to the total number of examples of data for Binary Classification tasks

    Arguments:
        y: Output labels of the train/test data (nd-array)
        preds: Predictions of the network (nd-array)
    Returns:
        accuracy: percentage of data correctly predicted when compared to the labels (float)
    """
    def __init__(self, y, preds):
        self.y, self.preds = y, preds

    def __call__(self):
        accuracy = float(np.mean(self.preds == self.y, axis=1) * 100)
        return accuracy


class EvaluateMulti:
    """
    Evaluate Multi
    Calculates the accuracy of the network, i.e gives the percentage of the ratio between the data that is correctly
    classified to the total number of examples of data for Multi Class Classification tasks

    Arguments:
        y: Output labels of the train/test data (nd-array)
        preds: Predictions of the network (nd-array)
    Returns:
        accuracy: percentage of data correctly predicted when compared to the labels (float)
    """
    def __init__(self, y, preds):
        self.y, self.preds = y, preds

    def __call__(self):
        ones_array = np.ones(self.preds.shape)
        temp1 = self.preds == ones_array
        ind = []
        for gee in range(0, temp1.shape[1]):
            for jee in range(0, temp1.shape[0]):
                if temp1[jee, gee] == True:
                    ind.append(jee)
        ind_arr = np.array(ind)
        y_list = []
        for gee in range(0, self.y.shape[1]):
            for jee in range(0, self.y.shape[0]):
                if self.y[jee, gee] == 1:
                    y_list.append(jee)
        y_arr = np.array(y_list)
        accuracy = float(np.mean(ind_arr == y_arr.T)) * 100
        return accuracy


class PrecisionRecall:
    """
    Precision Recall
    Calculates Precision, recall and F1 score of the network for Binary Classification tasks

    Arguments:
        A: Predictions of the network (nd-array)
        y: Labelled outputs of train/test set (nd-array)
    Returns:
        Precision, Recall and F1 score: All values between 0 and 1 (float)
    """
    def __init__(self, A, y):
        self.A, self.y = A, y

    def __call__(self):
        tp = 0
        fp = 0
        fn = 0
        for i in range(0, self.y.shape[1]):
            if ((self.A[0, i] == 1) and (self.y[0, i] == 1)):
                tp = tp + 1
            if ((self.A[0, i] == 1) and (self.y[0, i] == 0)):
                fp = fp + 1
            if (self.A[0, i] == 0) and (self.y[0, i] == 1):
                fn = fn + 1
        prec = tp / (tp + fp)
        rec = tp / (tp + fn)
        f1 = (2 * prec * rec) / (prec + rec)
        return prec, rec, f1


class PrecisionRecallMulti:
    """
    Precision Recall Multi
    Calculates Precision, recall and F1 score of the network for each of the classes of
    Multi Class Classification tasks

    Arguments:
        A: Predictions of the network (nd-array)
        y: Labelled outputs of train/test set (nd-array)
    Returns:
        Precision, Recall and F1 score: All values between 0 and 1 for all of the classes in Multi Class Classification
    """
    def __init__(self, A, y):
        self.A, self.y = A, y

    def __call__(self):
        epsilon = 1e-5
        tp_multi = {}
        fp_multi = {}
        fn_multi = {}
        prec_multi = {}
        rec_multi = {}
        f1_multi = {}
        num_classes = self.y.shape[0]
        for r in range(0, num_classes):
            tp_multi["class" + str(r)] = 0
            fp_multi["class" + str(r)] = 0
            fn_multi["class" + str(r)] = 0
        for c in range(0, self.y.shape[1]):
            for g in range(0, self.y.shape[0]):
                if ((self.A[g, c] == 1) and (self.y[g, c] == 1)):
                    tp_multi["class" + str(g)] = tp_multi["class" + str(g)] + 1
                if ((self.A[g, c] == 1) and (self.y[g, c] == 0)):
                    fp_multi["class" + str(g)] = fp_multi["class" + str(g)] + 1
                if ((self.A[g, c] == 0) and (self.y[g, c] == 1)):
                    fn_multi["class" + str(g)] = fn_multi["class" + str(g)] + 1
        for n in range(0, num_classes):
            prec_multi["class" + str(n)] = tp_multi["class" + str(n)] / (
                    tp_multi["class" + str(n)] + fp_multi["class" + str(n)] + epsilon)
            rec_multi["class" + str(n)] = tp_multi["class" + str(n)] / (
                    tp_multi["class" + str(n)] + fn_multi["class" + str(n)] + epsilon)
            f1_multi["class" + str(n)] = (2 * prec_multi["class" + str(n)] * rec_multi["class" + str(n)]) / (
                    prec_multi["class" + str(n)] + rec_multi["class" + str(n)] + epsilon)
        return prec_multi, rec_multi, f1_multi


class GradL1Reg:
    """
    Grad L1 Reg
    Calculates the derivative of the weights of the array to itself

    Arguments:
        layers_arr: List containing the objects of nw.layers classes
    """
    def __init__(self, layers_arr):
        self.layers_arr = layers_arr

    def __call__(self):
        for layer in self.layers_arr:
            layer.grad_L1 = np.zeros(layer.weights.shape)
            for p in range(0, layer.weights.shape[0]):
                for n in range(0, layer.weights.shape[1]):
                    if layer.weights[p, n] > 0:
                        layer.grad_L1[p, n] = 1
                    else:
                        layer.grad_L1[p, n] = -1


class CreateMiniBatches:
    """
    Create Mini Batches
    Creates mini batches for training with the specified mini-batch size

    Arguments:
        X: Training data (nd-array)
        y: Training data outputs (nd-array)
        mb_size: Number of training examples in each mini-batch (int)
    Returns:
        mini_batch: Dictionary containing all the mini-batches (dict)
        num: Number of mini-batches created with the specified mb_size (int)
    """
    def __init__(self, X, y, mb_size):
        self.X, self.y, self.mb_size = X, y, mb_size

    def __call__(self):
        m_ex = self.y.shape[1]
        mini_batch = {}
        num = m_ex // self.mb_size
        if m_ex % self.mb_size != 0:
            f = 0
            for p in range(0, num):
                mini_batch["MB_X" + str(p)] = self.X[f:(f + self.mb_size), :]
                mini_batch["MB_Y" + str(p)] = self.y[:, f:(f + self.mb_size)]
                f = f + self.mb_size
            mini_batch["MB_X" + str(num)] = self.X[f:m_ex, :]
            mini_batch["MB_Y" + str(num)] = self.y[:, f:m_ex]
            return mini_batch, num
        else:
            f = 0
            for p in range(0, num - 1):
                mini_batch["MB_X" + str(p)] = self.X[f:(f + self.mb_size), :]
                mini_batch["MB_Y" + str(p)] = self.y[:, f:(f + self.mb_size)]
                f = f + self.mb_size
            mini_batch["MB_X" + str(num - 1)] = self.X[f:m_ex, :]
            mini_batch["MB_Y" + str(num - 1)] = self.y[:, f:m_ex]
            return mini_batch, num - 1
