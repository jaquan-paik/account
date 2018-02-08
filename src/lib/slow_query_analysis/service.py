import tempfile
from datetime import datetime
from subprocess import check_output

from django.db import connections

from lib.email.services import email_service
from .config import AnalysisSlowQueryConfig


def analyze_slow_query() -> None:
    analysis_result = ''

    for db_alias in AnalysisSlowQueryConfig.get_analysis_db_list():
        analysis_result += '== ' + db_alias + '\n' + str(_analyze_db_slow_query(db_alias)) + '\n\n'

    email_service.send(
        AnalysisSlowQueryConfig.get_analysis_from_mail(),
        AnalysisSlowQueryConfig.get_analysis_to_mails(),
        '[Slow Query Analysis] %s' % datetime.now().date(),
        text=analysis_result
    )


def _analyze_db_slow_query(db_alias) -> str:
    cursor = connections[db_alias].cursor()

    cursor.execute('''
    SELECT CONCAT(
        '# Time: ', DATE_FORMAT(start_time, '%y%m%d %H:%i:%s'), CHAR(10),
        '# User@Host: ', user_host, CHAR(10),
        '# Query_time: ', TIME_TO_SEC(query_time),
        ' Lock_time: ', TIME_TO_SEC(lock_time),
        ' Rows_sent: ', rows_sent,
        ' Rows_examined: ', rows_examined, CHAR(10),
        'SET timestamp=', UNIX_TIMESTAMP(start_time), ';', CHAR(10),
        IF(FIND_IN_SET(sql_text, 'Sleep,Quit,Init DB,Query,Field List,Create DB,Drop DB,Refresh,Shutdown,Statistics,Processlist,Connect,Kill,Debug,Ping,Time,Delayed insert,Change user,Binlog Dump,Table Dump,Connect Out,Register Slave,Prepare,Execute,Long Data,Close stmt,Reset stmt,Set option,Fetch,Daemon,Error'),
        CONCAT('# administrator command: ', sql_text), sql_text),
        ';'
        ) AS `slow-log`
        FROM `mysql`.`slow_log`
        where start_time > subdate(now(), 1)
    ''')  # flake8: noqa: E501

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        while True:
            row = cursor.fetchone()
            if row is None:
                break

            temp.write(row[0])

        temp.flush()
        analysis_result = check_output(['pt-query-digest', temp.name])
        return analysis_result.decode('UTF-8')
