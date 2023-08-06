import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import sys
from sys import getsizeof
import time
import numpy as np
import pandas as pd


# Define CUDA function
mod = SourceModule(
    """

__global__ void get_cov(int cols, int total_rows, float *d_A, float *d_means, float *d_covariances) {
	extern __shared__ float s_sum[];  					// sum of the values per row per block
	int tid = threadIdx.x;  							// Local: Thread ID
	unsigned int g_tid = 0;								// Global ID of the first feature
	unsigned int g_tid_2 = 0; 							// Global ID of the second feature

	// First, get the means:
	for ( int i = 0; i < __float2uint_ru((float)total_rows/(float)blockDim.x); i++) {
		g_tid = (i * blockDim.x + tid) + (blockIdx.x * total_rows);
		s_sum[tid] = d_A[g_tid];
		__syncthreads();

		// Inclusive Scan
		float temp = 0.0;
		for (int j = 1; j < blockDim.x; j *= 2 ) {
			if ( (tid - j) >= 0)
				temp = s_sum[tid - j];
			__syncthreads();
			if ( (tid - j) >= 0)
				s_sum[tid] += temp;
			__syncthreads();
		}

		if(tid == blockDim.x - 1) {
			d_means[blockIdx.x] += s_sum[tid];
		}
		__syncthreads();		
	}

	// Save the result of Feature-Block on global memory
	if(tid == blockDim.x - 1)
		d_means[blockIdx.x] /= total_rows;
	__syncthreads();		


	// Then, compute the covariance:
	// Iterate over features, starting from the actual feature
	for (int i = blockIdx.x; i < cols; i++ ){

		// Index of cell i,j
		int index = (blockIdx.x * cols) + i;

		// index of cell j,i
		int index_2 = (i * cols) + blockIdx.x;
		
		// Iterate over the size of samples
		for ( int k = 0; k < __float2uint_ru((float)total_rows/(float)blockDim.x); k++) {

			// Calculate mapped indexes
			g_tid = (k * blockDim.x + tid) + (blockIdx.x * total_rows);			
			g_tid_2 = (k * blockDim.x + tid) + (total_rows * i);

			// Compute the covariance
			s_sum[tid] = (d_A[g_tid] - d_means[blockIdx.x]) * (d_A[g_tid_2] - d_means[i]);
			__syncthreads();

			// Inclusive scan
			float temp;
			for (int j = 1; j < blockDim.x; j *= 2 ){
				if ( (tid - j) >= 0)
					temp = s_sum[tid - j];
				__syncthreads();
				if ( (tid - j) >= 0)
					s_sum[tid] += temp;
				__syncthreads();
			}

			if(tid == blockDim.x - 1) {
				d_covariances[index] += s_sum[tid];

			}
			__syncthreads();
		}

		// Save the result of Feature-Block on global memory
		if(tid == blockDim.x - 1) {
			float aux = d_covariances[index] / total_rows;
			d_covariances[index] = aux;

			// Symmetric Cell
			// if not diagonal
			if ( index % (cols+1) != 0 ) {
				d_covariances[index_2] = aux;
			}
		}

	}
	
	
}"""
)

func = mod.get_function("get_cov")


def get_cov(argv):

    df = pd.read_csv(filepath_or_buffer="../data/data_small.txt", header=None, sep=" ")

    # rows = 8192
    rows = int(argv[0])

    # cols = 32
    cols = int(argv[1])

    # Host Memory
    means = np.zeros(cols)
    means = means.astype(np.float32)

    covariances = np.zeros(cols * cols)
    covariances = covariances.astype(np.float32)

    A = df.values
    A = A.astype(np.float32)

    # Allocate on device
    d_A = cuda.mem_alloc(A.size * A.dtype.itemsize)
    d_means = cuda.mem_alloc(means.size * means.dtype.itemsize)
    d_covariances = cuda.mem_alloc(covariances.size * covariances.dtype.itemsize)

    # Copy from host to device
    cuda.memcpy_htod(d_A, A)
    cuda.memcpy_htod(d_means, means)
    cuda.memcpy_htod(d_covariances, covariances)

    # Number of threads per block
    threadCount = 1024

    # Number of blocks per grid
    blockCount = cols

    # Start GPU time
    start = cuda.Event()
    end = cuda.Event()
    start.record()

    func(
        np.int32(cols),
        np.int32(rows),
        d_A,
        d_means,
        d_covariances,
        block=(threadCount, 1, 1),
        grid=(blockCount, 1),
        shared=threadCount * A.dtype.itemsize,
    )

    # End GPU time
    end.record()
    end.synchronize()

    # GPU time
    ms = start.time_till(end)
    print("GPU Execution time: %fms" % (ms))

    # CPU time using cov() from numpy
    start_time = time.time()
    cov_mat_np = np.cov(A, rowvar=False)
    ms = (time.time() - start_time) * 1000
    print("CPU Execution time (Numpy Cov): %fms" % (ms))

    # CPU time using lineal algebra manually with numpy
    start_time = time.time()
    mean_vec = np.mean(A, axis=0)
    cov_mat_la = (A - mean_vec).T.dot((A - mean_vec)) / (A.shape[0] - 1)
    ms = (time.time() - start_time) * 1000
    print("CPU Execution time (Linear Algebra): %fms \n" % (ms))

    # Copy result to host
    cuda.memcpy_dtoh(covariances, d_covariances)

    # Display results
    if len(sys.argv) > 3 and int(argv[2]) < cols:
        i = int(argv[2])
        print("\nRES GPU: \n", covariances[32 * i : (32 * i) + 31])
        print("\nRES CPU Numpy: \n", cov_mat_np[i])
        print("\nRES CPU Linear Algebra: \n", cov_mat_la[i])


# if __name__ == "__main__":
#     main(sys.argv[1:])

