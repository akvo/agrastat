import click
import subprocess
from ckan.model import Session, Vocabulary, Tag, PackageTag
from .data.countries import country_list, create_countries


@click.group(name="agra")
def agra():
    """CKAN CLI commands for Agra"""
    pass


@agra.command(name="fixer-dev")
def fixer_dev():
    """Runs the fixer-dev command"""
    click.echo("Running fixer-dev for Agra!")


@agra.command(name="regenerate-vocabulary")
@click.argument("vocabulary", type=str)
def regenerate_vocabulary(vocabulary):
    """Regenerates a specific vocabulary"""
    if vocabulary == "countries":
        vocab = Vocabulary.get(vocabulary)
        if not vocab:
            click.echo("Countries not found: Creating countries vocabulary")
            create_countries()
            return
        else:
            click.echo("Countries found: Deleting and recreating")
            tags = (
                Session.query(Tag).filter(Tag.vocabulary_id == vocab.id).all()
            )
            for tag in tags:
                Session.query(PackageTag).filter(
                    PackageTag.tag_id == tag.id
                ).delete()
                Session.delete(tag)
            Session.delete(vocab)
            Session.commit()
            create_countries()
            try:
                subprocess.run(["ckan", "search-index", "rebuild"], check=True)
                click.echo("Search index rebuild completed!")
            except subprocess.CalledProcessError as e:
                click.echo(f"Error rebuilding index: {e}", err=True)
            return
    else:
        click.echo("Vocabulary not found")
        return
