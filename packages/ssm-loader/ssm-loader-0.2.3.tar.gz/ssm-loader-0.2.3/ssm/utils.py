import click


def print_ok_ssm_load(parameter_name):
    message = parameter_name + click.style(' OK', fg='green')
    click.echo(message)
    return message


def print_error_ssm_load(parameter_name):
    message = parameter_name + click.style(' FAIL', fg='red')
    click.echo(message)
    return message
