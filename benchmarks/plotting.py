import matplotlib.pyplot as plt
import csv
import numpy as np
import os
from os.path import join

from collections import namedtuple
from logger import Logger

Timings = namedtuple('Timings', ['down', 'up', 'calculation'])

class Plotting(object):
    """ Takes care of all the necessary plotting """

    def __init__(self):
        pass

    def create_plots_per_lambda(self, csv_path, state_machine_name, to_file=True):
        for lambda_type in ['intermediate', 'collect', 'accumulate']:
            lambda_timings = self._load_timings(csv_path, lambda_type)
            self._plot_time_profile(self._with_average(lambda_timings), lambda_type, state_machine_name, os.path.dirname(csv_path), to_file)
            self._plot_time_distribution(lambda_timings, lambda_type, state_machine_name, os.path.dirname(csv_path), to_file)

    def create_combined_plots(self, csv_path, state_machine_name, to_file=True):
        combined_timings = self._load_timings(csv_path)
        self._plot_time_profile(combined_timings, 'combined', state_machine_name, os.path.dirname(csv_path), to_file)
        self._plot_time_distribution(combined_timings, 'combined', state_machine_name, os.path.dirname(csv_path), to_file)

    def _log(self, message):
        # call the logger
        Logger.log("plotting")

    def _load_timings(self, csv_path, lambda_type=None):
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            # 'type','down','up','execution'
            up, down, calculation = [], [], []
            for row in reader:
                if lambda_type == None or lambda_type == row['type']:
                    up.append(row['up'])
                    down.append(row['down'])
                    calculation.append(int(row['execution']) - int(row['down']) - int(row['up']))
        return Timings(np.array(up, dtype=int), np.array(down, dtype=int), np.array(calculation, dtype=int))

    def _with_average(self, timings):
        down = np.append(timings.down, np.average(timings.down))
        up = np.append(timings.up, np.average(timings.up))
        calculation = np.append(timings.calculation, np.average(timings.calculation))
        return Timings(down, up, calculation)

    def _plot_time_profile(self, timings, lambda_type, state_machine_name, plot_dir=None, to_file=True):
        self._log('Creating plot {} profile {}'.format(state_machine_name, lambda_type))

        N = len(timings.down)
        index = np.arange(N)    # the x locations for the groups
        width = 0.5           # the width of the bars: can also be len(x) sequence

        fig, ax = plt.subplots()

        p1 = plt.bar(index, timings.down, width, color='b')
        p2 = plt.bar(index, timings.up, width, color='c', bottom=timings.down)
        p3 = plt.bar(index, timings.calculation, width, color='m', bottom=np.add(timings.down,timings.up))

        ax.set_ybound(0, 15000) # take the max value of execution plus 100
        ax.set_xbound(-0.5, 7.5) # number of intermediate lambdas?

        ax.set_ylabel('time in ms')
        ax.set_xlabel('execution index, last one is averages across executions')
        ax.set_title('Timing profiles for {}-lambda executions.'.format(lambda_type))
        ax.legend((p3, p2, p1), ('Calculation', 'S3 upload','S3 download'), loc=4)

        if to_file:
            plot_path = '{}/{}_{}_profile.png'.format(plot_dir, state_machine_name, lambda_type)
            plt.savefig(join(BENCHMARKS_FOLDER, plot_path), dpi=500)
        else:
            plt.show()

    def _plot_time_distribution(self, timings, lambda_type, state_machine_name, plot_dir, to_file=True):
        self._log('Creating plot {} distribution {}'.format(state_machine_name, lambda_type))

        up, down, calculation = np.average(timings.up), np.average(timings.down), np.average(timings.calculation)
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'S3 upload\n({}ms)'.format(int(up)), 'S3 download\n({}ms)'.format(int(down)), 'calculation\n({}ms)'.format(int(calculation))
        sizes = [up, down, calculation]
        explode = (0, 0, 0.1)  # only "explode" the 3nd slice

        fig1, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90, colors=['c','b','m'])
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title('Time spent on S3 upload, S3 download and actual calculation in percent.')

        if to_file:
            plot_path = '{}/{}_{}_dist.png'.format(plot_dir, state_machine_name, lambda_type)
            plt.savefig(join(BENCHMARKS_FOLDER, plot_path), dpi=500)
        else:
            plt.show()
