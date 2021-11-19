# Config

Configuration details & files for MySQL servers

--------------------------------------------------------------------------------

## Files & Folders

-   `migrations`
    -   Folder containing database migration files. Files are written in
        MySQL 8-flavored SQL, and should be encompassed within a single
        transaction (e.g. `BEGIN; ... COMMIT;`). Filenames currently use the
        Flyway-style filenames
        -   _Versioned Migrations_ begin with a 'V', and contain a version
            number and description. The version number directly follows the 'V',
            and is separated from the description by a double underscore. For
            example, a valid Versioned Migration filename is:
            `V2__new_table.sql`. Versioned Migrations are applied exactly once,
            and in order by version number.
        -   _Undo Migrations_ follow a similar convention to Versioned
            Migrations, but begin with a 'U'. Undo Migrations are not applied by
            default. Their intent is to _undo_ the corresponding Versioned
            Migration. Because of this, each Versioned Migration should have a
            matching Undo Migration. If needed, Undo Migrations should be
            applied in reverse numeric order as needed, starting from the last
            applied Versioned Migration.
    -   All Migrations should be tested in a sandbox to verify functionality.
    -   There is no DB migration version tracking at this time, therefore it is
        expected that the Production DB has all migrations that have been
        pushed to `master`.
-   `named-queries`
    -   Folder containing Ignition Named Queries. These are likely not entirely
        valid SQL, as they will feature Ignition's custom templating language.
        Filenames should match the Named Query name in Ignition. As we currently
        have a single active Ignition project, it is expected that all queries
        belong to that project.
-   `my.cnf`
    -   MySQL configuration file containing group replication settings. Requires
        server-specific configuration.

--------------------------------------------------------------------------------



[Main README][]

[Main README]: ../README.md
