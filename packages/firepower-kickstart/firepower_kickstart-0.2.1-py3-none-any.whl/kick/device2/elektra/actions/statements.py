from unicon.eal.dialogs import Statement


def password_handler(spawn, password):
    spawn.sendline(password)
    spawn.sendline()


def enable_handler(spawn, password):
    spawn.sendline('enable')
    spawn.expect('Password: ')
    spawn.sendline(password)


class ElektraStatements:
    def __init__(self, patterns):
        self.login_password_statement = Statement(pattern=patterns.prompt.password_prompt,
                                                  action=password_handler,
                                                  args={'password': patterns.login_password},
                                                  loop_continue=True,
                                                  continue_timer=True)

        self.sudo_password_statement = Statement(pattern=patterns.prompt.password_prompt,
                                                 action=password_handler,
                                                 args={'password': patterns.sudo_password},
                                                 loop_continue=True,
                                                 continue_timer=True)

        self.enable_password_statement = Statement(pattern=patterns.prompt.disable_prompt,
                                                   action=enable_handler,
                                                   args={'password': patterns.enable_password},
                                                   loop_continue=True,
                                                   continue_timer=True)

        self.expert_password_statement = Statement(pattern=patterns.prompt.password_prompt,
                                                  action=password_handler,
                                                  args={'password': patterns.default_password},
                                                  loop_continue=True,
                                                  continue_timer=True)

