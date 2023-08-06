# -*- coding: utf-8 -*-

""" CapoConfig tests """

import os
import shutil
import subprocess
import sys
import unittest
from enum import Enum
from pathlib import Path

import pytest

from pycapo import CapoConfig

_TEST_PROFILES = ['dev_profile', 'prod_profile', 'empty_profile']

class Keys(Enum):
    ''' Keys in our fake Capo profiles '''
    METADATA_USER = 'TUNES.LOONEY.METADATADATABASE.JDBCUSERNAME'
    METADATA_PW   = 'TUNES.LOONEY.METADATADATABASEJDBCPASSWORD'
    METADATA_URL  = 'TUNES.LOONEY.METADATADATABASEJDBCURL'
    OTHER_USER    = 'TUNES.LOONEY.SOMEOTHERDATABASEJDBCUSERNAME'
    OTHER_PW      = 'TUNES.LOONEY.SOMEOTHERDATABASEJDBCPASSWORD'
    OTHER_URL     = 'TUNES.LOONEY.SOMEOTHERDATABASEJDBCURL'

class PycapoTestCase(unittest.TestCase):
    ''' Tests for pycapo and CapoConfig() '''

    @classmethod
    def setUpClass(cls) -> None:
        cls.get_props_files(cls)
        cls.capo_dir_was_created = False

    @classmethod
    def tearDownClass(cls) -> None:
        cls.delete_properties(cls)

    def test_capo_copes_with_bad_path(self):
        ''' if capo path is bad, capo should default to something usual
            rather than crashing
        '''
        user = os.environ['USER']
        for profile in _TEST_PROFILES:
            capo_config = CapoConfig(profile=profile, path='foo')
            self.assertTrue(user in capo_config.getpath())
            try:
                for key, val in capo_config.getoptions().items():
                    if 'prod' not in profile:
                        self.assertFalse('prod' in val)
                        if key == Keys.OTHER_URL.value:
                            self.assertTrue('dev' in val)
                    else:
                        if key == Keys.METADATA_USER.value:
                            self.assertTrue('_ro' not in val)
                        if key == Keys.OTHER_URL.value:
                            self.assertTrue('prod' in val)
            except Exception as exc:
                pytest.fail(f'failure for {capo_config.profile}, '
                            f'{capo_config.getpath()}: {exc}')

    def test_gets_expected_values_for_profile(self):
        ''' properties files for different profiles may (or may not)
            have disparate values
        '''
        for profile in _TEST_PROFILES:

            try:
                capo_config = CapoConfig(profile=profile)

                try:
                    options = capo_config.getoptions()
                    for key, val in options.items():
                        if key == Keys.OTHER_URL:
                            self.assertTrue('thin' in val)
                        if 'prod' not in profile:
                            self.assertFalse('prod' in val)
                            if key == Keys.OTHER_URL.value:
                                self.assertTrue('dev' in val)
                        else:
                            if key == Keys.METADATA_USER.value:
                                self.assertTrue('_ro' not in val)
                            if key == Keys.OTHER_URL.value:
                                self.assertTrue('prod' in val)
                except Exception as exc:
                    pytest.fail(f'failure for {profile} '
                                f'when {key}=={val}: {exc}')

            except Exception as exc:
                pytest.fail(f'failure for {profile}: {exc}')

    def test_capo_config_handles_bad_args_expectedly(self):
        ''' CapoConfig() should complain when given bad args or none '''
        with pytest.raises(ValueError):
            CapoConfig(profile=None)
            CapoConfig()
            CapoConfig(path='foo')

        bogus_config = CapoConfig(profile='bogus')
        # CapoConfig() should NOT have any default values
        self.assertEqual(0, len(bogus_config.getoptions()))
        self.assertEqual(0, len(bogus_config.getlocations()))

    def test_missing_setting_fails_expectedly(self):
        ''' missing Capo setting should return appropriate code '''
        with pytest.raises(SystemExit) as exc:
            CommandLineLauncher().run(profile='empty_profile')
            self.assertEqual(3, exc.value)


    def test_command_line_returns_expected_code(self):
        ''' under various scenarios, pycapo should return appropriate code
            for each
        '''

        # no arguments: should fail w/approp return code
        with pytest.raises(SystemExit) as exc:
            CommandLineLauncher().run()
            self.assertEqual(2, exc.value)
        # one argument, not a k/v pair: should fail w/approp return code
        with pytest.raises(TypeError) as exc:
            CommandLineLauncher().run('dev_profile')
            self.assertEqual(2, exc.value)
        # invalid k/v pair
        with pytest.raises(SystemExit) as exc:
            CommandLineLauncher().run(foo='bar')
            self.assertEqual(1, exc.value)
        # key but no value
        with pytest.raises(SystemExit) as exc:
            CommandLineLauncher().run(profile=None)
            self.assertEqual(1, exc.value)
        # invalid profile
        with pytest.raises(SystemExit) as exc:
            CommandLineLauncher().run(profile='foo')
            self.assertEqual(1, exc.value)
        # no profile; invalid path
        with pytest.raises(SystemExit) as exc:
            CommandLineLauncher().run(path='foo')
            self.assertEqual(1, exc.value)
        # no profile; valid path
        with pytest.raises(SystemExit) as exc:
            CommandLineLauncher().run(path=Path.cwd())
            self.assertEqual(1, exc.value)
        # valid profile, invalid path
        with pytest.raises(SystemExit) as exc:
            CommandLineLauncher().run(profile='dev_profile', path='foo')
            self.assertEqual(1, exc.value)

    ### UTILITIES ###

    def get_props_files(self):
        ''' grab our fake properties files  and copy them to user's .capo dir '''
        user_home = Path(os.environ['HOME'])
        capo_path = user_home / '.capo'
        props_source_dir = Path.cwd() / 'tests/test_data'

        if not capo_path.is_dir():
            capo_path.mkdir()
            self.capo_dir_was_created = True
        for profile in _TEST_PROFILES:
            filename = profile + '.properties'
            source = props_source_dir / filename
            destn = capo_path / filename
            shutil.copy(str(source), str(destn))


    def delete_properties(self):
        ''' delete fake properties files from user's .capo dir '''
        user_home = Path(os.environ['HOME'])
        default_path = user_home / '.capo'
        for profile in _TEST_PROFILES:
            filename = profile + '.properties'
            to_delete = default_path / filename
            if to_delete.is_file():
                to_delete.unlink()
        if self.capo_dir_was_created:
            default_path.unlink()


class CommandLineLauncher:
    ''' launches a system process and executes a pycapo command '''

    def run(self, **kwargs):
        ''' kick off pycapo with these args and grab return code '''
        args = ['pycapo']
        if kwargs:
            for arg in kwargs:
                args.append(arg)

        try:
            proc = subprocess.run(args,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  check=False,
                                  timeout=100,
                                  bufsize=1,
                                  universal_newlines=True)
            if proc.returncode != 0:
                sys.exit(proc.returncode)
            return proc.returncode

        except Exception as exc:
            pytest.fail(f'Error launching pycapo with args {args}: {exc}')


if __name__ == '__main__':
    unittest.main()
