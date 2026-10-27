import tempfile
import unittest
from pathlib import Path
from core.renamer import rename_files

class EpisodeMappingTests(unittest.TestCase):
    def test_mapped_lupin_and_default_behavior(self):
        mapping={"2":{"season":1,"episode_offset":5},"3":{"season":2},"4":{"season":3}}
        episode_map={(1,3):dict(season_number=1,episode_number=3,episode_name='Chapter 3',season_name='Season 1'),(1,8):dict(season_number=1,episode_number=8,episode_name='Chapter 8',season_name='Season 1'),(3,5):dict(season_number=3,episode_number=5,episode_name='Chapter 5',season_name='Part 4')}
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'source';source.mkdir()
            dest=Path(tmp)/'output'
            for name in ('Lupin.S02E03.mkv','Lupin.S04E05.mkv','Lupin.S01E03.mkv'):
                (source/name).write_bytes(b'video')
            rename_files({'name':'Lupin','first_air_date':'2021-01-08'},str(source),str(dest),episode_map,r'S(\d{1,2})E(\d{1,2})',False,False,True,mapping)
            self.assertTrue((dest/'Lupin (2021)'/'Season 1'/'Episode 08 - Chapter 8'/'S01E08.mkv').exists() is False) # dry run no writing
            rename_files({'name':'Lupin','first_air_date':'2021-01-08'},str(source),str(dest),episode_map,r'S(\d{1,2})E(\d{1,2})',False,False,False,mapping)
            self.assertTrue((dest/'Lupin (2021)'/'Season 1'/'Episode 08 - Chapter 8'/'S01E08.mkv').exists())
            self.assertTrue((dest/'Lupin (2021)'/'Season 3'/'Episode 05 - Chapter 5'/'S03E05.mkv').exists())
            self.assertTrue((dest/'Lupin (2021)'/'Season 1'/'Episode 03 - Chapter 3'/'S01E03.mkv').exists())

if __name__=='__main__': unittest.main()
