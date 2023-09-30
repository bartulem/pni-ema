"""
@author: bartulem
Select daily EMA targets.
"""

from datetime import datetime as dt
import math
import pandas as pd


class EMAOperator:
    # list of date ranges or dates when EMA does not occur
    no_ema_dates = ['12-24:01-05', '06-19', '07-04', '09-01', '11-22:12-01']

    # list of employee positions (abbreviated)
    # FA - faculty, PD - postdoc, GS - graduate student, OE (other employees) - administrative staff / lab manage / lab technician / IT staff
    pni_positions = ['Faculty', 'Postdoc', 'Graduate Student', 'OE']

    def __init__(self, ema_directory=None):
        self.ema_directory = ema_directory

    def check_date_validity(self):
        """
        Description
        ----------
        This method checks whether the current date falls within
        a range of holiday days or on a holiday.
        ----------

        Parameters
        ----------
        ----------

        Returns
        ----------
        (bool)
            Boolean specifying whether current date belongs to holiday list.
        ----------
        """

        date_now = dt.now()
        day_of_week = dt.today().weekday()

        for avoid_date in self.no_ema_dates:
            if ':' in avoid_date:
                date_split = avoid_date.split(':')
                if date_split[0].split('-')[0] <= date_split[1].split('-')[0]:
                    avoid_start_date = dt.strptime(f'{date_now.year}-{date_split[0]}', '%Y-%m-%d')
                    avoid_end_date = dt.strptime(f'{date_now.year}-{date_split[1]}', '%Y-%m-%d')
                else:
                    if date_now.month == 12:
                        year_start = date_now.year
                        year_end = date_now.year + 1
                    else:
                        year_start = date_now.year - 1
                        year_end = date_now.year
                    avoid_start_date = dt.strptime(f'{year_start}-{date_split[0]}', '%Y-%m-%d')
                    avoid_end_date = dt.strptime(f'{year_end}-{date_split[1]}', '%Y-%m-%d')
                if avoid_start_date <= date_now <= avoid_end_date:
                    return False
            else:
                if date_now.strftime('%m-%d') == avoid_date:
                    return False
        else:
            if day_of_week < 5:
                return True
            else:
                return False

    def target_individuals(self, csv_delimiter=',', select_all=False):
        """
        Description
        ----------
        This method selects the individuals to receive the EMA survey,
        by taking into consideration the date (sampling w/ replacement).
        ----------

        Parameters
        ----------
        Contains the following set of parameters
            csv_delimiter (str)
                Delimiter in ema_directory.csv file; defaults to ",".
            select_all (bool)
                Select everyone as EMA targets for the day.
        ----------

        Returns
        ----------
        individual_targets_dict (dict or bool)
            Dictionary w/ target e-mails, or False (if date is holiday).
        ----------
        """

        if self.check_date_validity():
            individual_targets_dict = {pos: [] for pos in self.pni_positions}
            csv_directory = pd.read_csv(filepath_or_buffer=self.ema_directory,
                                        sep=csv_delimiter,
                                        encoding='ISO-8859-1')

            for position in self.pni_positions:
                if select_all:
                    individual_targets_dict[position] = csv_directory[csv_directory['Title'] == position]['E-mail'].values.tolist()
                else:
                    # total number of individuals in given position
                    individuals_in_pos_num = csv_directory[csv_directory['Title'] == position].shape[0]
                    num_of_ind_to_sample = int(math.ceil(individuals_in_pos_num / 30))

                    # select random target(s) from available individuals
                    individual_targets_dict[position] = csv_directory[csv_directory['Title'] == position].sample(n=num_of_ind_to_sample)['E-mail'].values.tolist()

            return individual_targets_dict

        else:
            return False
