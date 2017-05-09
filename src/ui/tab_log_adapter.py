# coding=utf-8

import abc

from src.ui.itab import MainUiTabMethod

TAB_NAME = 'Log'


class TabLogAdapter:
    @MainUiTabMethod(TAB_NAME)
    @abc.abstractmethod
    def tab_log_write(self, *args, **kwargs):
        """"""