"""
SneDevice to configure SNE
"""
import subprocess
import requests, time
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import shutil
import xml.dom.minidom as xmldom
from test_framework.testbase.settings import *

class SneDevice():

    """
    SNE Session using Genie
    """

    def __init__(self, sne_device, logger, out_dir):
        """Initialize StcClient instance from testbed data."""
        self._logger = logger
        self._mapguid = None
        self._name_port_map = {}
        self._chassis = None
        self._tmp_config_file = None
        self._out_dir = out_dir

        if not sne_device or sne_device.type != SNE_TYPE:
            raise RuntimeError("Missing sne device")

        ifaces = sne_device.interfaces
        for iface in ifaces.values():
            parsed_iface = iface.parse_interface_name()
            self._name_port_map[iface.alias] = parsed_iface.port

        self._chassis = str(sne_device.connections.chassis.ip)
        self.url_get_maps = 'http://' + self._chassis + '/api/maps'
        self.url_upload = 'http://' + self._chassis + '/api/maps/upload'
        self.http_timeout = 5
        self.head_content_0 = {"Content-Length":'0'} 

    def get_request(self, get_url, err_msg):
        response = None
        try:
            response = requests.get(url=get_url, timeout=self.http_timeout)
            response.raise_for_status()
        except Exception as error:
            msg = err_msg + ': ' + str(error)
            self._logger.error(msg)
            raise RuntimeError(msg)
        return response       

    def put_request(self, put_url, put_headers, err_msg):
        response = None
        try:
            response = requests.put(url=put_url, headers=put_headers, timeout=self.http_timeout)
            response.raise_for_status()
        except Exception as error:
            msg = err_msg + ': ' + str(error)
            self._logger.error(msg)
            raise RuntimeError(msg)
        time.sleep(SNE_CLI_COMMAND_DELAY)
        return response

    def post_request(self, post_url, post_data, post_headers, err_msg):
        response = None
        try:
            response = requests.post(url=post_url, data=post_data, headers=post_headers, timeout=self.http_timeout)
            response.raise_for_status()
        except Exception as error:
            msg = err_msg + ': ' + str(error)
            self._logger.error(msg)
            raise RuntimeError(msg)
        time.sleep(SNE_CLI_COMMAND_DELAY)
        return response  

    def configure(self):
        '''configure command'''
        port_list = []
        self._logger.info(object=SNE_OBJECT, event="configure")
        response = self.get_request(self.url_get_maps, 'Error when get sne map info.')
        self._logger.info('Sne maps info is: {0}'.format(response.text))
        dict_response = response.json()
        #get all ports used currently
        if dict_response.get('maps'):
            for sne_map in dict_response.get('maps'):
                if sne_map.get('portsUsed'):
                    port_list.extend(sne_map.get('portsUsed').split(','))
        #raise error if ports are used by other user
        for value in self._name_port_map.values():
            value_map = str(int(value) + 1)
            if value_map in port_list:
                raise RuntimeError("Port {0} of SNE {1} is used by other user currently.".format(value, self._chassis))

    def upload(self, config_file=None):
        '''upload command'''
        #Sne does not supprot the ports relocatoin., so need replace the port number of sne configuration file
        if config_file is None:
            config = SNE_CONFIG_FILE
        else:
            config = config_file
        self._replace_ports_mapname(config)
        if os.path.exists(self._tmp_config_file):
            config = self._tmp_config_file
        self._logger.info(object=SNE_OBJECT, event="upload_configuration")
        mp_encoder = MultipartEncoder(fields={'mapFile': ('snemap_testpack.xml', open(config, 'rb'))})
        response = self.post_request(self.url_upload, mp_encoder, {'Content-Type': mp_encoder.content_type}, 'Error when upload sne config.')
        dict_response = response.json()
        try:
            self._mapguid = dict_response.get('map').get('mapId')
            self._logger.info('....map id is {0} after upload.'.format(self._mapguid))
        except Exception as error:
            raise RuntimeError("Error when get mapid: {0}".format(error))
        self.url_map = 'http://' + self._chassis + '/api/maps/' + self._mapguid
        response = self.get_request(self.url_get_maps, 'Error when get sne map info.')
        self._logger.info('Sne maps info is {0} after upload.'.format(response.text))

    def unload(self):
        '''Stop command'''
        #get corresponding map by mapid, should stop it firstly if state is active
        response = self.get_request(self.url_get_maps, 'Error when get sne map info.')
        self._logger.info('Sne maps info is when stop: {0}'.format(response.text))
        dict_response = response.json()
        if dict_response.get('maps'):
            for sne_map in dict_response.get('maps'):
                if sne_map.get('mapId') and sne_map.get('mapId') == self._mapguid:
                    if sne_map.get('state') and sne_map.get('state') == 'Active':
                        self.put_request(self.url_stop, self.head_content_0, 'Error when stop sne.')
                    url_unload = self.url_map + '/unload'
                    self.put_request(url_unload, self.head_content_0, 'Error when unload sne.')

    def linkdown(self, port):
        '''Linkdown command'''
        url_linkdown = self.url_map + '/' + port + '/linkdown'
        url_get_port = self.url_map + '/' + port
        self.put_request(url_linkdown, self.head_content_0, 'Error when break sne port.')
        response = self.get_request(url_get_port, 'Error when get sne port status.')
        self._logger.info(object=SNE_OBJECT, info='port info is {0} after linkdown'.format(response.text))

    def linkup(self, port):
        '''Linkup command'''
        url_linkup = self.url_map + '/' + port + '/linkup'
        url_get_port = self.url_map + '/' + port
        self.put_request(url_linkup, self.head_content_0, 'Error when recover sne port.')
        response = self.get_request(url_get_port, 'Error when get sne port status.')
        self._logger.info(object=SNE_OBJECT, info='port info is {0} after linkup'.format(response.text))

    def start(self):
        '''start command'''
        url_start = self.url_map + '/start'
        self.put_request(url_start, self.head_content_0, 'Error when start sne.')
        response = self.get_request(self.url_get_maps, 'Error when get sne map info.')
        self._logger.info(object=SNE_OBJECT, info='map info is {0} after start'.format(response.text))

    def stop(self):
        '''Stop command'''
        url_stop = self.url_map + '/stop'
        self.put_request(url_stop, self.head_content_0, 'Error when stop sne.')
        response = self.get_request(self.url_get_maps, 'Error when get sne map info.')
        self._logger.info(object=SNE_OBJECT, info='map info is {0} after stop'.format(response.text))

    def _replace_ports_mapname(self, config):
        '''replace the port number and map name in the configuration file'''
        write_file = False
        domobj = xmldom.parse(config)
        elementobj = domobj.documentElement
        sub_element_obj = elementobj.getElementsByTagName("Objects")
        if sub_element_obj:
            object_count = sub_element_obj[0].getAttribute("Count")
            for i in range(1, int(object_count)+1):
                sub_object_element = elementobj.getElementsByTagName("Object" + str(i))
                name = sub_object_element[0].getAttribute("Name")

                if name in self._name_port_map.keys():
                    item = sub_object_element.item(0)
                    port_item = item.getElementsByTagName('Port')
                    if (port_item) and (port_item[0].firstChild.data != self._name_port_map[name]):
                        port_item[0].firstChild.data = self._name_port_map[name]
                        write_file = True
        self._tmp_config_file = os.path.join(self._out_dir, os.path.basename(config))
        if write_file:
            try:
                file_handle = open(self._tmp_config_file, 'w', encoding='UTF-8')
                elementobj.writexml(file_handle)
                file_handle.close()
            except:
                raise RuntimeError("Cannot write SNE temp configuration file")
        else:
            shutil.copyfile(config, self._tmp_config_file)
