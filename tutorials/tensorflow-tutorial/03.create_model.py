import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 从csv文件中加载训练数据
training_data_df = pd.read_csv("./dataset/sales_data_training.csv", dtype=float)

# 拆分输入和输出
X_training = training_data_df.drop('销售总额', axis=1).values
Y_training = training_data_df[['销售总额']].values

# 加载测试数据
test_data_df = pd.read_csv("./dataset/sales_data_testing.csv", dtype=float)

# 拆分输入输出
X_testing = test_data_df.drop('销售总额', axis=1).values
Y_testing = test_data_df[['销售总额']].values

# 数据归一化：也可以像keras tutorial中那样统一用一个scaler
X_scaler = MinMaxScaler(feature_range=(0, 1))
Y_scaler = MinMaxScaler(feature_range=(0, 1))

# 输入输出都归一化
X_scaled_training = X_scaler.fit_transform(X_training)
Y_scaled_training = Y_scaler.fit_transform(Y_training)

# 很重要：训练数据和测试数据必须采用相同的归一化
X_scaled_testing = X_scaler.transform(X_testing)
Y_scaled_testing = Y_scaler.transform(Y_testing)

# 定义模型超参数
learning_rate = 0.001
training_epochs = 100
display_step = 5

# 定义输入输出
number_of_inputs = 9
number_of_outputs = 1

# 定义隐层的节点数：三个隐层
layer_1_nodes = 50
layer_2_nodes = 100
layer_3_nodes = 50

# 第一部分：定义神经网络的层

# 输入层
with tf.variable_scope('input'):
    X = tf.placeholder(tf.float32, shape=(None, number_of_inputs))

# 第一层隐层
with tf.variable_scope('layer_1'):
    weights = tf.get_variable(name="weights1", shape=[number_of_inputs, layer_1_nodes],
                              initializer=tf.contrib.layers.xavier_initializer())
    biases = tf.get_variable(name="biases1", shape=[layer_1_nodes], initializer=tf.zeros_initializer())
    layer_1_output = tf.nn.relu(tf.matmul(X, weights) + biases)

# 第二层隐层
with tf.variable_scope('layer_2'):
    weights = tf.get_variable(name="weights2", shape=[layer_1_nodes, layer_2_nodes],
                              initializer=tf.contrib.layers.xavier_initializer())
    biases = tf.get_variable(name="biases2", shape=[layer_2_nodes], initializer=tf.zeros_initializer())
    layer_2_output = tf.nn.relu(tf.matmul(layer_1_output, weights) + biases)

# 第三隐层
with tf.variable_scope('layer_3'):
    weights = tf.get_variable(name="weights3", shape=[layer_2_nodes, layer_3_nodes],
                              initializer=tf.contrib.layers.xavier_initializer())
    biases = tf.get_variable(name="biases3", shape=[layer_3_nodes], initializer=tf.zeros_initializer())
    layer_3_output = tf.nn.relu(tf.matmul(layer_2_output, weights) + biases)

# 输出层
with tf.variable_scope('output'):
    weights = tf.get_variable(name="weights4", shape=[layer_3_nodes, number_of_outputs],
                              initializer=tf.contrib.layers.xavier_initializer())
    biases = tf.get_variable(name="biases4", shape=[number_of_outputs], initializer=tf.zeros_initializer())
    prediction = tf.matmul(layer_3_output, weights) + biases

# 第二部分：定义损失函数来衡量训练阶段的预测准确度

with tf.variable_scope('cost'):
    Y = tf.placeholder(tf.float32, shape=(None, 1))
    cost = tf.reduce_mean(tf.squared_difference(prediction, Y))

# 第三部分： 定义优化函数
with tf.variable_scope('train'):
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)
