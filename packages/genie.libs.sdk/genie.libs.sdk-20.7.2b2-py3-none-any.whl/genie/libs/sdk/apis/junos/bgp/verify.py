"""Common verification functions for bgp"""

# Python
import re
import logging

# Genie
from genie.utils.dq import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_bgp_best_path(device,
                         target_route,
                         ip_address=None,
                         preference=None,
                         active_tag='*',
                         max_time=60, 
                         check_interval=10
                        ):
    """ Verify Best path is toward $ip_address or with preference $preference

        Args:
            device (`obj`): Device object
            target_route (`str`): Target route to check
            ip_address (`str`): IP Address to verify is best path, default: None
            preference (`int`): Preference of best path, default: None
            active_tag (`str`, optional): Active tag to check, default: '*' (best path)
            max_time (`int`, optional): Max time, default: 60
            check_interval (`int`, optional): Check interval, default: 10
        
        Returns:
            result (`bool`): Verified result
        
        Raises:
            N/A 
    """    
    timeout = Timeout(max_time, check_interval)
    
    preference = str(preference)
    
    while timeout.iterate():
        try:
            output = device.parse('show route protocol bgp')
        except SchemaEmptyParserError:
            log.info('Failed to parse. Device output might contain nothing.')
            timeout.sleep()
            continue
        
        # schema = {
        #     "route-information": {
        #         "route-table": [
        #             {
        #                   ...
        #                 "rt": [
        #                     {
        #                         "rt-destination": str,
        #                         "rt-entry": {
        #                             "active-tag": str,
        #                             "age": {
        #                                 "#text": str,
        #                             },
        #                                   ...
        #                             "preference": str,
        #                              ...
        #                         }
        #                     }
        #                 ],
        #                 ...
        #             }
        #         ]
        #     }
        # }
        
        route_tables = output.q.get_values('route-table')
        
        for routes in route_tables:
            rt_list = routes.get('rt')
            
            if rt_list:
                for rt in rt_list:
                    rt_entry = rt.get('rt-entry')
                    
                    # Check route and make sure is a best path ('*')
                    if (
                        rt.get('rt-destination') == target_route     
                        and rt_entry.get('active-tag') == active_tag
                    ):  
                        # Verify best path IP address or Prference to best path
                        if (
                            rt_entry.get('learned-from') == ip_address 
                            or rt_entry.get('local-preference') == preference
                        ):
                            return True
                    
        timeout.sleep()
    return False 

def verify_bgp_peer_state(device, interface, expected_state, max_time=60, check_interval=10):
    """
    Verify bgp peer state

    Args:
        device('obj'): device to use
        interface('str'): Peer interface   
        expected_state('str') : Expected peer state
        max_time ('int', optional): Maximum time to keep checking. Default to 60
        check_interval ('int', optional): How often to check. Default to 10

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    # show commands: "show bgp neighbor"

    # {'bgp-information': {'bgp-peer': [{
    #                                 'flap-count': '0',
    #                                 'peer-address': '20.0.0.3+63208', 
    #                                 'peer-state': 'Established',
    #                                   .
    #                                   .
    #                                   .

  
    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        peers_list = out.q.get_values("bgp-peer")

        for peer in peers_list:
            peer_interface = peer.get('peer-address')
            peer_state = peer.get("peer-state")

            # 20.0.0.3+63208
            if '+' in peer_interface:
                peer_interface = peer_interface.split('+')[0]

            if peer_interface == interface and peer_state == expected_state:
                return True 

        timeout.sleep()
    return False     


def verify_bgp_last_error(device, interface, expected_error, max_time=60, check_interval=10):
    """
    Verify bgp last error

    Args:
        device('obj'): device to use
        interface('str'): Peer interface   
        expected_error('str') : Expected last error
        max_time ('int', optional): Maximum time to keep checking. Default to 60
        check_interval ('int', optional): How often to check. Default to 10

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    # show commands: "show bgp neighbor"

    # {'bgp-information': {'bgp-peer': [{
    #                                 'flap-count': '0',
    #                                 'peer-address': '20.0.0.3+63208', 
    #                                 'last-error': 'None',
    #                                   .
    #                                   .
    #                                   .

  
    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        peers_list = out.q.get_values("bgp-peer")

        for peer in peers_list:
            peer_interface = peer.get('peer-address')
            error_msg = peer.get("last-error")

            # 20.0.0.3+63208
            if '+' in peer_interface:
                peer_interface = peer_interface.split('+')[0]

            if peer_interface == interface and error_msg == expected_error:
                return True 

        timeout.sleep()
    return False       

