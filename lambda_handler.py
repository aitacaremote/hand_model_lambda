import logging

import boto3
import requests

import CoinTranslate
import hand_model.Pipeline
from components.Response import Response, Status
from hand_model.Components.RingFitting import RingFitting

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def pipeline_hand_model(measurement_id: int, scopes: list[str], coin: float, ring_fitting: str):
    logger.info("Hand model request received")
    # CREATES PIPELINE
    logger.debug("Creating pipeline")
    pipeline = hand_model.Pipeline.Pipeline(process_id=measurement_id, coin_size=CoinTranslate.calculate_coin(coin),
                                            scopes=set(scopes),
                                            fit=RingFitting.FITTED if ring_fitting == "fitted" else RingFitting.LOOSE)
    logger.debug("Creating response")
    response = Response(measurement_id=measurement_id, version=pipeline.version,
                        params={"coin": coin, "ring_fitting": ring_fitting})
    try:
        logger.debug("Connecting response")
        response.connect()
        logger.info("Running pipeline")
        results, err_count = pipeline.run()
    except ConnectionError:
        logger.critical("Failed to set the measurement status due a failure with the measurement service")
        raise RuntimeError
    except Exception as e:
        if not isinstance(e, RuntimeError):
            logger.error("Failed to run the pipeline due to a fatal error", exc_info=True)
        response.set_status(Status.ERROR)
        return response.connect()
    else:
        logger.info("Pipeline completed")
        response.set_status(Status.READY)
        response.results = results
        logger.debug("Sending results to measurement service")
        return response.connect()


def handler(event, context):
    try:
        result = pipeline_hand_model(measurement_id=event.get('measurement_id'), scopes=event.get('scopes'),
                                     coin=event.get('coin'), ring_fitting=event.get('ring_fitting'))
        response = {"status": "OK", "result": result}
    except Exception as e:
        logger.error(e)
        response = {"status": "ERROR"}
    return response
