import os
import git
import sys
import re
from riscof.utils import yaml
import riscof.utils as utils
import collections
import logging
from git import InvalidGitRepositoryError
import riscof.constants as constants

logger = logging.getLogger(__name__)

class DbgenError(Exception):
    pass


def dirwalk(dir,ignore_dirs=[]):
    '''
        Recursively searches a directory and returns a list of
        relative paths(from the directory) of the files which end with ".S"(excluding any folder named wip).

        :params: dir - The directory in which the files have to be searched for.

        :return: a list of all .S file paths relative to the riscof home.
    '''
    list = []
    for root, dirs, files in os.walk(dir):
        if not any([i in root for i in ignore_dirs]):
            path = root[root.find(dir):] + "/"
            for file in files:
                if file.endswith(".S"):
                    list.append(os.path.join(path, file))
    return list


def orderdict(foo):
    '''
        Creates and returns a sorted dictionary from a given dictionary.
        :params foo: The dictionary which needs to be sorted.

        :type foo: dict

        :return: A dictionary with alphabetically sorted(based on keys) entries.

    '''
    ret = collections.OrderedDict()
    for key in sorted(foo.keys()):
        ret[key] = foo[key]
    return ret


def createdict(file):
    '''
        Parse the file and create the dictionary node for it.

        :param file: The relative path of the test from riscof home.

        :type file: str

        :return: A dictionary containing all the necesary nodes for the file.

        :raise DbgenError: Raised if the test file doesnt adhere to the rules.
    '''
    with open(file, "r") as k:
        lines = k.read().splitlines()
        code_start = False
        part_start = False
        isa = None
        part_number = ''
        i = 0
        part_dict = {}
        while i < len(lines):
            line = lines[i]
            i += 1
            line = line.strip()
            if line == "":
                continue
            if (line.startswith("#") or line.startswith("//")):
                continue
            if "RVTEST_ISA" in line:
                isa = (((line.strip()).replace('RVTEST_ISA(\"',
                                               "")).replace("\")", "")).strip()
            if "RVTEST_CASE(" in line:
                args = [(temp.strip()).replace("\"", '') for temp in (
                    line.strip()).replace('RVTEST_CASE', '')[1:-1].split(',')]
                part_number = args[0]
                conditions = (','.join(args[1:]).replace("//", '')).split(";")
                while (line.endswith('\\')):
                    line = lines[i]
                    i += 1
                    line = (line.strip()).replace("//", '')
                    conditions.append(str(
                        (line.replace("\")", '')).replace("//", '')).split(";"))
                    # args.append([(temp.strip()).replace("\")",'') for temp in (line.strip())[:-1]].split)
                    if ("\")" in line):
                        break
                if (part_number in part_dict.keys()):
                    logger.warning("{}:{}: Incorrect Naming of Test Case after ({})".
                          format(file, i, part_number))
                    raise DbgenError

                check = []
                define = []
                for cond in conditions:
                    cond = cond.strip()
                    if (cond.startswith('check')):
                        check.append(cond)
                    elif (cond.startswith('def')):
                        define.append(cond)
                part_dict[part_number] = {'check': check, 'define': define}
    if (isa is None):
        logger.warning("{}:ISA not specified.".format( file))
        raise DbgenError
    if len(part_dict.keys()) == 0:
        logger.warning("{}: Atleast one part must exist in the test.".format(file))
        raise DbgenError
    return {'isa': str(isa), 'parts': orderdict(part_dict)}


def generate_standard():
    list = dirwalk(os.path.join(constants.root, constants.suite),['/wip'])
    repo_path = os.path.normpath(constants.root+"/../")
    try:
        repo = git.Repo(repo_path)
    except InvalidGitRepositoryError:
        logger.error("This feature is available for developers only.")
        raise SystemExit
    dbfile = constants.framework_db
    logger.debug("Using "+dbfile)
    tree = repo.tree()
    try:
        db = utils.load_yaml(dbfile)
        delkeys = []
        for key in db.keys():
            if key not in list:
                delkeys.append(key)
        for key in delkeys:
            del db[key]
    except FileNotFoundError:
        db = {}
    cur_dir = constants.root
    existing = db.keys()
    new = [x for x in list if x not in existing]
    for file in existing:
        try:
            commit = next(
                repo.iter_commits(paths=file, max_count=1))
            if (str(commit) != db[file]['commit_id']):
                temp = createdict(os.path.join(cur_dir, file))
                db[file.replace(os.path.join(repo_path,"riscof/"),"")] = {'commit_id': str(commit), **temp}
        except DbgenError:
            del db[file.replace(os.path.join(repo_path,"riscof/"),"")]
    for file in new:
        try:
            commit = next(
                repo.iter_commits(paths=file, max_count=1))
            temp = createdict(os.path.join(cur_dir, file))
            db[file.replace(os.path.join(repo_path,"riscof/"),"")] = {'commit_id': str(commit), **temp}
        except DbgenError:
            continue
    with open(dbfile, "w") as wrfile:
        yaml.dump(orderdict(db),
                  wrfile)

def generate():
    file_list = dirwalk(constants.suite)
    dbfile = constants.framework_db
    db = {}
    for file in file_list:
        try:
            temp = createdict(file)
            db[file] = {'commit_id':'0',**temp}
        except DbgenError:
            continue
    with open(dbfile, "w") as wrfile:
        yaml.dump(orderdict(db),
                  wrfile)


if __name__ == '__main__':
    generate_standard()
