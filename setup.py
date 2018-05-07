from cx_Freeze import setup, Executable

executables = [
    Executable('APOD_DB.py')
]

setup(name='APOD_DB',
      version='0.1',
      description='APOD_DB setup script',
      executables=executables
      )