# coding=utf-8

if __name__ == '__main__':
    """Install better exception's hook"""
    # noinspection PyUnresolvedReferences
    import better_exceptions

    """Init Sentry"""
    # noinspection PyUnresolvedReferences
    from src.sentry import SENTRY
    from src.utils.threadpool import register_sentry
    register_sentry(SENTRY)

    """Setup logging"""
    from src.utils.custom_logging import make_logger
    # noinspection PyProtectedMember
    from src.global_ import PATH_LOG_FILE
    from src.misc.logging_handler import persistent_logging_handler

    """Other imports"""
    from src.utils import nice_exit

    try:
        logger = make_logger(__name__, log_file_path=PATH_LOG_FILE, custom_handler=persistent_logging_handler)

    except PermissionError:
        """Another instance is locking the log file"""
        from PyQt5.QtWidgets import QApplication, QMessageBox
        from PyQt5.QtGui import QIcon
        from src.ui import qt_resource
        from src.global_ import APP_SHORT_NAME, DEFAULT_ICON
        # noinspection PyArgumentList
        app = QApplication.instance()

        if not app:
            app = QApplication([])
        msgbox = QMessageBox(
            QMessageBox.Critical,
            'Uh oh...',
            'Another instance of EMFT is already running =)'.format(APP_SHORT_NAME)
        )
        msgbox.setWindowIcon(QIcon(DEFAULT_ICON))
        msgbox.exec()
        nice_exit(0)

    else:

        """Say hello !"""
        from src.__version__ import __version__
        logger.info(__version__)

        """Init config"""
        # noinspection PyUnresolvedReferences
        from src.cfg.cfg import Config
        SENTRY.register_context('config', Config())

        """Intercept SIGINT"""
        import signal as core_sig
        # Intercept OS signals to trigger a nice exit
        core_sig.signal(core_sig.SIGINT, nice_exit)

        import src.emft
        try:
            src.emft.main()
        except SystemExit as e:
            logger.info('caught SystemExit, bye bye !')
            nice_exit(e.code)
        except:
            logger.exception('caught exception in main loop')
            raise
