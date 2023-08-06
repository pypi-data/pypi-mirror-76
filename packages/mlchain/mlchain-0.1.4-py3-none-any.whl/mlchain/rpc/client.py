from mlchain.base import logger
logger.warn("mlchain.rpc.client is deprecated and will be remove in the next version. Please use mlchain.client instead")
from mlchain.client import get_model, HttpClient, GrpcClient,Client