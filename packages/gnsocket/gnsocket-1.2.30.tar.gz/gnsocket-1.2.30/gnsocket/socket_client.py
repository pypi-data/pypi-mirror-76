import socket
from basic_queuetools.queue import read_queue_gen
from gnsocket.gn_socket import GNCSocket
# Standar lib
import asyncio
import functools
from multiprocessing import Manager, Queue, Lock

# contrib modules
import ujson as json

# Own module
from gnsocket.gn_socket import GNCSocket
from gnsocket.socket_base import GNCSocketBase

# module tasktools
from networktools.colorprint import gprint, bprint, rprint

from networktools.library import pattern_value, \
    fill_pattern, context_split, \
    gns_loads, gns_dumps
from networktools.library import my_random_string
from asyncio import shield, wait_for, wait

import ujson as json
from tasktools.taskloop import TaskLoop

tsleep = 2


class GNCSocketClient(GNCSocketBase):

    def __init__(self, queue_n2t, queue_t2n, *args, **kwargs):
        super().__init__(queue_n2t, queue_t2n, 'client', *args, **kwargs)
        self.set_socket_task(self.socket_task)
        self.name = kwargs.get('name', "test")
        self.idc = None

    def socket_task(self):
        # client socket
        loop = asyncio.get_event_loop()
        self.connected = False
        with GNCSocket(mode='client', timeout=self.timeout,
                       raise_timeout=self.raise_timeout,
                       log_path=self.log_path) as gs:
            try:
                gs.set_new_client(self.client_name)
                self.loop = loop
                gs.set_address(self.address)
                gs.set_loop(loop)

                async def client_cycle(*args, **kwargs):
                    if gs.new_client(self.client_name):
                        try:
                            gs.report("client_cycle", "Creating new client...")
                            idc = await gs.create_client()
                            self.new_client("client", self.name, idc)
                            self.idc = idc
                            self.queue_channel(idc)
                            self.stop_read[idc] = False
                            self.stop_write[idc] = False
                            gs.report("client_cycle", "idc->%s" % idc)
                            await gs.new_client_queue.put({
                                "idc": idc,
                            })
                            gs.relation[self.client_name] = idc
                            gs.off_new_client(self.client_name)
                            print("Post connection", gs.active_conn)
                            # send client info to socket server
                            client_info = {
                                "SOCKET_COMMAND": "NEW_CLIENT",
                                "value": idc,
                                "name": self.client_name,
                                "idc": idc
                            }
                            self.qn2t.put(client_info)
                            print(f"Sended {client_info}")
                            await asyncio.sleep(2)
                            #
                            return [False, idc, *args], kwargs
                        except asyncio.CancelledError as ce:
                            gs.report("client_cycle",
                                      "Tareas canceladas...", ce)
                            gs.logger.exception("Tareas canceladas %s" % ce)
                            if idc in gs.clients.keys():
                                gs.clients.remove(idc)
                            gs.on_client_name()
                            return [True, *args], {}
                        except asyncio.TimeoutError as te:
                            gs.report("client_cycle",
                                      "Error timeout...", te, gs.mode)
                            gs.logger.exception("Tiempo fuera en escritura %s, mode %s" % (
                                te, gs.mode))
                            if idc in gs.clients.keys():
                                gs.clients.remove(idc)
                            await asyncio.sleep(10)
                            gs.on_client_name()
                            return [True, *args], {}
                        except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                            gs.report("client_cycle",
                                      "Error conexion...", conn_error, gs.mode)
                            gs.logger.exception("Excepción por desconexión %s, mode %s" % (
                                conn_error, gs.mode))
                            await asyncio.sleep(10)
                            if idc in gs.clients.keys():
                                gs.clients.remove(idc)
                            gs.on_client_name()
                            return [True, *args], {}
                        except Exception as e:
                            gs.report("client_cycle",
                                      "Excepción no considerada", e)
                            gs.logger.exception(
                                "Excepción no considerada al intentar leer%s" % e)
                            gs.on_client_name()
                            await asyncio.sleep(5)
                            return [True, *args], {}
                    else:
                        await asyncio.sleep(2)
                        return args, kwargs

                async def socket_io():
                    idc = None
                    try:
                        # client manage control
                        create_client = True
                        args = [create_client]
                        task_client_cycle = TaskLoop(client_cycle,
                                                     args, **{
                                                         "name": "task_client_cycle"
                                                     })
                        # client heartbeat
                        args = [None]
                        task_heart_beat = TaskLoop(gs.heart_beat,
                                                   args,
                                                   {"client_name": self.client_name,
                                                    "sleep": 5},
                                                   **{"name": "task_heart_beat"})
                        # sock_read
                        args = [gs, idc]

                        task_sock_read = TaskLoop(
                            self.sock_read,
                            args,
                            {},
                            **{"name": "task_sock_read"}
                        )

                        args = [gs, idc]
                        # task write
                        task_sock_write = TaskLoop(
                            self.sock_write,
                            args,
                            {},
                            **{"name": "task_sock_write"}
                        )

                        task_from = TaskLoop(
                            self.from_socket, [], {}, **{"name": "from_socket"})
                        task_to = TaskLoop(
                            self.to_socket, [], {}, **{"name": "to_socket"})

                        # create taskloops
                        tasks = [
                            task_client_cycle,
                            task_heart_beat,
                            task_sock_read,
                            task_sock_write,
                            task_from,
                            task_to
                        ]
                        for task in tasks:
                            task.create()
                    except Exception as ex:
                        gs.abort(idc)
                        await gs.close(idc)
                        gs.logger.exception(
                            "Cancelacion de tareas en gnsocket, error %s" % ex)
                        task_sock_write.close()
                        task_sock_read.close()
                        return False, {}
            except Exception as ex:
                gs.logger.exception(
                    "Error con modulo cliente gnsocket %s" % ex)
                gs.report("socket_task", "Exception as %s" % ex)
                raise ex
            # run the tasks :)
            future1 = loop.create_task(socket_io())
            if not loop.is_running():
                loop.run_forever()


if __name__ == "__main__":
    address = (socket.gethostbyname(socket.gethostname()), 5500)
    client = GNCSocketClient(address=address)
    client.socket_task()