def verify_bgp_error_message(device, interface, expected_message, expected_error_message, max_time=60, check_interval=10):
    """
    Verify bgp last error

    Args:
        device('obj'): device to use
        interface('str'): Peer interface   
        expected_message('str'): Expected message
        expected_error_message('str') : Expected error message
        max_time ('int', optional): Maximum time to keep checking. Default to 60
        check_interval ('int', optional): How often to check. Default to 10

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)

    # show commands: "show bgp neighbor"

    # {'bgp-information': {'bgp-peer': [{ 
    #                                 "flap-count": '0',
    #                                 "peer-address": '20.0.0.3+63208', 
    #                                 "peer-restart-flags-received": 'Notification',
    #                                 "bgp-error": [
    #                                 {
    #                                     "name": "Hold Timer Expired " "Error",
    #                                     "receive-count": "40",
    #                                     "send-count": "27",
    #                                 },
    #                                 {"name": "Cease", "receive-count": "0", "send-count": "16"},
    #                             ],
    #                                   .
    #                                   .
    #                                   .

  
    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        peers_list = out.q.get_values("bgp-peer")

        for peer in peers_list:

            peer_interface = peer.get('peer-address')

            # 20.0.0.3+63208
            if '+' in peer_interface:
                peer_interface = peer_interface.split('+')[0]

            notification_message = Dq(peer).get_values("peer-restart-flags-received", 0)

            error_message_dict = Dq(peer).get_values("bgp-error", 0)

            if len(notification_message)>0 and error_message_dict:
                if peer_interface == interface and notification_message == expected_message and error_message_dict.get('name') == expected_error_message:
                    return True

        timeout.sleep()
    return False        


def verify_bgp_holdtime(device, expected_holdtime, interface, 
                        max_time=60, check_interval=10):
    """
    Verify bgp holdtimer with peer {interface}

    Args:
        device('obj'): device to use
        interface('str'): Peer interface   
        expected_holdtime('str'): Expected holdtime
        max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds
        check_interval ('int', optional): How often to check. Default to 10 seconds

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)    

    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        filter_output = out.q.contains('holdtime|peer-address', regex=True).reconstruct()

        # {'bgp-information': {
        #     'bgp-peer': [
        #         {'bgp-option-information': {
        #                 'holdtime': '30'},
        #          'peer-address': '20.0.0.3+179'},
        #         {'bgp-option-information': {
        #                 'holdtime': '10'},
        #          'peer-address': '2001:20::3+179'}]}}

        peer_list = filter_output.get('bgp-information').get('bgp-peer')

        for peer in peer_list:

            # 20.0.0.3+63208
            peer_address = peer.get('peer-address').split('+')[0]

            if peer_address == interface and\
                     Dq(peer).get_values('holdtime')[0] == str(expected_holdtime):
                return True 

        timeout.sleep()
    return False       

def verify_bgp_active_holdtime(device, expected_holdtime, interface, 
                                max_time=60, check_interval=10):
    """
    Verify bgp active holdtimer with peer {interface}

    Args:
        device('obj'): device to use
        interface('str'): Peer interface   
        expected_holdtime('str'): Expected active holdtime
        max_time ('int', optional): Maximum time to keep checking. Default to 60 seconds
        check_interval ('int', optional): How often to check. Default to 10 seconds

    Returns:  
        Boolean       
    Raises:
        N/A    
    """
    timeout = Timeout(max_time, check_interval)    

    while timeout.iterate():
        try:
            out = device.parse('show bgp neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        filter_output = out.q.contains('active-holdtime|peer-address', regex=True).reconstruct()

        # {'bgp-information': {'bgp-peer': [{'peer-address': '20.0.0.3+179',
        #                                 'active-holdtime': '30'},
        #                                 {'peer-address': '2001:20::3+179',
        #                                 'active-holdtime': '60'}]}}

        peer_list = filter_output.get('bgp-information').get('bgp-peer')

        for peer in peer_list:

            peer_address = peer.get('peer-address').split('+')[0]

            if peer_address == interface and\
                     Dq(peer).get_values('active-holdtime', 0) == str(expected_holdtime):
                return True 

        timeout.sleep()
    return False              