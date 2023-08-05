# -*- coding: utf-8 -*-

# Echo server program
import os
import socket
import asyncio
import errno
import math
import re
import ssl
from pathlib import Path
from basic_logtools.filelog import LogFile
from asyncio import shield, wait_for, Task
# These values are constant
try:
    from conf.socket_conf import AF_TYPE, SOCK_TYPE
    from conf.socket_conf import HEADER
    from conf.socket_conf import ENDER
    from conf.socket_conf import sock
    from conf.socket_conf import gnc_path
    from conf.socket_conf import t_out
    from conf.socket_conf import buffsize
    from conf.socket_conf import uin
    from conf.socket_conf import char_code
    from conf.socket_conf import n_listen
    from conf.socket_conf import address

except Exception:
    from .conf.socket_conf import AF_TYPE, SOCK_TYPE
    from .conf.socket_conf import HEADER
    from .conf.socket_conf import ENDER
    from .conf.socket_conf import sock
    from .conf.socket_conf import gnc_path
    from .conf.socket_conf import t_out
    from .conf.socket_conf import buffsize
    from .conf.socket_conf import uin
    from .conf.socket_conf import char_code
    from .conf.socket_conf import n_listen
    from .conf.socket_conf import address

from networktools.library import (pattern_value,
                                  fill_pattern,
                                  context_split,
                                  gns_loads,
                                  gns_dumps,
                                  my_random_string,
                                  complete_nro,
                                  hextring,
                                  hextring2int)

from networktools.colorprint import gprint, bprint, rprint
from networktools.time import now, timestamp
from networktools.path import home_path

# Asyncio guide:
# http://www.snarky.ca/how-the-heck-does-async-await-work-in-python-3-5

# More ref about socket:
# http://stackoverflow.com/questions/27014955/socket-connect-vs-bind

# example:

# Best example: https://gist.github.com/jamilatta/7603968

# from scheduler import ReadWait, WriteWait

import uuid

import queue
import chardet
from datetime import datetime, timedelta


