import cv2
import numpy as np,sys


def Reduce_Image(img):
    scale_percent = 50
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_CUBIC) 
    return resized
    
def Expand_Image(img):
    scale_percent = 200
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim,interpolation =cv2.INTER_CUBIC ) 
    return resized

def Gaussian_Pyramid(X):
    layer = X.copy()
    Gaussianlist = [X]
    for i in range(6):
        layer = Reduce_Image(layer)
        layer = cv2.GaussianBlur(layer,(5,5),cv2.BORDER_DEFAULT)
        Gaussianlist.append(layer)
    return Gaussianlist

def Laplacian_pyramid(lst):
    LaplacianList = [lst[5]]
    for i in range(5,0,-1):
        GE = Expand_Image(lst[i])
        L = cv2.subtract(lst[i-1],GE)
        LaplacianList.append(L)
    return LaplacianList


def blend(l1, l2):
    LS = []
    for la,lb in zip(l1,l2):
        rows,cols,dpt = la.shape
        ls = np.hstack((la[:,0:cols//2], lb[:,cols//2:]))
        LS.append(ls)
    return LS

def reconstruct(LS):
    ls_ = LS[0]
    for i in range(1,6):
        ls_ = Expand_Image(ls_)
        ls_ = cv2.add(ls_, LS[i])
    return ls_

def savelp(a,b):
    l1 = Laplacian_pyramid(Gaussian_Pyramid(a))
    l2 = Laplacian_pyramid(Gaussian_Pyramid(b))
    end = reconstruct(blend(l1,l2))
    end = cv2.resize(end, (1800, 1000))
    cv2.imwrite('/Users/m451h/Desktop/projects/computer vision/gui/static/uploads/Pyramid_blending.jpg',end)
    cv2.destroyAllWindows()

def blendTwoImages():
    # A = cv2.imread('/Users/m451h/Desktop/projects/computer vision/gui/uploads/input1.png')
    # B = cv2.imread('/Users/m451h/Desktop/projects/computer vision/gui/uploads/input2.png')
    A = cv2.imread('/Users/m451h/Desktop/projects/computer vision/gui/static/uploads/input1.png')
    B = cv2.imread('/Users/m451h/Desktop/projects/computer vision/gui/static/uploads/input2.png')
    A = cv2.resize(A, (512, 512))
    B = cv2.resize(B, (512, 512))
    savelp(A,B)

blendTwoImages()