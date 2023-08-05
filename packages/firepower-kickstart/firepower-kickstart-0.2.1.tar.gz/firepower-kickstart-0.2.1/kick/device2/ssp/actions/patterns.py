"""patterns.py.

SSP prompt patterns

"""
import logging

import munch

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class SspPatterns:
    """SSP class that restores all prompt patterns."""
    def __init__(self, hostname, login_username, login_password, sudo_password, slot_id, app_hostname,
                 deploy_type='native', app_identifier=''):
        """Initializer of SspPatterns."""

        self.dev_hostname = hostname
        self.deploy_type = deploy_type
        self.app_identifier = app_identifier
        self.login_username = login_username
        self.login_password = login_password
        self.sudo_password = sudo_password
        self.slot_id = slot_id
        self.prompt = munch.Munch()

        # Prelogin prompts
        self.prompt.password_prompt = r'.*[Pp]assword: '
        self.prompt.prelogin_prompt = r'((%N )?(?<!Last )login: )'

        # MIO level prompts
        self.prompt.mio_prompt = r'%N([ /\w\-\*]+)?# '
        self.prompt.local_mgmt_prompt = r'%N\(local\-mgmt\)# '
        self.prompt.fxos_prompt = r'%N\(fxos\)# '
        self.prompt.fpr_module_prompt = r'\r\nFirepower-module.*>'
        self.prompt.cimc_prompt = r'\r\n\[.*\]# '

        self.prompt.rommon_prompt = r'rommon.*>' #?
        self.prompt.firepower_boot = r'-boot>' #?
        self.prompt.switch_boot = r'switch\(boot\)#' #?

        # FTD level prompts
        self.prompt.fireos_prompt = r'\r\n(\x1bE\x1b\[J)?> $'
        self.prompt.expert_cli = r'\r\n(\x1b\[18t)?admin@.*\$ $'
        self.prompt.sudo_prompt = '\r\n[^\r\n]*(root@.*#) $'
        self.prompt.disable_prompt = '[\r\n]{}> $'.format(app_hostname)
        self.prompt.enable_prompt = '[\r\n]{}# $'.format(app_hostname)
        self.prompt.config_prompt = '[\r\n]{}[\w]*\([\w\-]+\)# $'.format(app_hostname)

        # ASA level prompts
        self.prompt.asa_prompt = r'\r\nasa.*[>#]'

        logger.info('\n\n\nPrompts are: {}\n\n\n'.format(self.prompt))

    @property
    def hostname(self):
        return self.dev_hostname

    @hostname.setter
    def hostname(self, value):
        self.dev_hostname = value

