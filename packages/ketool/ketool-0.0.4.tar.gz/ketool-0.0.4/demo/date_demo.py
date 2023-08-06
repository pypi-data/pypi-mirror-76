#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc :
from ketool import date

ms_timestamp = date.timeStamp()
timestamp = date.timeStamp(ms=False)
print(ms_timestamp, timestamp)
