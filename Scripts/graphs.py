from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

def model_accuracy(fit_object):
    # fit_object = model1.fit(train_x, train_y,validation_split = 0.1, epochs=50, batch_size=4)
    plt.plot(fit_object.history['accuracy'])
    plt.plot(fit_object.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

def model_loss(fit_object):
    plt.plot(fit_object.history['loss'])
    plt.plot(fit_object.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

def conf_matrix(matrix):
    cmd = ConfusionMatrixDisplay(matrix, display_labels=['positive','negative'])
    cmd.plot(cmap='Blues')

