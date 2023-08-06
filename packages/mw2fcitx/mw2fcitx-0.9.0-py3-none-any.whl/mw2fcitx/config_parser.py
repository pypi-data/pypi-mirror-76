from mw2fcitx.utils import console


def confparser(filename):
    console.debug("Parsing config file: {}".format(filename))
    exec(compile(open(filename).read(), filename, 'exec'))
