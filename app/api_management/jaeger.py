from opentracing_instrumentation.client_hooks import install_all_patches
from jaeger_client import Config
from api_management.api_management import getConfig


def initializejaeger():

    jaegerdata = getConfig()
    print(jaegerdata)

    config = Config(config={'sampler': {'type': 'const', 'param': 1},
                            'logging': True,
                            'local_agent':
                                {'reporting_host': str(jaegerdata['jaeger']['host']), 'reporting_port': jaegerdata['jaeger']['port']}},
                    service_name=str(jaegerdata['jaeger']['service_name']))
    tracer = config.initialize_tracer()

    install_all_patches()

    return tracer
