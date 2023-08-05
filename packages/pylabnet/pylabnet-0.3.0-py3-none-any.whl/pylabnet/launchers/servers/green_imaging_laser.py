''' Configures a Staticline instance to use a NIDaqmx output'''

import socket

import pylabnet.hardware.ni_daqs.nidaqmx_card as nidaqmx
import pylabnet.hardware.staticline.staticline as staticline

from pylabnet.network.client_server.staticline import Service, Client

from pylabnet.network.core.generic_server import GenericServer

# Parameters
NI_DEVICE_NAME = 'cDAQ1Mod1'


def launch(**kwargs):
    """ Connects to a NI DAQ as staticline

    :param kwargs: (dict) containing relevant kwargs
        :logger: instance of LogClient for logging purposes
        :port: (int) port number for the Cnt Monitor server
    """

    staticline_logger = kwargs['logger']
    daq = nidaqmx.Driver(device_name=NI_DEVICE_NAME, logger=staticline_logger)

    test_staticline = staticline.Driver(
        name='Green Imaging Laser',
        logger=kwargs['logger'],
        hardware_module=daq,
        ao_output='ao2',
        down_voltage=0,
        up_voltage=3.3,
    )

    # Instantiate Server
    # Staticline server
    staticline_service = Service()
    staticline_service.assign_module(module=test_staticline)
    staticline_service.assign_logger(logger=staticline_logger)
    staticline_service_server = GenericServer(
        service=staticline_service,
        host=socket.gethostbyname(socket.gethostname()),
        port=kwargs['port']
    )

    staticline_service_server.start()
