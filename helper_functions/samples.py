# Libraries used
import numpy as np

# Write helper functions

# Sample from a normal distribution
def normal():
    mean = 0
    std_dev = 1
    num_samples = 1000

    # Samples is an array that contains the values of each person's political ideology
    samples = np.random.normal(mean, std_dev, num_samples)

    # Scale it so that it is between -1 and 1
    samples = 2 * (samples - np.min(samples)) / (np.max(samples) - np.min(samples)) - 1

    # Return a list
    return samples.tolist()

def two_peaks():
    mean1, std1 = -2, 1
    mean2, std2 = 2, 1
    n_samples = 1000
    samples1 = np.random.normal(loc=mean1, scale=std1, size=n_samples // 2)
    samples2 = np.random.normal(loc=mean2, scale=std2, size=n_samples // 2)
    bimodal_samples = np.concatenate([samples1, samples2])

    # Rescaling to the range [-1, 1]
    min_val = np.min(bimodal_samples)
    max_val = np.max(bimodal_samples)

    scaled_samples = 2 * (bimodal_samples - min_val) / (max_val - min_val) - 1

    return scaled_samples.tolist()

def uniform():
    num_samples = 1000

    # Generate samples uniformly distributed between -1 and 1
    samples = np.random.uniform(-1, 1, num_samples)
    return samples.tolist()

def skewed_left():
    num_samples = 1000
    a, b = 2, 4  # Shape parameters to skew the distribution
    samples = np.random.beta(a, b, num_samples)  # Beta distribution generates values in [0, 1]

    # Rescale to the range [-1, 1]
    samples = 2 * samples - 1
    return samples.tolist()

def skewed_right():
    num_samples = 1000
    a, b = 4, 2  # Shape parameters to skew the distribution
    samples = np.random.beta(a, b, num_samples)  # Beta distribution generates values in [0, 1]

    # Rescale to the range [-1, 1]
    samples = 2 * samples - 1
    return samples.tolist()