##########################################################################
# Copyright (c) Open Law Library. All rights reserved.                   #
# See ThirdPartyNotices.txt in the project root for license information. #
##########################################################################
import pytest

from pygls import features
from pygls.exceptions import (CommandAlreadyRegisteredError,
                              FeatureAlreadyRegisteredError, ValidationError)


def test_register_command_validation_error(feature_manager):

    with pytest.raises(ValidationError):
        @feature_manager.command(' \n\t')
        def cmd1():  # pylint: disable=unused-variable
            pass


def test_register_commands(feature_manager):
    cmd1_name = 'cmd1'
    cmd2_name = 'cmd2'

    @feature_manager.command(cmd1_name)
    def cmd1():
        pass

    @feature_manager.command(cmd2_name)
    def cmd2():
        pass

    reg_commands = feature_manager.commands.keys()

    assert cmd1_name in reg_commands
    assert cmd2_name in reg_commands

    assert feature_manager.commands[cmd1_name] is cmd1
    assert feature_manager.commands[cmd2_name] is cmd2


def test_register_feature_with_options(feature_manager):

    options = {
        'opt1': 1,
        'opt2': 2
    }

    @feature_manager.feature(features.COMPLETION, **options)
    def completions():
        pass

    reg_features = feature_manager.features.keys()
    reg_feature_options = feature_manager.feature_options.keys()

    assert features.COMPLETION in reg_features
    assert features.COMPLETION in reg_feature_options

    assert feature_manager.features[features.COMPLETION] is completions
    assert feature_manager.feature_options[features.COMPLETION] == options


def test_register_features(feature_manager):

    @feature_manager.feature(features.COMPLETION)
    def completions():
        pass

    @feature_manager.feature(features.CODE_LENS)
    def code_lens():
        pass

    reg_features = feature_manager.features.keys()

    assert features.COMPLETION in reg_features
    assert features.CODE_LENS in reg_features

    assert feature_manager.features[features.COMPLETION] is completions
    assert feature_manager.features[features.CODE_LENS] is code_lens


def test_register_same_command_twice_error(feature_manager):

    with pytest.raises(CommandAlreadyRegisteredError):

        @feature_manager.command('cmd1')
        def cmd1():  # pylint: disable=unused-variable
            pass

        @feature_manager.command('cmd1')
        def cmd2():  # pylint: disable=unused-variable
            pass


def test_register_same_feature_twice_error(feature_manager):

    with pytest.raises(FeatureAlreadyRegisteredError):

        @feature_manager.feature(features.CODE_ACTION)
        def code_action1():  # pylint: disable=unused-variable
            pass

        @feature_manager.feature(features.CODE_ACTION)
        def code_action2():  # pylint: disable=unused-variable
            pass
