from plotting import Plotting
from logger import Logger

Logger.log("Hello")

csv_path = '/Users/Johannes/Uni/Master/Master Arbeit/repos/matrix-operations/benchmarks/v2_benchmark_bs2/block_size_2000/v3_benchmark_bs2-8kx8k.csv'
state_machine_name = 'yeah'

plotting = Plotting()
plotting.create_plots_per_lambda(csv_path, state_machine_name, to_file=False)
plotting.create_combined_plots(csv_path, state_machine_name, to_file=False)
