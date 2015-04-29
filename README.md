# Apache Derby DB tools for XL Release and XL Deploy

This project introduces an XL Release and XL Deploy plugin which adds some tools to manage the embedded Apache Derby database. It is useful if your installation of XL Release or XL Deploy runs on the Derby database, which comes by default.

## Installation

Requirements:

* XL Release 4.6.0 or higher.
* XL Deploy 4.5.0 or higher.

To install the plugin you have to:

1. Download the [`xl-apache-derby-tools-plugin-1.0.jar`](https://github.com/xebialabs-community/xl-apache-derby-tools-plugin/releases/download/v1.0/xl-apache-derby-tools-plugin-1.0.jar) into `XLR_or_XLD_HOME/plugins/`.
2. Start the server.

## Usage

### Compressing Apache Derby database files

If you deleted a lot of data from your XL* installation then you would expect that the size taken by the repository would decrease. However this is not fully the case, because Apache Derby database [does not return unused space to the operating system](https://db.apache.org/derby/docs/10.2/ref/rrefaltertablecompress.html) and keeps it ready to fill with new rows. This is OK in normal situations, but if you did a cleanup of your data you might want your repository size to become small again.

To force compressing of database files there is a special system call, which is implemented in this plugin. You can run it using following `curl` statement, assuming your XL Release or XL Deploy is available at http://localhost:5516/my-xl/:

    curl --user admin -X POST http://localhost:5516/my-xl/api/extension/shrink-db

This works if you have default configuration of repository (`jackrabbit-repository.xml` file). If you have a custom configuration, for example [the one which stores everything in one database](https://github.com/xebialabs-community/xl-apache-derby-hot-backup/blob/master/src/main/resources/sample/jackrabbit-repository.xml), then you have to provide additional query parameters:

    curl --user admin -X POST http://localhost:5516/my-xl/api/extension/shrink-db\?defaultDb\=repository/db\&versionDb\=repository/db

The parameters are:

* `defaultDb` is the path to the database of the "default" Jackrabbit workspace, `repository/workspaces/default/db` by default. Path is relative to the server installation directory.
* `versionDb` is the path to the database of the "version" Jackrabbit workspace, `repository/version/db` by default.

Compressing works quite fast. For example, it takes less than 10 seconds to compress database after removing 2000 releases from XL Release.

Note that only _admin_ users are allowed to make this call.

Note also that this action has nothing to do with Lucene indexes. Lucene indexes are compressing automatically to some extent, but if you want them to become really small, the only way is to rebuild them from scratch.
