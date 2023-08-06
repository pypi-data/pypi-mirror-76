import click
from rich import print
from gnote import __about__
from rich.columns import Columns
from rich.table import Table
import gnote
from gnote import util

from gnote import note


@click.group()
def entry():
    """
    code-note
    代码笔记本，记录常用的代码例子，解释等
    """


@click.command()
def about():
    """关于"""
    table = Table('名称', '详情')
    table.add_row('版本', __about__.__version)
    table.add_row('作者', __about__.__author)
    table.add_row('邮箱', __about__.__author_email)
    table.add_row('git地址', gnote.repo_url)
    table.add_row('本地仓库地址', str(gnote.repo_dir))
    print(table)


@click.command()
def version():
    """版本"""
    click.echo(__about__.__version)


@click.command()
def ls():
    lst = util.list_note().keys()
    t = Table('名称')
    for i in lst:
        t.add_row(i)
    print(t)


@click.command()
@click.argument('name', type=click.STRING, autocompletion=note.auto_complete)
def cat(name):
    md = note.cat(name)
    print(md)


@click.command()
@click.argument('name')
def search(name):
    lst = note.search(name)
    print(Columns(lst, expand=True))


@click.command()
@click.argument('name')
def pyvim(name):
    note.pyvim(name)


@click.command()
@click.argument('name')
def code(name):
    util.code(name)


@click.command()
def path():
    p = note.open_root_path()
    click.echo(str(p))


@click.command()
def push():
    pass


entry.add_command(about)
entry.add_command(version)
entry.add_command(ls)
entry.add_command(cat)
entry.add_command(search)
entry.add_command(pyvim)
entry.add_command(code)
entry.add_command(path)
