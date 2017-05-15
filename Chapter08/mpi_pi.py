from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

import numpy as np

N = 10000

n_procs = comm.Get_size()

print("This is process", rank)

# Create an array
x_part = np.random.uniform(-1, 1, int(N/n_procs))
y_part = np.random.uniform(-1, 1, int(N/n_procs))

hits_part = x_part**2 + y_part**2 < 1
hits_count = hits_part.sum()

print("partial counts", hits_count)

total_counts = comm.reduce(hits_count, root=0)

if rank == 0:
    print("Total hits:", total_counts)
    print("Final result:", 4 * total_counts/N)


