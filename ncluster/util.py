import random
import string
import time
from collections import Iterable
import shlex

# starting value for now_micros (Aug 31, 2018)
# using this to make various timestamped names shorter
EPOCH_MICROS=1535753974788163

def is_iterable(k):
  return isinstance(k, Iterable)


def now_micros(absolute=False) -> int:
  """Return current micros since epoch as integer."""
  micros = int(time.time()*1e6)
  if absolute:
    return micros
  return micros - EPOCH_MICROS


def now_millis(absolute=False) -> int:
  """Return current micros since epoch as integer."""
  millis = int(time.time()*1e3)
  if absolute:
    return millis
  return millis - EPOCH_MICROS/1000


def log_error(*args, **kwargs):
  print(f"Error encountered {args} {kwargs}")


def log(*args, **kwargs):
  print(f"{args} {kwargs}")


def install_pdb_handler():
  """Make CTRL+\ break into gdb."""
  
  import signal
  import pdb

  def handler(_signum, _frame):
    pdb.set_trace()
  signal.signal(signal.SIGQUIT, handler)


def shell_add_echo(script):
  """Goes over each line script, adds "echo cmd" in front of each cmd.

  ls a

  becomes

  echo * ls a
  ls a
  """
  new_script = ""
  for cmd in script.split('\n'):
    cmd = cmd.strip()
    if not cmd:
      continue
    new_script += "echo \\* " + shlex.quote(cmd) + "\n"
    new_script += cmd+"\n"
  return new_script


def shell_strip_comment(cmd):
  """ hi # testing => hi"""
  if '#' in cmd:
    return cmd.split('#', 1)[0]
  else:
    return cmd


def random_id(N=5):
  """Random id to use for AWS identifiers."""
  #  https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
  return ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))


def reverse_taskname(name: str) -> str:
  """
  Reverses components in the name of task. Reversed convention is used for filenames since
  it groups log/scratch files of related tasks together

  0.somejob.somerun -> somerun.somejob.0
  0.somejob -> somejob.0
  somename -> somename

  Args:
    name: name of task

  """
  components = name.split('.')
  assert len(components) <= 3
  return '.'.join(components[::-1])
