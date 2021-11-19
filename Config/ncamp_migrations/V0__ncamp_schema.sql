/* NCAMP Printer Dashboard Schema Generation
 *
 * This is where the magic is.
 */

BEGIN;

/*******************************************************************************
 * TABLES
 ******************************************************************************/

/* `active printers` lists all printers actively displayed
 */
CREATE TABLE `active_printers` (
    `id`    VARCHAR(40),
    `name`  TEXT,
    PRIMARY KEY (`id`)
);

/* `printer_state_map` maps states reported from the Eiger API to a smaller
 * subset.
 */
CREATE TABLE `printer_state_map` (
    `eiger_state`   VARCHAR(60),
    `simple_state`  INT NOT NULL,
    PRIMARY KEY (`eiger_state`)
);

/* `printer_states` defines subset of states displayed in Ignition, along w/
 * metadata
 */
CREATE TABLE `printer_states` (
    `id`    INT,
    `name`  TEXT,
    `color` CHAR(9),    -- #RRGGBBAA color code
    `next`  INT,        -- ID of next state to display
    PRIMARY KEY (`id`)
);

INSERT INTO `printer_states` (`id`, `name`, `color`, `next`) VALUES
    (-1, 'ERROR', '#D3D3D3FF', NULL),
    (0, 'NEED PRINT', '#FFBF00FF', 1),
    (1, 'PRINTING','#238823FF', 2),
    (2, 'PRINT COMPLETE', '#FFBF00FF', 1),
    (3, 'NEEDS ATTN', '#D32222FF', 1);

INSERT INTO `printer_state_map` (`eiger_state`, `simple_state`) VALUES
    ('Disabled', 3),
    ('Ready', 0),
    ('Printing', 1),
    ('Print Finished', 2),
    ('Canceling', 3),
    ('Print Bed Needs Clearing', 2),
    ('Configuration in Progress', 3),
    ('Pausing', 3),
    ('Print Paused', 3),
    ('Resuming Print', 1),
    ('Low on Material', 3),
    ('Out of Material', 3),
    ('Purge Strip Removal Needed', 3),
    ('Update in Progress', 3),
    ('Dislocation Error', 3),
    ('Bed Needs Leveling', 3),
    ('Incompatible Print File', 3),
    ('Fiber Jam', 3),
    ('System Cooldown', 3),
    ('Setup Workflow', 3),
    ('System Precheck', 3),
    ('Material Jam', 3),
    ('Vacuum Not Engaged', 3),
    ('Offline', 3),
    ('Running Job', 3),
    ('Finished', 3),
    ('Busy', 3),
    ('Updating', 3),
    ('Running Utility', 3),
    ('Canceled Job', 3),
    ('Downloading', 1),
    ('Error', -1);


/*******************************************************************************
 * USERS
 ******************************************************************************/

/* `ignition` is used by the Ignition Gateway and Clients
 *
 * This account currently touches all there is to be touched in the `mf_igniton`
 * schema.
 */
CREATE USER 'ncamp_ignition'@'%' IDENTIFIED BY 'not_a_secure_password';
GRANT ALL ON * TO 'ncamp_ignition'@'%';

FLUSH PRIVILEGES;

COMMIT;