class GNCSocket:
    """
    This class allows yo to enable a socket to communicate among different process or terminals.

    Define a protocol that take a string of bytes and slice in an amount of parts related to the
    *buffsize* parameter.

    You can select the *mode* to use this class: like a server to *listen* connections or like a client to *connect* to some source.

    Also, if you need security, set the ssl parameter to True.

    The *backlog* parameter aludes to the queued connections to the server.


    Socket class for GNC
    Create or connect to an UNIX/TCP socket
    Methods:
    * connect
    * send_msg
    * recv_msg
    * server
    * client
    """

    def __init__(self, mode='server', address=address, **kwargs):
        self.mode = mode
        self.bs = kwargs.get("buffsize", buffsize)
        self.gnc_path = kwargs.get("gnc_path", gnc_path)
        # default timeout
        self.timeout = kwargs.get('timeout', t_out)
        self.raise_timeout = kwargs.get("raise_timeout", False)
        self.module = kwargs.get('module', 'test')
        self.ssl = kwargs.get('ssl', False)
        # IF SSL ACTIVE
        if self.ssl:
            self.set_ssl(**kwargs)
        else:
            self.context = None
        ####
        self.address = kwargs.get('address', address)
        self.AF_TYPE = kwargs.get('AF_TYPE', AF_TYPE)
        # self.set_logger()
        if mode == 'server':
            self.set_server(self.AF_TYPE, self.address)
            self.server = None
        if mode == 'client':
            self.set_client(self.AF_TYPE, self.address)
        self.status = False
        # BIND: connect a path with socket
        # list of connections, address.
        self.backlog = kwargs.get("backlog", n_listen)
        # MSG Format
        # Defined:
        # LEN_HEAD MSG LCHAR(hex) LEN MSG END
        # Send format
        self.msg_struct = b"IDX hex(PAGE)/hex(TOT_PAGES) MSG hex(LEN) MSG END"
        self.msg_template = "{idx} {page}/{tot_pages} MSG {length} MSG END"
        self.msg_spaces = [x.start()
                           for x in re.finditer(b' ', self.msg_struct)]
        # IDX hex(PAGE)/hex(TOT_PAGES) MSG hex(LEN) MSG END
        # How to generate:
        # msg -> bytes
        # len(msg_bytes)
        # # envios
        # self.msg_limit = msg_limit
        # self.msg_limit_hex = str(hex(self.msg_limit)).split('x')[1]
        # self.nchar = len(self.msg_limit_hex)
        # Limit_msg = 512 (default), n=len(str(512))
        # To hex: 0x200
        # Split x
        # Get value and complete => LCHAR (en hex)
        self.header = kwargs.get("header", HEADER)
        self.ender = kwargs.get("ender", ENDER)
        # number of chars for id
        self.uin = kwargs.get("uin", uin)
        self.idx = []
        self.conns = []
        self.addrs = []
        self.msg_r = ''
        # asyncio coroutines
        self.alert = ""
        self.loop = ''
        self.mq = {}
        # message queues
        self.clients = {}
        self.idc = []
        self.server = object
        # a fn to print or show on some other screen
        self.report = kwargs.get("report", print)
        #
        # new client queue: if a new client is created, then give
        # the idc value to heart_beat assigned to this client
        self.new_client_queue = asyncio.Queue()
        #
        log_path = home_path(kwargs.get('log_path', '~/socket_log'))
        log_level = kwargs.get('log_level', 'INFO')
        self.logger = LogFile(self.class_name,
                              self.mode,
                              "_".join(map(str, self.address)),
                              path=log_path,
                              base_level=log_level)

        self.queue_socket_status = None
        self.active_conn = {}
        self.relation = {}
        self.closing = {}
        self.reading = {}
        self.queue_cancel = queue.Queue()
        self.busy_read = False

    def off_new_client(self, key):
        if key in self.active_conn.keys():
            self.active_conn[key] = False

    def on_new_client(self, key):
        if key in self.active_conn.keys():
            self.active_conn[key] = True

    def drop_conn(self, key):
        if key in self.active_conn:
            del self.active_conn[key]

    def new_client(self, key):
        return self.active_conn.get(key)

    def set_new_client(self, key):
        self.active_conn[key] = True

    @property
    def class_name(self):
        return self.__class__.__name__

    def set_queue_socket_status(self, queue):
        self.queue_socket_status = queue

    def set_ssl(self, **kwargs):
        purpose_key = kwargs.get('ssl_protocol', 'tls')
        self.protocols = {
            'tls': ssl.PROTOCOL_SSLv23,
        }
        self.protocol = self.protocols.get(purpose_key, ssl.PROTOCOL_SSLv23)
        self.set_certs = kwargs.get('set_certificates',
                                    {'cafile': None,
                                     'capath': None,
                                     'cadata': None,
                                     'crtkey': None})
        data_ssl = {}
        data_ssl.update(self.set_certs)
        self.ssl_context(self.protocol, data_ssl)

    def ssl_context(self, protocol, data_ssl):
        self.context = ssl.SSLContext(protocol)
        crt = data_ssl.get('cafile')
        key = data_ssl.get('crtkey')
        if self.mode == 'server':
            self.context.load_cert_chain(crt, key)
        elif self.mode == 'client':
            path = data_ssl.get('cadata')
            data = data_ssl.get('capath')
            self.context.load_verify_locations(crt, path, data)
        print("SSL Settings end")

    def send_msg_sock_status(self, value):
        msg = {'command': 'socket_bar',
               'status': value}
        if self.queue_socket_status:
            self.queue_socket_status.put(msg)
            self.queue_socket_status.join()

    def set_server(self, AF_TYPE, address):
        if AF_TYPE == socket.AF_UNIX:
            self.address = self.gnc_path
            if os.path.exists(self.gnc_path):
                os.remove(self.gnc_path)
        elif AF_TYPE == socket.AF_INET:
            self.address = address
        # self.logger.info("Se crea un socket server")

    def set_client(self, AF_TYPE, address):
        if AF_TYPE == socket.AF_UNIX:
            self.address = self.gnc_path
        elif AF_TYPE == socket.AF_INET:
            self.address = address
        # self.logger.info("Se crea un socket client")

    def set_status(self, value):
        if value in [True, False]:
            self.status = value
        else:
            print("Status don't change")
        # self.logger.info("Se crea modifica status a %s" %value)

    def switch_status(self):
        self.status = not self.status
        # self.logger.info("Se crea modifica status a %s" %self.status)

    def get_status(self):
        return self.status

    def set_loop(self, loop):
        print(format(loop))
        self.loop = loop

    def get_writer(self, idc):
        return self.clients[idc]['writer']

    def get_reader(self, idc):
        return self.clients[idc]['reader']

    def generate_msg(self, msg: str):
        # self.msg_struct = b"IDX hex(PAGE)/hex(TOT_PAGES) MSG hex(LEN) MSG END"
        # self.msg_tempalte = b"{header} {page}/{tot_pages} MSG {length} MSG END"
        b_msg = msg.encode(char_code)
        T_LEN = len(b_msg)
        # Cantidad de caracteres en hexadecimal
        hex_T_LEN = hextring(T_LEN)
        # Se obtiene el largo de caracteres como
        # cota superior de largo de mensaje
        # A utilizar en paginacion
        # largo del valor
        # n_char es lo mismo
        new_n = len(hex_T_LEN)
        self.n_char = new_n
        # obtener el largo base del mensaje
        self.base_len = len(self.header) + len(self.ender) + \
            len(self.msg_spaces) + self.uin + 3 * self.n_char + 1
        # n_char is the amount of chars for numbers
        # tha last  +1 is for the space after IDX
        # Largo de pedazo de mensaje a enviar por partes
        self.len_msg = self.bs - self.base_len

        assert self.len_msg >= 1, "Debes definir un buffsize de mayor tamaño"
        assert new_n + 1 < self.len_msg, "No es posible enviar mensaje"

        # Cantidad maxima de mensajes a enviar
        n_msgs = math.ceil(T_LEN / self.len_msg)
        # transformar a hex y sacar string
        hex_n_msgs = hextring(n_msgs)
        # Cantidad de paginas
        self.N_n_msgs = len(str(hex_n_msgs))
        # hex_nmsgs = str(hex(n_msgs)).split('x')[1]
        ender = self.ender.encode(char_code)
        # Se construye: hex(PAGE)/hex(TOT_PAGES) MSG hex(LEN) MSG END
        NON = "".encode(char_code)
        head_template = "{header} {page}/{tot_pages} {length} "
        msg_ender = " END"
        if n_msgs > 1:
            for i in range(n_msgs):
                # Construir header:
                # Conocer parte de msg a enviar
                # Conocer largo de msg_i
                # Cantidad carácteres largo
                step = i * self.len_msg
                this_page = hextring(i + 1)
                msg_i = b_msg[step:step + self.len_msg]
                msg_l = len(msg_i)
                # +2 erased because quoted don't go
                msg_len = msg_l + len(ender)
                # print("MSG to send -> Encoded by" , the_encoding)
                componentes = {
                    'header': self.header,
                    'page': complete_nro(this_page, n=new_n),
                    'tot_pages': complete_nro(hex_n_msgs, n=new_n),
                    'length': complete_nro(hextring(msg_len), n=new_n)
                }
                msg_header = head_template.format(**componentes)
                this_msg = NON.join([msg_header.encode(char_code),
                                     msg_i,
                                     msg_ender.encode(char_code)])
                #bprint("Generated msg Encoded by")
                # rprint(this_msg)
                yield this_msg

        elif n_msgs == 1:
            this_page = hextring(1)
            msg_len = (T_LEN + len(ender))
            hex_msg_len = complete_nro(hextring(msg_len), n=new_n)
            componentes = {
                'header': self.header,
                'page': complete_nro(this_page, n=new_n),
                'tot_pages': complete_nro(hextring(1), n=new_n),
                'length': complete_nro(hextring(msg_len), n=new_n)
            }
            msg_header = head_template.format(**componentes)
            this_msg = NON.join([msg_header.encode(char_code),
                                 b_msg,
                                 msg_ender.encode(char_code)])
            #print("Generated msg Encoded by" , the_encoding)
            yield this_msg

    def gen_idx(self):
        IDX = my_random_string(self.uin)
        t = True
        while t:
            if IDX not in self.idx:
                self.idx.append(IDX)
                t = False
            else:
                IDX = my_random_string(self.uin)
        return IDX

    async def send_msg(self, msg, id_client):
        writer = self.clients.get(id_client).get('writer')
        # tot = self.N_n_msgs
        try:
            if writer.transport.is_closing():
                # self.logger.error("La conexión se cerró %s" % self.status)
                raise Exception("Conexión perdida")
            # assert tot == len(msg), "Hay un cruce de mensajes"
            pre = datetime.now()
            await shield(self.send_text(msg, writer))
            delta = datetime.now()-pre
            await shield(self.send_text('<END>', writer))
        except asyncio.CancelledError as ex:
            bprint("Cancelled error en send_msg")
            self.logger.exception(
                "Hubo una excepción, error de cancelación con modulo asyncio %s" % self.status)
            raise ex
        except (ConnectionResetError, ConnectionAbortedError) as conn_error:
            rprint("Error de conexion")
            self.logger.exception("Excepción por desconexión %s, mode %s" % (
                conn_error, self.mode))
            await asyncio.sleep(10)
            raise conn_error
        except socket.error as ex:
            bprint("Socket error en send msg")
            self.logger.exception(
                "Hubo una excepción, error en socket %s" % self.status)
            await asyncio.sleep(10)
            raise ex
        except Exception as ex:
            bprint("Excpecion desconocida send_msg")
            self.set_status(False)
            await asyncio.sleep(10)
            self.logger.exception("Hubo una excepción %s" % self.status)
            raise ex
        except asyncio.TimeoutError as te:
            bprint("Send-msg timeouterror")
            self.logger.exception(
                "Hubo una excepción, error de timeout con modulo asyncio %s" % te)
            raise te

    async def send_text(self, msg, writer):
        IDX = self.gen_idx().encode(char_code)
        for b_msg in self.generate_msg(msg):
            # print(b_msg)
            # Here the splited messages
            # First value is header length
            # Catch them
            # 1+1+self.uin
            # Find first space to get index from header len value
            to_send = b"".join([IDX, b" ", b_msg])
            # print("Contexted:::>",q)
            # yield WriteWait(conn)
            if writer.get_extra_info('peername'):
                writer.write(to_send)
                # Transport.write(data)
                await writer.drain()
            else:
                writer.write_eof()
                await writer.close()

    def get_extra_info(self, idc):
        writer = self.clients.get(idc).get('writer')
        return writer.get_extra_info('peername')

    def send_eof(self, id_client):
        writer = self.clients.get(id_client).get('writer')
        writer.write_eof()

    def abort(self, id_client):
        writer = self.clients.get(id_client).get('writer')
        writer.abort()

    def at_eof(self, id_client):
        reader = self.clients.get(id_client).get('reader')
        return reader.at_eof()

    def feed_eof(self, id_client):
        reader = self.clients.get(id_client).get('reader')
        reader.feed_eof()

    async def heart_beat(self, idc, *args, **kwargs):
        sleep = kwargs.get('sleep', 2)
        await asyncio.sleep(sleep)
        client_name = kwargs.get('client_name')
        tnow = now()
        if client_name:
            idc = self.relation.get(client_name)
        reader = self.clients.get(idc, {}).get('reader')
        writer = self.clients.get(idc, {}).get('writer')
        if idc in self.clients.keys() and reader and writer:
            await asyncio.sleep(.5)
            closing = writer.is_closing()
            extra_info = writer.get_extra_info('peername')
            if not closing and extra_info:
                kwargs.update({"result": True, "msg": "idc exists ok"})
                return [idc, *args], kwargs
            else:
                msg_error = "Closing %s, extra_info %s" % (
                    closing, extra_info)
                self.report("heartbeat", "msgerror "+msg_error)
                self.logger.error(msg_error)
                self.logger.error("no heart_beat, at %s" % tnow)
                print("IDC To close", idc)
                kwargs['result'] = False
                try:
                    await self.close(idc)
                    self.on_new_client(client_name)
                    print("Conexiones activas", self.active_conn)
                except BrokenPipeError as be:
                    self.report(
                        "heart_beat", "Close->Broken Pipe Error al cerrar %s bytes" % (be))
                    self.logger.exception(
                        f"Socket error {be}, mode {self.mode}")
                    await asyncio.sleep(1)
                    self.on_new_client(client_name)
                    await asyncio.sleep(2)
                except socket.error as e:
                    self.report(
                        "heart_beat", "Socket error, <%s>, client" % (e, client_name))
                    self.logger.exception(
                        "Socket error %s, mode %s" % (e, self.mode))
                    await asyncio.sleep(1)
                    self.on_new_client(client_name)
                    await asyncio.sleep(2)
                except asyncio.TimeoutError as te:
                    self.logger.exception(
                        "Tiempo fuera en intento de cerrar conexión %s, mode %s" % (te, self.mode))
                    self.on_new_client(client_name)
                    await asyncio.sleep(2)
                except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                    self.logger.exception(
                        "Excepción por desconexión %s, mode %s" % (conn_error, self.mode))
                    self.on_new_client(client_name)
                    await asyncio.sleep(2)
                except Exception as e:
                    self.report(
                        "heart_beat", "Excepción no considerada, <%s>" % e)
                    self.logger.exception(
                        "Excepción no considerada %s, mode %s" % (e, self.mode))
                    await asyncio.sleep(1)
                    self.on_new_client(client_name)
                    await asyncio.sleep(2)
                self.logger.exception(
                    "Cerrando correctamente la conexión, por no heartbeat")
                self.status = False
                kwargs.update({"msg": "idc exists ok"})
                return [idc, *args], kwargs
        else:
            self.logger.error(
                "no heart_beat, idc %s not client,  mode %s" % (idc, self.mode))
            return [idc, *args], kwargs

    async def readbytes(self, reader, n, idc, origin="none"):
        future = reader.readexactly(n)
        try:
            result = await future
            return result
        except BrokenPipeError as be:
            self.report(
                "readbytes", "Close->Broken Pipe Error al cerrar %s bytes" % (be))
            await asyncio.sleep(5)
            return b''
        except socket.error as se:
            self.report(
                "readbytes", "Close->Socket Error al leer %s bytes" % (se))
            await asyncio.sleep(5)
            return b''
        except asyncio.TimeoutError as te:
            self.report("readbytes", "Error Timeout al leer %d bytes en %s, origen: %s" % (
                n, self.mode, origin))
            self.logger.exception("Mode %s, Tiempo fuera al leer en readbytes, %s, origen %s" % (self.mode, te,
                                                                                                 origin))
            await asyncio.sleep(5)
            return b''
        except asyncio.IncompleteReadError as ir:
            self.report("readbytes", "Incomplete read, mode %s" %
                        self.mode, reader, n)
            self.logger.exception(
                "Mode  %s, Tiempo fuera al no poder leer en readbytes %s bytes, %s" % (n, self.mode, ir))
            await asyncio.sleep(5)
            return b''
        except (ConnectionResetError, ConnectionAbortedError) as conn_error:
            self.logger.exception(
                "Excepción por desconexión al intentar leer %s" % conn_error)
            await asyncio.sleep(5)
            return b''
        except Exception as e:
            print(self.clients.keys())
            self.report("readbytes", "Excepción no considerada",
                        e, "client", idc, "origin", origin)
            self.logger.exception(
                "Excepción no considerada al intentar leer %s, %s" % (e, origin))
            await asyncio.sleep(5)
            rprint("cancelando llamada")
            return "CANCEL"

    async def recv_msg(self, id_client):
        if id_client in self.clients:
            reader = self.clients[id_client]['reader']
            writer = self.clients[id_client]['writer']
            # heartbeat = await self.heart_beat(id_client)
            # addr = self.addr
            bs_0 = 1
            count = 0
            b_header = b''
            idx_recv = ''
            t = True
            msg_tot = b''
            mlist = []
            n_msgs_idx = 0
            try:
                # moment 1 -> get hueader
                if writer.transport.is_closing():
                    # self.logger.error("La conexión se cerró %s" % writer)
                    raise Exception("Conexión perdida")
                idx_recv = ''
                page = [0, 0]
                while t:
                    while count < 4:
                        char_recv = b''
                        if not reader.at_eof():
                            # moment 2 -> get content message, check if there are more
                            try:
                                task_rb = self.readbytes(reader,
                                                         bs_0,
                                                         id_client,
                                                         origin="recv_msg_header")
                                char_recv = await task_rb
                                if char_recv == 'CANCEL':
                                    bprint(
                                        "Cancelando lectura de socket,reding header...")
                                    return ""
                                elif char_recv:
                                    b_header += char_recv
                            except asyncio.TimeoutError as te:
                                self.logger.exception("Tiempo fuera en intento de cerrar conexión %s, mode %s" % (
                                    te, self.mode))
                                await asyncio.sleep(10)
                                continue
                            except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                                self.logger.exception("Excepción por desconexión %s, mode %s" % (
                                    conn_error, self.mode))
                                await asyncio.sleep(10)
                                continue
                            except Exception as ex:
                                self.report(
                                    "recv_msg", "Error al leer data -> %s" % ex, char_recv)
                                continue
                        else:
                            # buffer is empty
                            await asyncio.sleep(1)
                            return "{}"
                        # cuando ocurre un espacio, sumar count
                        # de otra manera continuar iteración
                        if char_recv == b" ":
                            count += 1
                    header = b_header.decode(char_code)
                    b_header = b''
                    spaces = [x.start() for x in re.finditer(' ', header)]
                    sp_1 = spaces[0]
                    sp_2 = spaces[1]
                    sp_3 = spaces[2]
                    # obtener número de página
                    s_page = header[sp_2 + 1:sp_3].split("/")
                    a = page[0]
                    b = page[1]
                    page = list(map(hextring2int, s_page))
                    sp_4 = spaces[3]
                    check_header = header[sp_1 + 1:sp_2]
                    assert self.header == header[sp_1 + 1:
                                                 sp_2], "No es un encabezado correcto"
                    this_idx_recv = header[:sp_1]
                    if idx_recv == '':
                        idx_recv = this_idx_recv
                        n_msgs_idx = 1
                    else:
                        n_msgs_idx += 1
                    assert n_msgs_idx == page[
                        0], "Error en mensaje, no coincide #idx con pagina " + str(
                            page[0])
                    lmsg = header[sp_3 + 1:sp_4]
                    bs_1 = hextring2int(lmsg)+1
                    b_MSG = b''
                    n = 0
                    while n < bs_1:
                        bm = None
                        # moment 2 -> get content message, check if there are more
                        try:
                            bm = await self.readbytes(
                                reader, 1, id_client, origin="recv_msg_body")
                            if bm == 'CANCEL':
                                return ""
                        except asyncio.TimeoutError as te:
                            self.logger.exception("Tiempo fuera en intento de cerrar conexión %s, mode %s" % (
                                te, self.mode))
                            await asyncio.sleep(10)
                            continue
                        except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                            self.logger.exception("Excepción por desconexión %s, mode %s" % (
                                conn_error, self.mode))
                            await asyncio.sleep(10)
                            continue
                        except Exception as ex:
                            self.logger.exception(
                                "Error al leer datos %s, con %s" % (ex, b_MSG))
                            print("Error en conexión excepction:<%s>" % ex)
                            print("Mensaje....", bm)
                            continue
                        if bm:
                            b_MSG += bm
                            n += 1
                    l_ender = len(self.ender.encode(char_code))
                    nlast = b_MSG.rfind(b" ")
                    pre_msg = b_MSG[:nlast]
                    count = 0
                    if pre_msg == b"<END>" or page[0] == page[1]:
                        t = False
                        mlist.append(pre_msg)
                        n_msgs_idx = 0
                        break
                    else:
                        mlist.append(pre_msg)
            except asyncio.CancelledError as ex:
                self.logger.exception("Error de conexión cancelada  %s" % ex)
                self.report(
                    "recv_msg", "Asyncio cancelación de conexión <%s>" % ex)
                self.queue_cancel.put(id_client)
            except socket.error as ex:
                self.logger.exception(f"Error de conexión de socket  {ex}")
                self.report("recv_msg", "Error de socket")
                await asyncio.sleep(3)
                self.report(
                    "recv_msg", "Falla en la conexión al recibir mensaje, %s" %
                    ex)
                self.queue_cancel.put(id_client)
            except Exception as ex:
                await asyncio.sleep(3)
                self.logger.exception("Error de conexión  %s" % ex)
                self.report(
                    "recv_msg", "Falla en la conexión al recibir mensaje, %s" % ex)
                self.report("recv_msg", "Lista msgs", mlist)
            #print("Procesando final")
            msg_tot = b"".join(mlist)
            MSG_TOT = msg_tot.decode(char_code)
            MT = MSG_TOT.strip()
            MT = MSG_TOT.rstrip()
            self.msg_r = MSG_TOT
            return MSG_TOT
        else:
            return "{}"

    def get_path(self):
        return self.gnc_path

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def set_path(self, new_gnc_path):
        if os.path.exists(new_gnc_path):
            os.remove(new_gnc_path)
        self.gnc_path = new_gnc_path

    # callback for create server:

    def set_idc(self):
        """
        Defines a new id for relation process-collect_task, check if exists
        """
        uin = 4
        idc = my_random_string(uin)
        while True:
            if idc not in self.idc:
                self.idc.append(idc)
                break
            else:
                idc = my_random_string(uin)
        return idc

    async def set_reader_writer(self, reader, writer):
        idc = self.set_idc()
        # self.log_info_client(writer)
        new_client = {
            'reader': reader,
            'writer': writer
        }
        self.clients[idc] = new_client
        return idc

    def log_info_client(self, writer):
        names = ['peername', 'socket', 'sockname']
        for name in names:
            info = writer.get_extra_info(name)
            # self.loggger.info("La info correspondiente a %s es %s" %(name, info))

    def off_blocking(self):
        if self.mode == 'server':
            [sock.setblocking(False) for sock in self.server.sockets]
        elif self.mode == 'client':
            pass

    def on_blocking(self):
        if self.mode == 'server':
            [sock.setblocking(True) for sock in self.server.sockets]
        elif self.mode == 'client':
            pass

    def settimeout(self, timeout=5):
        [sock.settimeout(timeout) for sock in self.server.sockets]

    async def connect(self):
        """
        Connect client to socket
        """
        while not self.status:
            try:
                result = await self.loop.sock_connect(
                    self.sock, self.address)
                self.alert = "Conectado a socket-base"
                self.status = True
                self.report("async connect", "Resultado de conectar socket")
                print(result)
                # self.logger.info("Conexión a %s realizada" % self.address)
                break
            except socket.timeout as timeout:
                # self.on_blocking()
                # self.logger.error(
                #     "Error en conexión con %s, error: %s" % (self.address, timeout))
                self.report("async connect", "Error de socket a GSOF \
                en conexión %s, %s" % (self.address, timeout))
                self.status = False
                await asyncio.sleep(.5)
                await self.connect()  # go to begin -|^
            except socket.error as e:
                self.status = False
                # self.on_blocking()
                if e.errno == errno.ECONNREFUSED:
                    pass
                    # self.logger.error(e)
                else:
                    pass
                    # self.logger.error(e)

    def clean_socket(self, host, port):
        comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.report("clean socket", "ex socket->ComSocket:::", comSocket)
        self.report("clean socket", socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.report("clean socket", socket.SOL_SOCKET, socket.SO_REUSEPORT)
        self.report("clean socket", "Cleaning address", (host, port))
        comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # comSocket.shutdown(socket.SHUT_RDWR)

    async def close(self, idc):
        self.closing[idc] = True
        self.report("close", "La conexión se cerró en cliente %s" % idc)
        self.logger.error("La conexión se cerró en cliente %s" % idc)
        self.status = False
        print(idc, self.clients)
        if idc in self.clients:
            reader = self.clients.get(idc, {}).get('reader')
            writer = self.clients.get(idc, {}).get('writer')
            try:
                if writer:
                    if writer.can_write_eof():
                        print("Closing idc client,,,,")
                        writer.close()
                del self.clients[idc]
                del self.closing[idc]
                self.drop_conn(idc)
                print("Deleted idc de clients", idc, self.clients)
            except BrokenPipeError as be:
                self.report(
                    "close", "Close->Broken Pipe Error al cerrar %s bytes" %
                    (be))
                self.queue_cancel.put(idc)
                raise be
            except socket.error as se:
                self.report(
                    "close", "Close->Socket Error al leer %s bytes" % (se))
                self.queue_cancel.put(idc)
                raise se
            except asyncio.TimeoutError as te:
                self.report(
                    "close", "Close->Error Timeout al leer %d bytes" % (te))
                self.logger.exception(
                    "Tiempo fuera al leer en close, %s" % (te))
            except asyncio.IncompleteReadError as ir:
                self.report(
                    "close", "Close_>Incomplete read, reader %s" % reader)
                self.logger.exception(
                    "Station %s, Tiempo fuera al no poder leer en readbytes %s bytes, %s" % (n, self.station, ir))
            except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                self.logger.exception(
                    "Close->Excepción por desconexión al intentar leer %s" %
                    conn_error)
                self.queue_cancel.put(idc)
                raise conn_error
            except Exception as e:
                self.report("close", "Excepción no considerada", e)
                self.logger.exception(
                    "Close->Excepción no considerada al intentar leer%s" % e)
                raise e
        else:
            raise Exception("No existe %s" % idc)

    async def create_server(self, callback_io, loop):
        # SI ES UNIX SOCKET
        # includes  bind
        # https://github.com/python/asyncio/blob/fff05d480760703adbc3e2d4cb3dbcfbff803c29/asyncio/unix_events.py
        bprint("loop runing before create server")
        self.report("create server", loop.is_running())
        mode = self.mode
        context = self.context
        self.report("create server", "Creando server---_>")
        self.report("create server", loop, mode, context, AF_TYPE)
        self.server = None
        try:
            if mode == 'server':
                if AF_TYPE == socket.AF_UNIX:
                    self.report("create server",  "Se crea Socket Server Unix")
                    # ref https://docs.python.org/3/library/asyncio-eventloop.html
                    future_server = asyncio.start_unix_server(callback_io,
                                                              loop=loop,
                                                              path=self.get_path(),
                                                              limit=self.backlog,
                                                              ssl=context)
                    self.server = await asyncio.wait_for(
                        future_server, timeout=self.timeout)
                elif AF_TYPE in {socket.AF_INET, socket.AF_INET6}:
                    host = self.address[0]
                    port = self.address[1]
                    self.report("create server", "Se crea Socket Server TCPx")
                    self.report("create server", "Cleaning address")
                    self.clean_socket(host, port)
                    self.report("create server", "Closing cleaning address")
                    self.report("create server", "New server listening......")
                    rprint(host)
                    rprint(port)
                    future_server = asyncio.start_server(
                        callback_io,
                        loop=loop,
                        host=host,
                        port=port,
                        family=AF_TYPE,
                        backlog=self.backlog,
                        ssl=context)
                    self.report("create server",
                                "Future coro to run server:::")
                    rprint(future_server)
                    self.server = await asyncio.wait_for(
                        future_server, timeout=self.timeout)
                    self.report("create server",
                                "(create_server works!)El server es")
                    self.report("create server", loop)
                    print(self.server, type(self.server))
            else:
                self.report("create server", "Asigna primero mode=server")
        except asyncio.TimeoutError as te:
            self.logger.exception("Tiempo fuera en intento de cerrar conexión %s, mode %s" % (
                te, self.mode))

            await asyncio.sleep(10)
            raise te
        except (ConnectionResetError, ConnectionAbortedError) as conn_error:
            self.logger.exception("Excepción por desconexión %s, mode %s" % (
                conn_error, self.mode))
            self.report("create server",
                        "Excepcion error de conexión", conn_error)
            await asyncio.sleep(10)
        except Exception as ex:
            self.report("create server",
                        "Excepcion en create_server <::::", ex, "::::>")
        except asyncio.TimeoutError as te:
            self.report("create server", "Timeout error", te)
            raise te
        self.status = 'OFF'
        return self.server

    async def create_client(self):
        mode = self.mode
        loop = self.loop
        self.send_msg_sock_status(20)
        reader, writer = (None, None)
        idc = ""
        while self.status != 'ON':
            try:
                if mode == 'client':
                    if AF_TYPE == socket.AF_UNIX:
                        # ref https://docs.python.org/3/library/asyncio-eventloop.html
                        future_unix_client = asyncio.open_unix_connection(
                            loop=loop, path=self.get_path(), ssl=self.context)
                        (reader, writer) = await asyncio.wait_for(future_unix_client, timeout=self.timeout)
                        self.send_msg_sock_status(40)
                    elif AF_TYPE == socket.AF_INET or AF_TYPE == socket.AF_INET6:
                        host = self.address[0]
                        port = self.address[1]
                        print("La direccion es %s con tipo: %s " % (self.address,
                                                                    AF_TYPE))
                        future_client = asyncio.open_connection(
                            loop=loop,
                            host=host,
                            port=port,
                            ssl=self.context)
                        (reader, writer) = await asyncio.wait_for(future_client, timeout=self.timeout)
                        self.send_msg_sock_status(40)
                    idc = await self.set_reader_writer(reader, writer)
                    self.report("create client", "Cliente creado--->", idc)
                    self.report("create client", "Clientes", self.clients)
                    self.send_msg_sock_status(50)
                    self.alert = "Conectado a socket-base"
                    self.status = 'ON'
                    self.report("create client", self.alert)
                    self.report("create client", "Creando nuevo client")
            except asyncio.TimeoutError as te:
                self.logger.exception("Tiempo fuera en intento de cerrar conexión %s, mode %s" % (
                    te, self.mode))
                self.report("create server", "Excepcion error de timeout", te)
                self.status = 'OFF'
                await asyncio.sleep(10)
            except (ConnectionResetError, ConnectionAbortedError) as conn_error:
                self.logger.exception("Excepción por desconexión %s, mode %s" % (
                    conn_error, self.mode))
                await asyncio.sleep(10)
                self.status = 'OFF'
            except Exception as ex:
                self.report("create client", "Excepcion en", ex)
                print("Creating new client?", self.new_client)
                self.send_msg_sock_status(-1)
                self.status = 'OFF'
                await asyncio.sleep(10)
        return idc

    def set_backlog(self, new_backlog):
        # ?
        assert isinstance(new_backlog,
                          int), "El nuevo backlog no es un valor válido"
        self.backlog = new_backlog

    async def accept(self):
        conn, addr = await self.loop.sock_accept(self.server.sockets[0])
        self.conns.append(conn)
        self.addrs.append(addr)
        self.conn = conn
        self.addr = addr
        self.status = 'ON'
        return conn, addr

    def list_clients(self):
        for i in range(len(self.conss)):
            print(str(self.addrs[i]) + ":" + str(self.conns[i]))

    def clean_client(self, idc):
        self.report("clean_client", "Limpiando cliente", idc)
        if idc in self.clients:
            client = self.clients.get(idc)
            client.get('writer').close()
            del self.clients[idc]

    async def wait_closed(self):
        for ids, client in self.clients.items():
            await client.get('writer').wait_closed()
        if self.mode == 'server' and self.server:
            await self.server.wait_closed()

    async def server(self):
        await self.create_server()

    async def client(self):
        return await self.create_client()
        # Connect to path

    def get_name(self):
        return self.gnc_path

    def __enter__(self):
        self.report("enter socket", "Starting GNC Socket (enter)")
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        bprint("="*20)
        self.report("enter socket", "Enviando EOF al otro lado")
        self.report("enter socket", "Clossing succesful, Socket exit->",
                    exception_type, exception_value, traceback)
        self.report("enter socket", "Socket exit -> traceback", traceback)
        self.report("enter socket", "Closing GNC Socket")
        # self.close()
        self.report("enter socket", "Socket closed")
        self.report("enter socket", self.loop)
        self.report("enter socket", "Loop status |^")
        # self.loop.run_until_complete(self.wait_closed())
        self.report("enter socket", "="*20)
