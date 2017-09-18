from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('cal.py', base=base)
]

setup(name='thucal-py',
      version = '1.0',
      description = 'A python program to transform xls into ics',
      options = dict(build_exe = buildOptions),
      executables = executables)
