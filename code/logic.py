import importlib.util
import os
from subprocess import Popen, PIPE, TimeoutExpired
from logging import getLogger

from const import TIMEOUT, LANGUAGES, TASK_MODULE_PATH
from exceptions import CallError
import task_loader


logger = getLogger('app')

# dynamic file loading
task_module = task_loader.load_module(
    task_path=TASK_MODULE_PATH,
)


def execute_cmd(code, lang):
    cmd = LANGUAGES.get(lang)
    if cmd is None:
        raise CallError(err='wrong language')
    args_list = task_module.make_arguments()
    for args in args_list:
        assert_call(cmd, code, args)


def decode_output(output):
    if not output:
        return ''
    return output.decode('utf-8', errors='replace')


def assert_call(cmd_args, code, args):
    cmd_args = cmd_args + [str(arg) for arg in args]
    cmd_args = [
        'nsjail',
        '-Mo',
        '--user', '4242',
        '--group', '4242',
        '--chroot', '/',
        # with this flag, nodejs is VERY VERY SLOW OMG
        # '--cgroup_cpu_ms_per_sec', '100',
        '--cgroup_pids_max', '64',
        '--cgroup_mem_max', '67108864',
        '--rlimit_as=max',
        '--disable_clone_newcgroup',
        '--disable_proc',
        '--iface_no_lo',
        '-Q',
        '--',
    ] + cmd_args
    correct = task_module.do_it(*args)

    process = None
    try:
        process = Popen(
            args=cmd_args,
            stdin=PIPE, stdout=PIPE, stderr=PIPE,
            env={'PYTHONIOENCODING': 'UTF-8'},
        )
        output, err_output = process.communicate(code.encode('utf-8'), timeout=TIMEOUT)
    except TimeoutExpired as exp:
        raise CallError(err='timeout :(', args=args)
    except Exception as exp:
        logger.exception('!!!')
        raise CallError(err='something is wrong: %s' % exp, args=args)
    finally:
        if process is not None:
            process.kill()

    output = decode_output(output)
    err_output = decode_output(err_output)

    if process.returncode != 0 or output != correct:
        raise CallError(
            wrong=output,
            correct=correct,
            err=err_output,
            args=args,
        )
