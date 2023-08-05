#----------------------------- scalar_losses.py file ----------------------------------#
"""
This file contains the definition of the loss functions that are employed in the TBNN-s
class, between predicted and truth u'c' vector
"""

import numpy as np
import tensorflow as tf

def lossLog(uc, uc_predicted, tf_flag=False):
    """
    One possible loss to determine how bad is uc_predicted compared to uc, the log
    loss: mean(log(||uc-uc_predicted||/||uc||))
    
    Arguments:
    uc -- np.array or tensor containing the true uc vector, shape [None, 3]
    uc_predicted -- np.array or tensor containing the predicted uc vector, 
                    shape [None, 3]
    tf_flag -- optional argument, bool which says whether we are dealing with tensorflow
               tensors or with numpy arrays.
               
    Returns:
    loss_pred -- the prediction loss for the given uc_predicted (either a number or a
                 tensor shape [] depending on tf_flag)    
    """
    
    if tf_flag:
        loss_ratio = ( tf.norm(uc - uc_predicted, ord=2, axis=1) /
                       tf.norm(uc, ord=2, axis=1) )       
        loss_pred = tf.reduce_mean(tf.math.log(loss_ratio))        
        return loss_pred    
    else:
        loss_ratio = ( np.linalg.norm(uc-uc_predicted, ord=2, axis=1) /
                       np.linalg.norm(uc, ord=2, axis=1) )       
        loss_pred = np.mean(np.log(loss_ratio))                    
        return loss_pred

        
def lossL2k(uc, uc_predicted, one_over_k, tf_flag=False):
    """
    One possible loss to determine how bad is uc_predicted compared to uc, the l2
    loss normalized by k: mean(||uc-uc_predicted||^2/k)
    
    Arguments:
    uc -- np.array or tensor containing the true uc vector, shape [None, 3]
    uc_predicted -- np.array or tensor containing the predicted uc vector, 
                    shape [None, 3]
    one_over_k -- np.array or tensor containing the elements in k (turbulent kinetic
                  energy), shape [None, 1] (must be broadcastable with uc)
    tf_flag -- optional argument, bool which says whether we are dealing with tensorflow
               tensors or with numpy arrays.
               
    Returns:
    loss_pred -- the prediction loss for the given uc_predicted (either a number or a
                 tensor shape [] depending on tf_flag)    
    """
    
    FACTOR = 2e3 # factor to multiply the loss so it's O(1)
    if tf_flag:
        loss = tf.math.squared_difference(uc, uc_predicted)*one_over_k                               
        loss_pred = FACTOR*tf.reduce_mean(tf.reduce_sum(loss, axis=1))
        return loss_pred        
    else:
        if len(one_over_k.shape) == 1: one_over_k=np.expand_dims(one_over_k,-1)
        loss_pred = FACTOR*np.mean( np.sum((uc_predicted - uc)**2 * one_over_k, axis=1) )
        return loss_pred
        

def lossL2(uc, uc_predicted, one_over_u2c2, tf_flag=False):
    """
    One possible loss to determine how bad is uc_predicted compared to uc, the l2
    loss un-normalized (non-dimensionalized by bulk quantities):
    mean(||uc-uc_predicted||^2/Uj^2C^2)
    
    Arguments:
    uc -- np.array or tensor containing the true uc vector, shape [None, 3]
    uc_predicted -- np.array or tensor containing the predicted uc vector, 
                    shape [None, 3]
    one_over_u2c2 -- np.array or tensor containing the elements in 1/Uj^2*C^2 (bulk 
                     quantities for U and C), shape [None, 1] (must be broadcastable
                     with uc)
    tf_flag -- optional argument, bool which says whether we are dealing with tensorflow
               tensors or with numpy arrays.
               
    Returns:
    loss_pred -- the prediction loss for the given uc_predicted (either a number or a
                 tensor shape [] depending on tf_flag)    
    """
    
    FACTOR = 4e4 # factor to multiply the loss so it's O(1)    
    if tf_flag:
        loss = tf.math.squared_difference(uc, uc_predicted)*one_over_u2c2                               
        loss_pred = FACTOR*tf.reduce_mean(tf.reduce_sum(loss, axis=1))
        return loss_pred        
    else:
        if len(one_over_u2c2.shape) == 1: one_over_u2c2=np.expand_dims(one_over_u2c2,-1)
        loss_pred = FACTOR*np.mean(np.sum((uc_predicted - uc)**2 *one_over_u2c2, axis=1))
        return loss_pred

        
def lossL1(uc, uc_predicted, one_over_uc, tf_flag=False):
    """
    One possible loss to determine how bad is uc_predicted compared to uc, the l1
    loss un-normalized (non-dimensionalized by bulk quantities):
    mean(|uc-uc_predicted|/Uj*C)
    
    Arguments:
    uc -- np.array or tensor containing the true uc vector, shape [None, 3]
    uc_predicted -- np.array or tensor containing the predicted uc vector, 
                    shape [None, 3]
    one_over_uc -- np.array or tensor containing the elements in 1/Uj^2*C^2 (bulk 
                   quantities for U and C), shape [None, 1] (must be broadcastable
                   with uc)
    tf_flag -- optional argument, bool which says whether we are dealing with tensorflow
               tensors or with numpy arrays.
               
    Returns:
    loss_pred -- the prediction loss for the given uc_predicted (either a number or a
                 tensor shape [] depending on tf_flag) 
    """    
    
    FACTOR = 2e2 # factor to multiply the loss so it's O(1)
    if tf_flag:
        loss = tf.abs(uc - uc_predicted)*one_over_uc                               
        loss_pred = FACTOR*tf.reduce_mean(tf.reduce_sum(loss, axis=1))
        return loss_pred        
    else:
        if len(one_over_uc.shape) == 1: one_over_uc=np.expand_dims(one_over_uc,-1)
        loss_pred = FACTOR*np.mean(np.sum(np.abs(uc_predicted - uc)*one_over_uc, axis=1))
        return loss_pred
        
        
def lossCos(uc, uc_predicted, tf_flag=False):
    """
    One possible loss to determine how bad is uc_predicted compared to uc, the angle
    loss. This is quadratic in the cosine of the angle between uc and uc_predicted 
    (0 is best, 1 is worst)
    
    Arguments:
    uc -- np.array or tensor containing the true uc vector, shape [None, 3]
    uc_predicted -- np.array or tensor containing the predicted uc vector, 
                    shape [None, 3]    
    tf_flag -- optional argument, bool which says whether we are dealing with tensorflow
               tensors or with numpy arrays.
               
    Returns:
    loss_pred -- the prediction loss for the given uc_predicted (either a number or a
                 tensor shape [] depending on tf_flag)    
    """
    
    if tf_flag:
        cos = ( tf.reduce_sum(uc*uc_predicted, axis=1) / 
                (tf.norm(uc, ord=2, axis=1)*tf.norm(uc_predicted, ord=2, axis=1)) )                             
        loss_pred = 0.5*(-1.0*tf.reduce_mean(cos)+1.0)
        return loss_pred        
    else:
        cos = ( np.sum(uc*uc_predicted, axis=1) / 
             (np.linalg.norm(uc, ord=2, axis=1)*np.linalg.norm(uc_predicted, ord=2, axis=1)) )        
        loss_pred = 0.5*(-1.0*np.mean(cos)+1.0)
        return loss_pred        