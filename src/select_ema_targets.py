"""
@author: bartulem
Select daily EMA targets.
"""

from datetime import datetime as dt
import pandas as pd


class EMAOperator:
    # list of date ranges or dates when EMA does not occur
    no_ema_dates = ['12-24:01-05', '06-19', '07-04', '09-01', '11-22:12-01']

    # list of employee positions (abbreviated)
    # FA - faculty, PD - postdoc, GS - graduate student, OE (other employees) - administrative staff / lab manage / lab technician / IT staff
    pni_positions = ['FA', 'PD', 'GS', 'OE']

    def __init__(self, ema_directory=None):
        self.ema_directory = ema_directory

    def check_date_validity(self):
        """
        Description
        ----------
        This method check whether the current date falls within
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

    def target_individuals(self, csv_delimiter=','):
        """
        Description
        ----------
        This method selects the individuals to receive the EMA survey,
        by taking into consideration the date and the eligibility history.
        ----------

        Parameters
        ----------
        Contains the following set of parameters
            csv_delimiter (str)
                Delimiter in ema_directory.csv file; defaults to ",".
        ----------

        Returns
        ----------
        individual_targets_dict (dict or bool)
            Dictionary w/ target e-mails, or False (if date is holiday).
        ----------
        """

        if self.check_date_validity():
            individual_targets_dict = {}
            csv_directory = pd.read_csv(filepath_or_buffer=self.ema_directory,
                                        sep=csv_delimiter)

            # check eligibility and correct if necessary
            for position in self.pni_positions:
                if not csv_directory[(csv_directory['POSITION'] == position) & (csv_directory['ELIGIBLE'] > 0)].shape[0] > 0:
                    csv_directory.loc[(csv_directory['POSITION'] == position), 'ELIGIBLE'] = 1

                # select random target from eligible individuals
                individual_targets_dict[position] = csv_directory[(csv_directory['POSITION'] == position) & (csv_directory['ELIGIBLE'] > 0)].sample()['E-MAIL'].values[0]

                # update eligibility
                csv_directory.loc[(csv_directory['E-MAIL'] == individual_targets_dict[position]), 'ELIGIBLE'] = 0

            # save modified CSV file
            csv_directory.to_csv(path_or_buf=self.ema_directory,
                                 sep=csv_delimiter,
                                 index=False)

            return individual_targets_dict

        else:
            return False
