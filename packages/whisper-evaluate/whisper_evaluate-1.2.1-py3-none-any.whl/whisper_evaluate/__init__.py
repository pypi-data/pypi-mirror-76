from whisper_evaluate.statistics import Statistics
from whisper_evaluate.whisper_statistics import WhisperStatistics
from whisper_evaluate.netease_statistics import NetEaseStatistics
from whisper_evaluate.report import Report
from whisper_evaluate.utils import context_test_single, regression_test_single
import sys
import logging as log

log.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=log.INFO,
    stream=sys.stdout)
