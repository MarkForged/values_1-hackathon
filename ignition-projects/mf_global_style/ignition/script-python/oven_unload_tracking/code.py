import db_utils


def unload_oven(
    load_id, wip_spools_out, qc_spools_out, unload_time, unload_operator, unload_comment
):
    try:

        logger = system.util.getLogger(__name__)

        tx = system.db.beginTransaction(timeout=10000)

        # Query the existing oven_name
        (oven_name, total_time) = db_utils._db_single_row_null_allow(
            "SELECT oven_name, time_to_sec(timediff(unload_time, load_time))/3600 as hour_diff FROM ovens WHERE id = '{}'".format(
                load_id
            )
        )
        # Use the oven_name (location) and unload_time to create a universal event ID
        event_id = _create_universal_event(unload_time, oven_name, unload_operator, tx)

        # Create spool Events for each spool that stays WIP
        for spool_id in wip_spools_out:
            _create_spool_event(event_id, spool_id, 0, tx)
        # Create spool Events for each spool that moves to QC
        for spool_id in qc_spools_out:
            _create_spool_event(event_id, spool_id, 1, tx)

        # Update the ovens table and include event_id
        _update_ovens_table(
            load_id,
            event_id,
            len(qc_spools_out),
            unload_time,
            total_time,
            unload_operator,
            unload_comment,
            tx,
        )

        logger.debug("inserted event id: {}".format(event_id))

        # Handle commit/rollback and close of transaction
        system.db.commitTransaction(tx)
    except Exception:
        system.db.rollbackTransaction(tx)
        raise
    finally:
        system.db.closeTransaction(tx)


def _create_universal_event(event_time, location, operator, tx):
    """Creates a universal event for specific item event and process event log tab to link to


    @param event_time: date and time that the even happened (string of format "YYYY-MM-DD HH:MM:SS.sssss")
    @param location: location where the event happened (string maxlen 30)
    @param operator: employee or 'beaglebone'. The actor that created the event (string maxlen 45)
    @param tx: Ignition Jython transaction id

    @returns: the event id that was just added
    """
    params_dict = {"event_time": event_time, "location": location, "operator": operator}
    db_utils._db_insert(params_dict, db_utils.EVENT_LOG_TABLE, tx=tx)
    event_id = db_utils._db_single_row_null_allow("SELECT LAST_INSERT_ID()", tx=tx)[0]

    logger = system.util.getLogger(__name__)
    logger.debug("new universal event id: {}".format(event_id))

    return event_id


def _create_spool_event(event_id, spool_id, next_state, tx):
    prev_state_row = db_utils._db_single_row_null_allow(
        "SELECT next_state FROM spool_event_log WHERE spool_id = '{}' ORDER BY event_id DESC LIMIT 1".format(
            spool_id
        ),
        tx=tx,
    )
    if prev_state_row is None:
        prev_state_row = db_utils._db_single_row_null_allow(
            "SELECT status FROM extrusion_runs WHERE spool_id = '{}'".format(spool_id),
            tx=tx,
        )
    params_dict = {
        "event_id": event_id,
        "spool_id": spool_id,
        "prev_state": prev_state_row[0],
        "next_state": next_state,
    }
    db_utils._db_insert(params_dict, db_utils.SPOOL_EVENT_LOG_TABLE, tx=tx)
    extrusion_runs_params = {"spool_id": spool_id, "status": next_state}
    db_utils._db_insert(extrusion_runs_params, db_utils.EXTRUSION_RUN_TABLE, tx=tx)


def _update_ovens_table(
    id, event_id, qc_spools, unload_time, total_time, u_operator, unload_comment, tx
):
    params_dict = locals()
    del params_dict["tx"]
    db_utils._db_insert(params_dict, db_utils.OVENS_TABLE, tx=tx)
