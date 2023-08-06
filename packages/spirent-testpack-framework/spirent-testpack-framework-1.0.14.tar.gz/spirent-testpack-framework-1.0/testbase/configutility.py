"""
To parse Yaml configuration file
"""
class BaseConfig():
    """
    It is base Class for parsing config parameters.
    """
    def __init__(self, cfg):
        if cfg is None:
            raise RuntimeError("Config object is None")
        self._cfg = cfg

        #phy, speed, auto_negotiation come from testbed yaml file
        self.port_phy = self.get_value(['phy'])
        self.port_speed = self.get_value(['speed'])
        self.auto_negotiation = self.get_value(['auto_negotiation'])
        self.ucs_line_rate = self.get_value(['ucs_line_rate'])
        self.bandwidth_limitation_ucs1 = self.get_value(['bandwidth_limitation_ucs1'])
        self.bandwidth_limitation_ucs2 = self.get_value(['bandwidth_limitation_ucs2'])
        self.bandwidth_limitation_tolerance = self.get_value(['bandwidth_limitation_tolerance'])
        self.packet_loss_tolerance = self.get_value(['packet_loss_tolerance'])
        self.swvc_reserved_ipv4_prefix = self.get_value(['swvc_reserved_ipv4_prefix'])
        self.swvc_reserved_ipv6_prefix = self.get_value(['swvc_reserved_ipv6_prefix'])
        self.tunnel_destination_address = self.get_value(['tunnel_destination_address'])
        self.max_wait_time_after_break_link = self.get_value(['max_wait_time_after_break_link'])
        self.max_wait_time_after_recover_link = self.get_value(['max_wait_time_after_recover_link'])
        self.vrrp_switchover_time = self.get_value(['vrrp_switchover_time'])
        self.vrrp_switchback_time = self.get_value(['vrrp_switchback_time'])
        self.vrrp_wait_time_non_preempt = self.get_value(['vrrp_wait_time_non_preempt'])
        self.tolerance_traffic_rate = self.get_value(['tolerance_traffic_rate'])
        self.tolerance_connection_failure = self.get_value(['tolerance_connection_failure'])
        self.delta_loadbalance_per_flow = self.get_value(['delta_loadbalance_per_flow'])
        self.ipv6_mtu = self.get_value(['ipv6_mtu'])
        self.mef70_o1_flag = self.get_value(['mef70_o1_flag'])
        self.nat_server_existence = self.get_value(['nat_server_existence'])
        self.nat_server_ip = self.get_value(['nat_server_ip'])
        self.policy_apply_delay = self.get_value(['policy_apply_delay'])
        self.latency_traffic_load = self.get_value(['latency_traffic_load'])
        self.internet_port_behind_nat = self.get_value(['internet_port_behind_nat'])
        self.internet_port_public_address = self.get_value(['internet_port_public_address'])
        self.throughput_frame_size_list = self.get_value(['throughput_frame_size_list'])
        self.throughput_imix_list = self.get_value(['throughput_imix_list'])
        self.throughput_initial_rate = self.get_value(['throughput_initial_rate'])
        self.tcp_setup_rate_duration = self.get_value(['tcp_setup_rate_duration'])
        self.tcp_setup_rate_rate_lower_limit = self.get_value(['tcp_setup_rate_rate_lower_limit'])
        self.tcp_setup_rate_rate_upper_limit = self.get_value(['tcp_setup_rate_rate_upper_limit'])
        self.tcp_setup_rate_initial_rate = self.get_value(['tcp_setup_rate_initial_rate'])
        self.tcp_setup_rate_resolution = self.get_value(['tcp_setup_rate_resolution'])
        self.tcp_setup_rate_transactions_per_connection = self.get_value(['tcp_setup_rate_transactions_per_connection'])
        self.tcp_setup_rate_server_payload_size = self.get_value(['tcp_setup_rate_server_payload_size'])
        self.application_throughput_duration = self.get_value(['application_throughput_duration'])
        self.application_throughput_ramp_up = self.get_value(['application_throughput_ramp_up'])
        self.application_throughput_ramp_down = self.get_value(['application_throughput_ramp_down'])
        self.application_throughput_protocol_distribution = self.get_value(['application_throughput_protocol_distribution'])
        self.application_throughput_rate_lower_limit = self.get_value(['application_throughput_rate_lower_limit'])
        self.application_throughput_rate_upper_limit = self.get_value(['application_throughput_rate_upper_limit'])
        self.application_throughput_initial_rate = self.get_value(['application_throughput_initial_rate'])
        self.application_throughput_resolution = self.get_value(['application_throughput_resolution'])
        if self.ucs_line_rate:
            if not (isinstance(self.ucs_line_rate, int) and self.ucs_line_rate > 0):
                raise RuntimeError("ucs_line_rate should be positive integer, actual value : {0}".format(self.ucs_line_rate))
        if self.vrrp_switchover_time:
            if not (isinstance(self.vrrp_switchover_time, int) and self.vrrp_switchover_time > 0):
                raise RuntimeError("vrrp_switchover_time should be positive integer, actual value : {0}".format(self.vrrp_switchover_time))
        if self.vrrp_switchback_time:
            if not (isinstance(self.vrrp_switchback_time, int) and self.vrrp_switchback_time > 0):
                raise RuntimeError("vrrp_switchback_time should be positive integer, actual value : {0}".format(self.vrrp_switchback_time))
        if self.vrrp_wait_time_non_preempt:
            if not (isinstance(self.vrrp_wait_time_non_preempt, int) and self.vrrp_wait_time_non_preempt > 0):
                raise RuntimeError("vrrp_wait_time_non_preempt should be positive integer, actual value : {0}".format(self.vrrp_wait_time_non_preempt))
        if self.ipv6_mtu:
            if not (isinstance(self.ipv6_mtu, int) and self.ipv6_mtu > 0):
                raise RuntimeError("ipv6_mtu should be positive integer, actual value : {0}".format(self.ipv6_mtu))
        if self.mef70_o1_flag:
            if not (self.mef70_o1_flag == 0 or self.mef70_o1_flag == 1):
                raise RuntimeError("mef70_o1_flag should be integer 0 or 1, actual value : {0}".format(self.mef70_o1_flag))
        if self.policy_apply_delay:
            if not (isinstance(self.policy_apply_delay, int) and self.policy_apply_delay > 0):
                raise RuntimeError("policy_apply_delay should be positive integer, actual value : {0}".format(self.policy_apply_delay))
        if self.bandwidth_limitation_ucs1:
            if not (isinstance(self.bandwidth_limitation_ucs1, str) and self.bandwidth_limitation_ucs1[-1:] == '%' and self.bandwidth_limitation_ucs1[:-1].isdigit()):
                raise RuntimeError("bandwidth limitation of ucs1 should be formatted as X% and X should be integer, actual value : {0}".format(self.bandwidth_limitation_ucs1))
            self.bandwidth_limitation_ucs1 = self.bandwidth_limitation_ucs1.replace('%', '')
            float_bandwidth_limitation_ucs1 = float(self.bandwidth_limitation_ucs1)
            self.bandwidth_limitation_ucs1 = float_bandwidth_limitation_ucs1 / 100
            if self.bandwidth_limitation_ucs1 > 1 or self.bandwidth_limitation_ucs1 < 0.01:
                raise RuntimeError("bandwidth limitation of ucs1 should between 1% and 100%, actual value : {0}%".format(float_bandwidth_limitation_ucs1))
        if self.bandwidth_limitation_ucs2:
            if not (isinstance(self.bandwidth_limitation_ucs2, str) and self.bandwidth_limitation_ucs2[-1:] == '%' and self.bandwidth_limitation_ucs2[:-1].isdigit()):
                raise RuntimeError("bandwidth limitation of ucs2 should be formatted as X% and X should be integer, actual value : {0}".format(self.bandwidth_limitation_ucs2))
            self.bandwidth_limitation_ucs2 = self.bandwidth_limitation_ucs2.replace('%', '')
            float_bandwidth_limitation_ucs2 = float(self.bandwidth_limitation_ucs2)
            self.bandwidth_limitation_ucs2 = float_bandwidth_limitation_ucs2 / 100
            if self.bandwidth_limitation_ucs2 > 1 or self.bandwidth_limitation_ucs2 < 0.01:
                raise RuntimeError("bandwidth limitation of ucs2 should between 1% and 100%, actual value : {0}%".format(float_bandwidth_limitation_ucs2))
        if self.bandwidth_limitation_tolerance:
            if not (isinstance(self.bandwidth_limitation_tolerance, str) and self.bandwidth_limitation_tolerance[-1:] == '%' and self.bandwidth_limitation_tolerance[:-1].isdigit()):
                raise RuntimeError("bandwidth tolerance should be formatted as X% and X should be integer, actual value : {0}".format(self.bandwidth_limitation_tolerance))
            self.bandwidth_limitation_tolerance = self.bandwidth_limitation_tolerance.replace('%', '')
            float_bandwidth_limitation_tolerance = float(self.bandwidth_limitation_tolerance)
            self.bandwidth_limitation_tolerance = float_bandwidth_limitation_tolerance / 100
            if self.bandwidth_limitation_tolerance > 1 or self.bandwidth_limitation_tolerance < 0.01:
                raise RuntimeError("bandwidth tolerance should between 1% and 100%, actual value : {0}%".format(float_bandwidth_limitation_tolerance))
        if self.packet_loss_tolerance:
            if not (isinstance(self.packet_loss_tolerance, str) and self.packet_loss_tolerance[-1:] == '%' and self.packet_loss_tolerance[:-1].isdigit()):
                raise RuntimeError("internet_packet_loss tolerance should be formatted as X% and X should be integer, actual value : {0}".format(self.packet_loss_tolerance))
            self.packet_loss_tolerance = self.packet_loss_tolerance.replace('%', '')
            float_packet_loss_tolerance = float(self.packet_loss_tolerance)
            self.packet_loss_tolerance = float_packet_loss_tolerance / 100
            if self.packet_loss_tolerance > 1 or self.packet_loss_tolerance < 0:
                raise RuntimeError("internet_packet_loss tolerance should between 0% and 100%, actual value : {0}%".format(float_packet_loss_tolerance))
        if self.tolerance_traffic_rate:
            if not (isinstance(self.tolerance_traffic_rate, str) and self.tolerance_traffic_rate[-1:] == '%' and self.tolerance_traffic_rate[:-1].isdigit()):
                raise RuntimeError("tolerance of traffic rate should be formatted as X% and X should be integer, actual value : {0}".format(self.tolerance_traffic_rate))
            self.tolerance_traffic_rate = self.tolerance_traffic_rate.replace('%', '')
            float_tolerance_traffic_rate = float(self.tolerance_traffic_rate)
            self.tolerance_traffic_rate = float_tolerance_traffic_rate / 100
            if self.tolerance_traffic_rate > 1 or self.tolerance_traffic_rate < 0.01:
                raise RuntimeError("tolerance of traffic rate should between 1% and 100%, actual value : {0}%".format(float_tolerance_traffic_rate))

        if self.tolerance_connection_failure:
            if not (isinstance(self.tolerance_connection_failure, str) and self.tolerance_connection_failure[-1:] == '%' \
                    and self.tolerance_connection_failure[:-1].isdigit()):
                raise RuntimeError("tolerance of traffic connection failure rate should between 0% and 100%, actual value : {0}%".format(self.tolerance_connection_failure))
            self.tolerance_connection_failure = self.tolerance_connection_failure.replace('%', '')
            int_tolerance_connection_failure = int(self.tolerance_connection_failure)
            self.tolerance_connection_failure = int_tolerance_connection_failure
            if self.tolerance_connection_failure > 100 or self.tolerance_connection_failure < 0:
                raise RuntimeError("tolerance of connection failure ratio should between 0% and 100%, actual value : {0}%".format(int_tolerance_connection_failure))

        if self.delta_loadbalance_per_flow:
            if not (isinstance(self.delta_loadbalance_per_flow, str) and self.delta_loadbalance_per_flow[-1:] == '%' and self.delta_loadbalance_per_flow[:-1].isdigit()):
                raise RuntimeError("delta_loadbalance_per_flow should be formatted as X% and X should be integer, actual value : {0}".format(self.delta_loadbalance_per_flow))
            self.delta_loadbalance_per_flow = self.delta_loadbalance_per_flow.replace('%', '')
            float_delta_loadbalance_per_flow = float(self.delta_loadbalance_per_flow)
            self.delta_loadbalance_per_flow = float_delta_loadbalance_per_flow / 100
            if self.delta_loadbalance_per_flow > 1 or self.delta_loadbalance_per_flow < 0.01:
                raise RuntimeError("delta_loadbalance_per_flow should between 1% and 100%, actual value : {0}%".format(float_delta_loadbalance_per_flow))
        if self.latency_traffic_load:
            try:
                traffic_load_list = self.latency_traffic_load.split(' ')
                for traffic_load in traffic_load_list:
                    if not (traffic_load.isdigit() and int(traffic_load) >= 1 and int(traffic_load) <= 100):
                        raise RuntimeError("latency_traffic_load should be formatted as 'a b c...' and a b c should be integer between 1 and 100, actual value : {0}".format(self.latency_traffic_load))
            except:
                raise RuntimeError("latency_traffic_load should be formatted as 'a b c...' and a b c should be integer between 1 and 100, actual value : {0}".format(latency_traffic_load))
        if self.throughput_initial_rate:
            if not(float(self.throughput_initial_rate.replace('%', '')) >= 0.001 and float(self.throughput_initial_rate.replace('%', '')) <= 100):
                raise RuntimeError("throughput_initial_rate should between 0.001% and 100%, actual value : {0}".format(self.throughput_initial_rate))
        if not self.tcp_setup_rate_duration:
            self.tcp_setup_rate_duration = 60
        if not self.tcp_setup_rate_rate_lower_limit:
            self.tcp_setup_rate_rate_lower_limit = 100
        if not self.tcp_setup_rate_rate_upper_limit:
            self.tcp_setup_rate_rate_upper_limit = 10000
        if not self.tcp_setup_rate_initial_rate:
            self.tcp_setup_rate_initial_rate = 1000
        if not self.tcp_setup_rate_resolution:
            self.tcp_setup_rate_resolution = 100
        if not self.tcp_setup_rate_transactions_per_connection:
            self.tcp_setup_rate_transactions_per_connection = 1
        if not self.tcp_setup_rate_server_payload_size:
            self.tcp_setup_rate_server_payload_size = 64
        if not (isinstance(self.tcp_setup_rate_duration, int) and self.tcp_setup_rate_duration >= 10):
            raise RuntimeError("tcp_setup_rate_duration should be positive integer and not be less than 10, actual value : {0}".format(self.tcp_setup_rate_duration))
        if not (isinstance(self.tcp_setup_rate_rate_lower_limit, int) and self.tcp_setup_rate_rate_lower_limit > 0):
            raise RuntimeError("tcp_setup_rate_rate_lower_limit should be positive integer, actual value : {0}".format(self.tcp_setup_rate_rate_lower_limit))
        if not (isinstance(self.tcp_setup_rate_rate_upper_limit, int) and self.tcp_setup_rate_rate_upper_limit > 0):
            raise RuntimeError("tcp_setup_rate_rate_upper_limit should be positive integer, actual value : {0}".format(self.tcp_setup_rate_rate_upper_limit))
        if not (isinstance(self.tcp_setup_rate_initial_rate, int) and self.tcp_setup_rate_initial_rate > 0):
            raise RuntimeError("tcp_setup_rate_initial_rate should be positive integer, actual value : {0}".format(self.tcp_setup_rate_initial_rate))
        if not (isinstance(self.tcp_setup_rate_resolution, int) and self.tcp_setup_rate_resolution > 0):
            raise RuntimeError("tcp_setup_rate_resolution should be positive integer, actual value : {0}".format(self.tcp_setup_rate_resolution))
        if not (isinstance(self.tcp_setup_rate_transactions_per_connection, int) and self.tcp_setup_rate_transactions_per_connection > 0):
            raise RuntimeError("tcp_setup_rate_transactions_per_connection should be positive integer, actual value : {0}".format(self.tcp_setup_rate_transactions_per_connection))
        if not (isinstance(self.tcp_setup_rate_server_payload_size, int) and self.tcp_setup_rate_server_payload_size >= 0):
            raise RuntimeError("tcp_setup_rate_server_payload_size should be integer and not be less than 0, actual value : {0}".format(self.tcp_setup_rate_server_payload_size))
        if not(self.tcp_setup_rate_rate_lower_limit < self.tcp_setup_rate_rate_upper_limit):
            raise RuntimeError("tcp_setup_rate_rate_lower_limit should be less than tcp_setup_rate_rate_upper_limit, actual rate_lower_limit and rate_upper_limit value is : {0}, {1}".format(self.tcp_setup_rate_rate_lower_limit, self.tcp_setup_rate_rate_upper_limit))
        if not(self.tcp_setup_rate_initial_rate > self.tcp_setup_rate_rate_lower_limit and self.tcp_setup_rate_initial_rate < self.tcp_setup_rate_rate_upper_limit):
            raise RuntimeError("initial_rate should between rate_lower_limit and rate_upper_limit, actual initial_rate, rate_lower_limit and rate_upper_limit value is : {0}, {1}, {2}".format(self.tcp_setup_rate_initial_rate, self.tcp_setup_rate_rate_lower_limit, self.tcp_setup_rate_rate_upper_limit))
        if not self.application_throughput_duration:
            self.application_throughput_duration = 120
        if not self.application_throughput_ramp_up:
            self.application_throughput_ramp_up = 10
        if not self.application_throughput_ramp_down:
            self.application_throughput_ramp_down = 10
        if not self.application_throughput_rate_lower_limit:
            self.application_throughput_rate_lower_limit = '1%'
        if not self.application_throughput_rate_upper_limit:
            self.application_throughput_rate_upper_limit = '100%'
        if not self.application_throughput_initial_rate:
            self.application_throughput_initial_rate = '10%'
        if not self.application_throughput_resolution:
            self.application_throughput_resolution = '1%'
        if not self.application_throughput_protocol_distribution:
            self.application_throughput_protocol_distribution = '7% 7% 7% 7% 7% 7% 4.5% 4.5% 7% 7% 7% 7% 7% 7% 7%'
        if not (isinstance(self.application_throughput_duration, int) and self.application_throughput_duration >= 120):
            raise RuntimeError("application_throughput_duration should be positive integer and not be less than 120, actual value : {0}".format(self.application_throughput_duration))
        if not (isinstance(self.application_throughput_ramp_up, int) and self.application_throughput_ramp_up >= 10):
            raise RuntimeError("application_throughput_ramp_up should be positive integer and not be less than 10, actual value : {0}".format(self.application_throughput_ramp_up))
        if not (isinstance(self.application_throughput_ramp_down, int) and self.application_throughput_ramp_down >= 10):
            raise RuntimeError("application_throughput_ramp_down should be positive integer and not be less than 10, actual value : {0}".format(self.application_throughput_ramp_down))
        if (self.application_throughput_duration - self.application_throughput_ramp_up - self.application_throughput_ramp_down) < 100:
            raise RuntimeError("steady time(duration - ramp_up - ramp_down) should not be less than 100 seconds, actual value : {0}".format((self.application_throughput_duration - self.application_throughput_ramp_up - self.application_throughput_ramp_down)))        
        if not (isinstance(self.application_throughput_rate_lower_limit, str) and self.application_throughput_rate_lower_limit[-1:] == '%'):
            raise RuntimeError("application_throughput_rate_lower_limit should be formatted as X%, actual value : {0}".format(self.application_throughput_rate_lower_limit))
        if not (isinstance(self.application_throughput_rate_upper_limit, str) and self.application_throughput_rate_upper_limit[-1:] == '%'):
            raise RuntimeError("application_throughput_rate_upper_limit should be formatted as X%, actual value : {0}".format(self.application_throughput_rate_upper_limit))
        if not (isinstance(self.application_throughput_initial_rate, str) and self.application_throughput_initial_rate[-1:] == '%'):
            raise RuntimeError("application_throughput_initial_rate should be formatted as X%, actual value : {0}".format(self.application_throughput_initial_rate))
        if not (isinstance(self.application_throughput_resolution, str) and self.application_throughput_resolution[-1:] == '%'):
            raise RuntimeError("application_throughput_resolution should be formatted as X%, actual value : {0}".format(self.application_throughput_resolution))
        if isinstance(self.application_throughput_protocol_distribution, str):
            sum_distribution = 0
            list_distribution = self.application_throughput_protocol_distribution.split(' ')
            if len(list_distribution) != 15:
                raise RuntimeError("application_throughput_protocol_distribution should be formatted as 'X% X% X% X% X% X% X% X% X% X% X% X% X% X% X%', actual value : {0}".format(self.application_throughput_protocol_distribution))
            for ele in list_distribution:
                # if not(ele[-1:] == '%' and ele[:-1].isdigit()):
                    # raise RuntimeError("application_throughput_protocol_distribution should be formatted as 'X% X% X% X% X% X% X% X% X% X% X% X% X% X% X%', actual value : {0}".format(self.application_throughput_protocol_distribution))
                sum_distribution += float(ele[:-1])
            if sum_distribution != float(100):
                raise RuntimeError("sum of every throughput_protocol_distribution percentage should be 100%, actual value : {0}".format(sum_distribution))
        else:
            raise RuntimeError("type of application_throughput_protocol_distribution should be string")
        if not(float(self.application_throughput_rate_lower_limit.replace('%', '')) >= 0.01 and float(self.application_throughput_rate_lower_limit.replace('%', '')) <= 100):
            raise RuntimeError("application_throughput_rate_lower_limit should between 0.01% and 100%, actual value : {0}".format(self.application_throughput_rate_lower_limit))
        if not(float(self.application_throughput_rate_upper_limit.replace('%', '')) >= 0.01 and float(self.application_throughput_rate_upper_limit.replace('%', '')) <= 100):
            raise RuntimeError("application_throughput_rate_upper_limit should between 0.01% and 100%, actual value : {0}".format(self.application_throughput_rate_upper_limit))
        if not(float(self.application_throughput_initial_rate.replace('%', '')) >= 0.01 and float(self.application_throughput_initial_rate.replace('%', '')) <= 100):
            raise RuntimeError("application_throughput_initial_rate should between 0.01% and 100%, actual value : {0}".format(self.application_throughput_initial_rate))
        if not(float(self.application_throughput_resolution.replace('%', '')) >= 0.01 and float(self.application_throughput_resolution.replace('%', '')) <= 100):
            raise RuntimeError("application_throughput_resolution should between 0.01% and 100%, actual value : {0}".format(self.application_throughput_resolution))
        if not(self.application_throughput_rate_lower_limit < self.application_throughput_rate_upper_limit):
            raise RuntimeError("application_throughput_rate_lower_limit should be less than application_throughput_rate_upper_limit, actual rate_lower_limit and rate_upper_limit value is : {0}, {1}".format(self.application_throughput_rate_lower_limit, self.application_throughput_rate_upper_limit))
        if not(self.application_throughput_initial_rate > self.application_throughput_rate_lower_limit and self.application_throughput_initial_rate < self.application_throughput_rate_upper_limit):
            raise RuntimeError("initial_rate should between rate_lower_limit and rate_upper_limit, actual initial_rate, rate_lower_limit and rate_upper_limit value is : {0}, {1}, {2}".format(self.application_throughput_initial_rate, self.application_throughput_rate_lower_limit, self.application_throughput_rate_upper_limit))

    def get_value(self, param_list):
        '''Get the parameters value.'''
        config_dict = self._cfg
        for key in param_list:
            if key in config_dict:
                config_dict = config_dict[key]
            else:
                return ''
        return config_dict

class SneConfig(BaseConfig):
    """
    Sne config Class for parsing SNE config parameters
    """
    def __init__(self, cfg):
        super().__init__(cfg)
        #Disruptor
        self.disruptor_delay = self.get_value(['Disruptor', 'PacketDelayDisruptor', 'Delay'])
        self.disruptor_jitter = self.get_value(['Disruptor', 'PacketDelayDisruptor', 'Jitter'])
        self.disruptor_duration = self.get_value(['Disruptor', 'PacketDelayDisruptor', 'Duration'])
        self.disruptor_max_throughput = self.get_value(['Disruptor', 'PacketDelayDisruptor', 'MaxThroughput'])

        #Corruptor
        self.corruptor_drop_count = self.get_value(['Corruptor', 'PacketDropCorruptor', 'DropCount'])
        self.corruptor_duration = self.get_value(['Corruptor', 'PacketDropCorruptor', 'Duration'])
        self.corruptor_packet_count = self.get_value(['Corruptor', 'PacketDropCorruptor', 'PerPacketCount'])
