#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from java.sql import DriverManager
from org.springframework.security.core.context import SecurityContextHolder


def is_current_user_admin():
    authentication = SecurityContextHolder.getContext().getAuthentication()
    return authentication.getPrincipal() == "admin"


def db_url(db_path):
    return "jdbc:derby:%s;create=false" % db_path


def shrink_db(db_path, tables):
    conn = DriverManager.getConnection(db_url(db_path), "", "")
    for table in tables:
        logger.info("Shrinking table %s" % table)
        cs = conn.prepareCall("CALL SYSCS_UTIL.SYSCS_COMPRESS_TABLE('APP', '%s', 1)" % table)
        cs.execute()
        cs.close()
    conn.close()


def jackrabbit_tables(prefix):
    return map(lambda t: prefix + t, ['BUNDLE', 'REFS', 'BINVAL', 'NAMES'])


if not is_current_user_admin():
    response.statusCode = 403
    response.entity = "Only the 'admin' user can run this action"

else:
    default_db_path = request.query.get('defaultDb', 'repository/workspaces/default/db')
    version_db_path = request.query.get('versionDb', 'repository/version/db')

    logger.info('Shrinking Apache Derby databases by paths [%s] and [%s]' % (default_db_path, version_db_path))

    shrink_db(default_db_path, jackrabbit_tables('DEFAULT_'))
    shrink_db(version_db_path, jackrabbit_tables('VERSION_'))
