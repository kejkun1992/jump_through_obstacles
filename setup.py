from distutils.core import setup
import py2exe

'''settings of .exe file'''

setup(
        windows = [
                {'script':'jump.py',
                'icon_resources':[(1,'icon\\icon.ico')]
                }
                ],
        data_files = [
                ('scores',['scores\\scores.txt']),
                ('graphics',['graphics\\background_800x400.png','graphics\\background2_800x400.png'])
                ]
      )
