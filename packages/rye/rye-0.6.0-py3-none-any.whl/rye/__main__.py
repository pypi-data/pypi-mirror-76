import click
from click import Group, echo
from click.exceptions import Exit
from settingscascade import SettingsManager

from rye import __version__
from rye.application import Application
from rye.config import config_dict_from_file, get_config


class DefaultGroup(Group):
    def parse_args(self, ctx, args):
        self.invoke_without_command = True
        if not args:
            args.insert(0, "run")
        return super(DefaultGroup, self).parse_args(ctx, args)

    def resolve_command(self, ctx, args):
        base = super(DefaultGroup, self)
        cmd_name, cmd, args = base.resolve_command(ctx, args)
        return cmd_name, cmd, args


@click.group(cls=DefaultGroup)
@click.pass_context
@click.option("-v", "--version", is_flag=True)
@click.option("-c", "--context", help="Specify an extra context for this execution")
def cli(ctx, version, context):
    if version:
        echo(__version__)
        Exit(0)
    ctx.obj = get_config()
    ctx.obj.push_context(context)


@cli.command()
@click.pass_obj
@click.argument("tasks", nargs=-1, default=None)
@click.option("-e", "--envs")
def run(config: SettingsManager, envs, tasks):
    envs = envs.split(",") if envs else None
    app = Application(config, tasks=tasks, envs=envs)
    raise Exit(code=app.run())


@cli.command()
@click.pass_obj
@click.argument("envs", nargs=-1, default=None)
def build_envs(config: SettingsManager, envs):
    app = Application(config)
    Exit(code=app.build_envs(envs))


@cli.command()
def list_tasks():
    data = config_dict_from_file()
    for key in [k for k in data if len(k.split("task.")) > 1]:
        echo(key.split("task.")[-1])
    Exit()
