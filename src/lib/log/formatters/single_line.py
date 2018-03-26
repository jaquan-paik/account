import traceback
from logging import Formatter


class SingleLineFormatter(Formatter):
    def formatException(self, ei):
        e_traceback = traceback.format_exception(ei[0], ei[1], ei[2])
        traceback_lines = []
        for line in e_traceback:
            line = line.rstrip('\n')
            traceback_lines.extend(line.splitlines())

        return str(traceback_lines)

    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            s = s + '\t' + record.exc_text
        if record.stack_info:
            s = s + '\t' + self.formatStack(record.stack_info)
        return s
