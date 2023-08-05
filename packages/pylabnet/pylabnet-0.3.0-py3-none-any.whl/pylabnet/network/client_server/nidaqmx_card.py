import pickle

from pylabnet.network.core.service_base import ServiceBase
from pylabnet.network.core.client_base import ClientBase


class Service(ServiceBase):

    def exposed_set_ao_voltage(self, ao_channel, voltage_pickle):
        voltages = pickle.loads(voltage_pickle)
        return self._module.set_ao_voltage(
            ao_channel=ao_channel,
            voltages=voltages
        )

    def exposed_create_timed_counter(
        self, counter_channel, physical_channel, duration=0.1, name=None
    ):
        return self._module.create_timed_counter(
            counter_channel=counter_channel,
            physical_channel=physical_channel,
            duration=duration,
            name=name
        )

    def exposed_start_timed_counter(self, name):
        return self._module.start_timed_counter(name)

    def exposed_close_timed_counter(self, name):
        return self._module.close_timed_counter(name)

    def exposed_get_count(self, name):
        return self._module.get_count(name)


class Client(ClientBase):

    def set_ao_voltage(self, ao_channel, voltages):
        voltage_pickle = pickle.dumps(voltages)
        return self._service.exposed_set_ao_voltage(
            ao_channel=ao_channel,
            voltage_pickle=voltage_pickle
        )

    def create_timed_counter(
        self, counter_channel, physical_channel, duration=0.1, name=None
    ):
        return self._service.exposed_create_timed_counter(
            counter_channel=counter_channel,
            physical_channel=physical_channel,
            duration=duration,
            name=name
        )

    def start_timed_counter(self, name):
        return self._service.exposed_start_timed_counter(name)

    def close_timed_counter(self, name):
        return self._service.exposed_close_timed_counter(name)

    def get_count(self, name):
        return self._service.exposed_get_count(name)
