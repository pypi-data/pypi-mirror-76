from mlchain.base import logger
logger.warn("mlchain.rpc.server is deprecated and will be remove in the next version. Please use mlchain.server instead")
try:
    from mlchain.server.flask_server import FlaskServer
except:
    import warnings
    warnings.warn("Can't import FlaskServer")

try:
    from mlchain.server.quart_server import QuartServer
except:
    import warnings
    warnings.warn("Can't import QuartServer")

try:
    from mlchain.server.grpc_server import GrpcServer
except:
    import warnings
    warnings.warn("Can't import GrpcServer")