EXTRUSION_RUN_TABLE = "extrusion_runs"
PLASTIC_SPOOL_TABLE = "plastic_spools"
RAW_FIBER_TABLE = "raw_fiber_spools"
FIBER_CHANGE_TABLE = "fiber_lot_changes"
OVENS_TABLE = "ovens"
EVENT_LOG_TABLE = "event_log"
SPOOL_EVENT_LOG_TABLE = "spool_event_log"


def _db_insert(params_dict, table, tx=None):
    logger = system.util.getLogger(__name__)
    logger.info("_db_insert dict: {}".format(params_dict))
    query = "INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s" % (
        table,
        ", ".join(params_dict.keys()),
        ", ".join(["?" for key in params_dict]),
        ",".join(("{}=?".format(key) for key in params_dict)),
    )
    system.db.runPrepUpdate(query, params_dict.values() + params_dict.values(), tx=tx)


def _db_single_row_null_allow(querystring, tx=None):
    dataset_res = system.db.runQuery(querystring, tx=tx)
    res = None  # return None if result is empty or > 1 row
    if (
        dataset_res.getRowCount() == 1
    ):  # convert result to a PyDataSet if we receive a single row result
        res = system.dataset.toPyDataSet(dataset_res)[0]

    return res
