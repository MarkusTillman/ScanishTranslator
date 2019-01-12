import logging

logging.basicConfig(filename="log.log", level=logging.DEBUG, filemode="w")

def logIncomingRequest(headers, body):
    logging.info("Received request: ")
    logging.info(str(headers) + "\n" + str(body))

def logOutgoingRequest(headers, body, url):
    logging.info("Sending request to " + str(url))
    logging.info(str(headers) + "\n" + str(body))

def logIncomingResponse(headers, body):
    logging.info("Received response: ")
    logging.info(str(headers) + "\n" + str(body))