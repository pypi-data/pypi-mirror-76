"""Cookiecutter repository functions."""
import os
import re

from cookiecutter.exceptions import RepositoryNotFound, ContextFileNotFound
from cookiecutter.vcs import clone
from cookiecutter.zipfile import unzip

REPO_REGEX = re.compile(
    r"""
# something like git:// ssh:// file:// etc.
((((git|hg)\+)?(git|ssh|file|https?):(//)?)
 |                                      # or
 (\w+@[\w\.]+)                          # something like user@...
)
""",
    re.VERBOSE,
)

valid_context_files = [
    'nuki.json',
    'nuki.yaml',
    'nuki.yml',
    'nuki.hcl',
    'nukikata.json',
    'nukikata.yaml',
    'nukikata.yml',
    'nukikata.hcl',
    'cookiecutter.json',
    'cookiecutter.yaml',
    'cookiecutter.yml',
    'cookiecutter.hcl',
]

cookiecutter_gen = None


def is_repo_url(value):
    """Return True if value is a repository URL."""
    return bool(REPO_REGEX.match(value))


def is_zip_file(value):
    """Return True if value is a zip file."""
    return value.lower().endswith('.zip')


def expand_abbreviations(template, abbreviations):
    """Expand abbreviations in a template name.

    :param template: The project template name.
    :param abbreviations: Abbreviation definitions.
    """
    if template in abbreviations:
        return abbreviations[template]

    # Split on colon. If there is no colon, rest will be empty
    # and prefix will be the whole template
    prefix, sep, rest = template.partition(':')
    if prefix in abbreviations:
        return abbreviations[prefix].format(rest)

    return template


def repository_has_cookiecutter_json(repo_directory, context_file=None):
    """Determine if `repo_directory` contains a `cookiecutter.json` file.

    :param repo_directory: The candidate repository directory.
    :param context_file:
    :return: True if the `repo_directory` is valid, else False.
    """
    global cookiecutter_gen
    repo_directory_exists = os.path.isdir(repo_directory)
    if context_file:
        context_file_exists = os.path.isfile(
            os.path.join(os.path.abspath(repo_directory), context_file)
        )
        if context_file_exists:
            # The supplied context file exists
            cookiecutter_gen = 'nukikata'
            return context_file

    if repo_directory_exists:
        # Check for valid context files as default
        for f in valid_context_files:
            if os.path.isfile(os.path.join(repo_directory, f)):
                if f.startswith('cookiecutter'):
                    cookiecutter_gen = 'cookiecutter'
                else:
                    cookiecutter_gen = 'nukikata'
                return f
    else:
        return False


def determine_repo_dir(
    template,
    abbreviations,
    clone_to_dir,
    checkout,
    no_input,
    context_file=None,
    password=None,
    directory=None,
):
    """
    Locate the repository directory from a template reference.

    Applies repository abbreviations to the template reference.
    If the template refers to a repository URL, clone it.
    If the template is a path to a local repository, use it.

    :param template: A directory containing a project template directory,
        or a URL to a git repository.
    :param abbreviations: A dictionary of repository abbreviation
        definitions.
    :param clone_to_dir: The directory to clone the repository into.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param no_input: Prompt the user at command line for manual configuration?
    :param password: The password to use when extracting the repository.
    :param directory: Directory within repo where cookiecutter.json lives.
    :return: A tuple containing the cookiecutter template directory, and
        a boolean descriving whether that directory should be cleaned up
        after the template has been instantiated.
    :raises: `RepositoryNotFound` if a repository directory could not be found.
    """
    template = expand_abbreviations(template, abbreviations)
    if is_zip_file(template):
        unzipped_dir = unzip(
            zip_uri=template,
            is_url=is_repo_url(template),
            clone_to_dir=clone_to_dir,
            no_input=no_input,
            password=password,
        )
        repository_candidates = [unzipped_dir]
        cleanup = True
    elif is_repo_url(template):
        cloned_repo = clone(
            repo_url=template,
            checkout=checkout,
            clone_to_dir=clone_to_dir,
            no_input=no_input,
        )
        repository_candidates = [cloned_repo]
        cleanup = False
    else:
        repository_candidates = [template, os.path.join(clone_to_dir, template)]
        cleanup = False

    if directory:
        repository_candidates = [
            os.path.join(s, directory) for s in repository_candidates
        ]

    for repo_candidate in repository_candidates:
        if context_file:
            if not os.path.exists(context_file):
                raise ContextFileNotFound(
                    'The context file "{}" could not be found'.format(context_file)
                )
        context_file = repository_has_cookiecutter_json(repo_candidate, context_file)
        if not context_file:
            # Means that no valid context file has been found or provided
            continue
        else:
            return repo_candidate, context_file, cleanup

    raise RepositoryNotFound(
        'A valid repository for "{}" could not be found in the following '
        'locations:\n{}'.format(template, '\n'.join(repository_candidates))
    )
