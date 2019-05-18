import multiprocessing
import ConfigParser
import sys
import os


CONF_FILE = "config.conf"


def get_physical_mem_size():
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    mem_gib = round(mem_bytes/(1024.**3))
    return mem_gib


def get_worker_threads_count():
    cpu_count = multiprocessing.cpu_count()
    mem_size = get_physical_mem_size()
    if (mem_size <= cpu_count):
        return cpu_count

    max_threads = cpu_count * 5
    return max_threads if mem_size >= max_threads else mem_size


def print_line(text="_"):
    part = "_" * 30
    line = part + text + part
    print("\n{}\n".format(line[:70]))


def read_conf_file():
    config = {}
    conf = ConfigParser.SafeConfigParser()
    if os.path.exists(CONF_FILE):
        conf.read([CONF_FILE])
    else:
        return {}
    for sec in conf.sections():
        for k, v in conf.items(sec):
            config[k] = v
    return config
