# mf-ignition

Testbed for Ignition failover/HA cluster.

--------------------------------------------------------------------------------

## Prerequisites
Git, Vagrant and VirtualBox are required. That's about it.

--------------------------------------------------------------------------------

## Folders

### Config
Contains configuration files for the MySQL cluster, database migrations, and
Named Query templates.

### images
Images used in `mf-ignition` documentation as well as in Ignition projects.

### Test
Currently unused Python scripts for a barest-of-bones MySQL router.

### Vagrant
Vagrant configuration for test of MySQL Group Replication. Instructions for
initializing the virtual development environment can be found in the
[Vagrant README][].

--------------------------------------------------------------------------------

## Setup

1.  Change to `Vagrant` directory and start the vagrant VM:
    ```
    cd Vagrant
    vagrant up
    ```

2.  Manually bootstrap the primary node \[`db-0`\]:
    ```
    vagrant ssh db-0
    sudo mysql -u root
    SET GLOBAL GROUP_REPLICATION_BOOTSTRAP_GROUP=ON;
    START GROUP_REPLICATION;
    SET GLOBAL GROUP_REPLICATION_BOOTSTRAP_GROUP=OFF;
    EXIT;
    exit
    ```

3.  Start group replication on secondary nodes \[`db-1`, `db-2`\]:
    ```
    # Repeat for each secondary node
    vagrant ssh <vm-hostname>
    sudo mysql -u root
    START GROUP_REPLICATION;
    EXIT;
    exit
    ```

4.  Start redundancy on the Ignition Gateways:

    Official Ignition redundancy setup instructions can be found and followed
    [here][Ignition Redundancy]. To get to the master gateway webpage as
    described in these instructions,  type the Master node IP followed by port
    8088 into your web browser as shown below:
    ```
    <master_ip_address>:8088
    ```

    Our configuration follows the default configuration, but disables the
    "Auto-Detect Network Interface" option and explicitly specifies the "Network
    Bind Interface" (the IP address of the server whose page you're on) within
    the "Network Settings" part of the redundancy configuration. In the past,
    Ignition has had trouble identifying the correct network interface to do
    redundancy things over.

    At this point, the blank Ignition/MySQL HA cluster is fully configured. To
    obtain a copy of the production Ignition project/MySQL DB, follow the
    instructions below.

5.  Get and upload a sample dataset:

    The actual production DB is small enough that it's reasonable to use the
    entire set as an example. Grab a DB dump by logging into an existing
    production server and running the following:
    ```
    sudo mysqldump --set-gtid-purged=OFF mf_ignition > dump.sql
    ```
    Copy this into the project folder (generally via `scp`), and enter one of
    the server nodes \[`db-0`, `db-1`, `db-2`\]. Upload the DB dump by running
    `sudo mysql mf_ignition < dump.sql`. This may take a while.

6.  Get and upload a Gateway Backup:

    Navigate to an existing production Ignition Gateway and download a
    [Gateway Backup][]. Once this is done, navigate to the Ignition Gateway at
    `db-0` and do a [Gateway Restore][]. Ensure that the "Restore Disabled"
    option is checked.

7.  Reconfigure databases and external resources

    Once the Gateway restore is complete, reconfigure the connected databases
    to point to `db-0`, `db-1`, and `db-2`, and re-enable all external
    resources.

    To reconfigure the databases, navigate to "Databases > Connections" and edit
    each one. To do this:
    -   go to "Connect URL" and switch out the `ignition.corp.markforged.com`
        host to the IP address of the database's server IP
    -   change the password to `not_a_secure_password`
    -   check off "Enabled" to enable communication with the database

    To re-enable external resources (MF_Production Project, database tag
    providers, and the OPC-UA) navigate to each their respective configuration
    pages as shown below. To re-enable:
    -   **MF_Production Project:** navigate to "System > Projects", click on
        "edit" for "MF_Production", and check off "Enabled" under Project
        Settings. Also ensure that "Connections > Default Tag Provider" is set
        to default.
    -   **Database Tag Providers:** navigate to "Tags > History", "edit" each
        Tag Provider, and check off "Enabled" under "Main".
    -   **OPC-UA Server:** navigate to "OPC Connections > Servers", "edit" the
        "Ignition OPC-UA Server", and check off "Enabled" under "Main".

    ![alt-text][re-enabling guide]

8.  Verify things are functioning properly

    First make sure that everything returns to normal on the Ignition server web
    interfaces. This entails checking that the servers show the correct IP
    addresses, activity statuses are "Active" for the Master and "Cold" for the
    backup, and that database and OPC connections are full.

    Conduct tests from within the MySQL shell of any database as you will. Group
    Replication nodes can be shown using
    `SELECT * FROM performance_schema.replication_group_members;`, while the
    current primary node can be found using `SHOW STATUS LIKE '%primary%';`.
    Detailed steps can be found in either the Vagrantfile or
    [SETUP_GROUP_REPLICATION.md][].

9.  Open the Ignition GUI!

    Open up the Ignition "Client Launcher", change the "Gateway URL" from the
    production server to the virtual one by selecting "CHANGE > Manually Input
    Gateway" and entering `<master_ip>:8088/main`, and hitting continue.
    Finally, you can hit launch to start the GUI!

[Gateway Backup]: https://docs.inductiveautomation.com/display/DOC80/Gateway+Backup+and+Restore#GatewayBackupandRestore-GatewayBackup
[Gateway Restore]: https://docs.inductiveautomation.com/display/DOC80/Gateway+Backup+and+Restore#GatewayBackupandRestore-GatewayRestore
[Ignition Redundancy]: https://docs.inductiveautomation.com/display/DOC80/Setting+Up+Redundancy
[re-enabling guide]: images/re-enabling_guide.png
[SETUP_GROUP_REPLICATION.md]: Config/SETUP_GROUP_REPLICATION.md
[Vagrant README]: Vagrant/README.md
