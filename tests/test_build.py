from configparser import ConfigParser
from clara.plugins.clara_build import main
import pytest
#from clara.utils import get_from_config



def fakeconfig():
    config = ConfigParser()
    config.read("../example-conf/config.ini")
    return config


def test_main(mocker):
    def fakedocopt(doc, argv=None, options_first=False):
        fake_options = {'<dist>': 'calibre9',
                        'source': True,
                        '<dsc_file>': 'clara_0.20190424-0sci8u1.dsc'}
        return fake_options

    mocker.patch("clara.plugins.clara_build.docopt.docopt",
                 side_effect=fakedocopt)

    mocker.patch("clara.utils.getconfig",
                 side_effect=fakeconfig)

    m_exit = mocker.patch("clara.plugins.clara_build.sys.exit")
    m_p_info = mocker.patch("clara.plugins.clara_build.print_info")
    m_chdir = mocker.patch("clara.plugins.clara_build.os.chdir")
    m_subprocess = mocker.patch("clara.plugins.clara_build.subprocess.call")
    m_logging = mocker.patch("clara.plugins.clara_build.logging.debug")

    main()


    m_exit.assert_called_with("The file /root/cowbuilder-calibre9 doesn't exist")
    m_p_info.assert_called_with('clara', '0.20190424-0sci8u1', '0.20190424', '0sci8u1')
    m_subprocess.assert_any_call(['dpkg-source', '-x', 'clara_0.20190424-0sci8u1.dsc'])
    m_subprocess.assert_any_call(['dch',
                                  '--force-distribution',
                                  '-D',
                                  'calibre9',
                                  '-v', u'0.20190424-0sci8u1+c9+1',
                                  'Rebuild for calibre9.'])
    m_logging.assert_any_call(u'/root/cowbuilder-calibre9 --build clara_0.20190424-0sci8u1+c9+1.dsc')

    #m_subprocess.assert_any_call(['/root/cowbuilder-calibre9', '--build','clara_0.20190424-0sci8u1.dsc'])
    #([u'/root/cowbuilder-calibre9',\n  '--build',\n  'clara_0.20190424-0sci8u1+c9+1.dsc'])
