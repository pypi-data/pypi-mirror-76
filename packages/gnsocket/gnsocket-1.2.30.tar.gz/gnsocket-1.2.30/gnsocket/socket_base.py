import asyncio
import socket
from basic_queuetools.queue import read_queue_gen, read_async_queue
# contrib modules
import ujson as json

# Own module
from gnsocket.exceptions import clean_exception

# module tasktools
from networktools.colorprint import gprint, bprint, rprint


tsleep = 2


class GNCSocketBase:

    def __init__(self, queue_n2t,
                 queue_t2n,
                 mode,
                 callback_exception=clean_exception,
                 *args,
                 **kwargs):
        self.qn2t = queue_n2t
        self.qt2n = queue_t2n
        self.address = kwargs.get('address', ('localhost', 6666))
        self.log_path = kwargs.get('log_path', '~/gnsocket_log')
        self.mode = mode
        self.exception = callback_exception
        self.timeout = kwargs.get("timeout", 20)
        self.raise_timeout = kwargs.get("raise_timeout", False)
        self.client = None
        self.client_name = kwargs.get('client_name', "test")
        self.commands = {
        }
        self.stop_read = {}
        self.stop_write = {}
        self.queues = {}
        self.clients = {}

    def new_client(self, value, name, socket_id, **kwargs):
        if name not in self.clients:
            self.clients[name] = dict()
            self.clients[name].update({
                socket_id: value
            })
            gprint(f"Nuevos clientes ::: {self.clients}")
        else:
            self.clients[name].update({
                socket_id: value
            })
            # estable relacion entre id en server
            # e id cliente

    def queue_channel(self, idc):
        q_t2n = asyncio.Queue()
        q_n2t = asyncio.Queue()
        self.queues[idc] = {'t2n': q_t2n, 'n2t': q_n2t}

    def get_channel(self, idc):
        channel = self.queues.get(idc, {})
        return channel

    async def sock_write(self, gs, idc, *args, **kwargs):
        if not idc:
            idc_list = list(gs.clients.keys())
            if idc_list:
                idc = idc_list.pop()
        await asyncio.sleep(1)
        if idc in list(gs.clients.keys()):
            queue_n2t = self.get_channel(idc).get("n2t")
            if not self.stop_write[idc]:
                try:
                    async for msg in read_async_queue(queue_n2t, fn_name='sock_write'):
                        msg_send = json.dumps(msg)
                        idc_server = msg.get('idc_server')
                        try:
                            send_msg = gs.send_msg(msg_send, idc)
                            await asyncio.wait_for(send_msg, timeout=60)
                        except BrokenPipeError as be:
                            gs.report(
                                "sock_write",
                                "Close->Broken Pipe Error al cerrar %s bytes" % (be))
                            gs.logger.exception(
                                "Tiempo fuera en escritura %s, mode %s" % (
                                    be, gs.mode))
                            await asyncio.sleep(1)
                            continue
                        except socket.error as se:
                            gs.report(
                                "socke_write", "Close->Socket Error al leer %s bytes" % (se))
                            await asyncio.sleep(1)
                            continue
                        except asyncio.TimeoutError as te:
                            gs.report("sock write",
                                      "Timeout, tiempo fuera al enviar", te)
                            gs.logger.exception(
                                f"Tiempo fuera en escritura {te}, mode {gs.mode}")
                            await asyncio.sleep(1)
                            continue
                        except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                            gs.report("sock write", "Error de conexion",
                                      conn_error, gs.mode)
                            gs.logger.exception("Excepción por desconexión %s, mode %s" % (
                                conn_error, gs.mode))
                            await asyncio.sleep(1)
                            gs.set_status(False)
                            del gs.clients[idc]
                            continue
                        except Exception as ex:
                            gs.on_new_client(self.client_name)
                            gs.report("sock write", "Exepción", ex)
                            gs.logger.exception(
                                "Error con modulo cliente gnsocket coro write %s" % ex)
                            print(
                                "Error con modulo de escritura del socket IDC %s" % idc)
                            continue
                except asyncio.TimeoutError as te:
                    gs.report("sock write", "Timeout error B", te)
                    gs.logger.exception("HEARTBEAT: Tiempo fuera en escritura %s, mode %s" % (
                        te, gs.mode))
                    await asyncio.sleep(10)
                except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                    gs.report("sock write", "Error de conexion",
                              conn_error, gs.mode)
                    gs.logger.exception("HEARTBEAT: Excepción por desconexión %s, mode %s" % (
                        conn_error, gs.mode))
                    await asyncio.sleep(10)
                    gs.set_status(False)
                    del gs.clients[idc]
                except Exception as ex:
                    gs.report("sock write", "Exepción", ex)
                    gs.logger.exception(
                        "HEARTBEAT: Error con modulo cliente gnsocket coro write %s" % ex)
                    gs.report(
                        "sock_write",
                        f"Error con modulo de escritura del socket IDC {idc}")
            kwargs["stop"] = self.stop_write[idc]
        else:
            await asyncio.sleep(2)
        return [gs, idc, *args], kwargs
    # socket communication terminal to engine

    async def sock_read(self, gs, idc, *args, **kwargs):
        if not idc:
            idc_list = list(gs.clients.keys())
            if idc_list:
                idc = idc_list.pop()
        #queue_t2n = self.qt2n
        await asyncio.sleep(1)
        if idc in list(gs.clients.keys()):
            queue_t2n = self.get_channel(idc).get("t2n")
            try:
                recv_msg = gs.recv_msg(idc)
                datagram = await asyncio.wait_for(recv_msg, timeout=60)
                if datagram not in {'', "<END>", 'null', None}:
                    msg_dict = json.loads(datagram)
                    if 'SOCKET_COMMAND' in msg_dict:
                        msg_dict['socket_id'] = idc
                        self.check_msg(msg_dict)
                    else:
                        msg = {'dt': msg_dict, 'idc': idc}
                        await queue_t2n.put(msg)
            except BrokenPipeError as be:
                gs.report(
                    "sock_read",
                    f"Close->Broken Pipe Error al cerrar {be} bytes")
                gs.logger.exception("Tiempo fuera en escritura %s, mode %s" % (
                    be, gs.mode))
                await asyncio.sleep(1)
            except socket.error as se:
                gs.report("socke_read",
                          f"Close->Socket Error al leer {se} bytes")
                await asyncio.sleep(1)
            except asyncio.TimeoutError as te:
                gs.report("sock_read", "Timeout, waiting more than 60 secs", te)
                gs.logger.exception(
                    f"Tiempo fuera en lectur {te}, mode {gs.mode}")
                await asyncio.sleep(2)
            except (ConnectionResetError,
                    ConnectionAbortedError) as conn_error:
                gs.report("sock_read", "Error de conexion",
                          conn_error, gs.mode)
                gs.logger.exception("Excepción por desconexión %s, mode %s" % (
                    conn_error, gs.mode))
                await asyncio.sleep(2)
                gs.set_status(False)
                del gs.clients[idc]
                if self.exception:
                    self.exception(conn_error, gs, idc)
            except Exception as ex:
                gs.report("sock_read", "Exepción", ex)
                rprint(ex)
                gs.logger.exception(
                    f"Error con modulo cliente gnsocket coro read {ex}")
                gs.report("sock_read", f"Some error {ex} en sock_read")
        else:
            await asyncio.sleep(2)
            idc = self.client
        return [gs, idc, *args], kwargs

    async def from_socket(self, *args, **kwargs):
        for idc, channel in self.queues.items():
            # read queue multiplexer
            queue_t2n = channel.get('t2n')
            if not queue_t2n.empty():
                # block until process the list
                for i in range(queue_t2n.qsize()):
                    msg = await queue_t2n.get()
                    self.qt2n.put(msg)
        await asyncio.sleep(.1)
        return args, kwargs

    async def to_socket(self, *args, **kwargs):
        queue_n2t = self.qn2t
        if self.clients:
            # dicts->keys()->last value
            if not queue_n2t.empty():
                # block until process the list
                default = self.first_key()
                for i in range(queue_n2t.qsize()):
                    msg = queue_n2t.get()
                    idc = msg.get('idc', default)
                    if idc in self.queues.keys():
                        q_n2t = self.get_channel(idc).get('n2t')
                        await q_n2t.put(msg)
        await asyncio.sleep(.1)
        return args, kwargs

    def first_key(self):
        default = ""
        clientes = list(self.clients.values())
        if clientes:
            default = list(clientes.pop().keys())[-1]
        return default

    def check_msg(self, msg):
        command = msg.get('SOCKET_COMMAND', "print")
        callback = self.commands.get(command, print)
        callback(**msg)

    def set_socket_task(self, callback_socket_task):
        self.socket_task = callback_socket_task
