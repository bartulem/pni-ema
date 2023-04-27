"""
@author: bartulem
Code to send e-mail w/ EMA survey.
"""

import configparser
from datetime import datetime as dt
import email.message
import smtplib
from select_ema_targets import EMAOperator


class Messenger:

    def __init__(self,
                 eml_file=None,
                 email_config_file=None,
                 ema_directory=None):

        self.eml_file = eml_file
        self.email_config_file = email_config_file
        self.ema_directory = ema_directory

    def get_email_params(self):
        """
        Description
        ----------
        This method gets the EMA-PNI e-mail address and password to send a message.
        ----------

        Parameters
        ----------
        ----------

        Returns
        ----------
        email_address (str)
            EMA-PNI e-mail address.
        email_password (str)
            EMA-PNI e-mail password.
        ----------
        """

        config = configparser.ConfigParser()
        config.read(self.email_config_file)
        return config['email']['email_address'], \
            config['email']['email_password'], \
            config['email']['smtp_host'], \
            int(config['email']['smtp_port'])

    def send_message(self):
        """
        Description
        ----------
        This method send the EMA survey to all relevant parties.
        ----------

        Parameters
        ----------
        ----------

        Returns
        ----------
        ----------
        """

        individual_targets_dict = EMAOperator(ema_directory=self.ema_directory).target_individuals()

        if type(individual_targets_dict) == dict:
            email_address, email_password, email_host, email_port = self.get_email_params()

            ema_email = open(self.eml_file, 'r').read()
            message = email.message_from_string(ema_email)

            smtp = smtplib.SMTP(email_host, email_port)
            smtp.starttls()
            smtp.login(email_address, email_password)
            for position in individual_targets_dict.keys():
                message.replace_header('From', email_address)
                message.replace_header('To', individual_targets_dict[position])
                message.replace_header('Subject', message['Subject'])
                message.replace_header('Date', f'{dt.now()}')

                smtp.sendmail(email_address, individual_targets_dict[position], message.as_string())

            smtp.quit()


if __name__ == '__main__':
    Messenger(eml_file= '.../PNI_Daily_Climate_Survey.eml',
              email_config_file='.../email_config.ini',
              ema_directory='.../ema_directory.csv').send_message()
