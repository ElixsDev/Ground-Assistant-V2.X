def makedict(datetime, string):
    #string = "{'raw_message': 'ICA3D2F0C>OGFLR,qAS,LuDa:/174633h4952.58N\\00801.77E^042/118/A=002192 !W99! id213D2F0C -118fpm -1.4rot 2.2dB 2e +4.1kHz gps3x4', 'reference_timestamp': datetime.datetime(2021, 9, 9, 17, 46, 34, 976553), 'aprs_type': 'position', 'name': 'ICA3D2F0C', 'dstcall': 'OGFLR', 'relay': None, 'receiver_name': 'LuDa', 'timestamp': datetime.datetime(2021, 9, 9, 17, 46, 33), 'latitude': 49.87648333333333, 'symboltable': '\\', 'longitude': 8.02965, 'symbolcode': '^', 'track': 42, 'ground_speed': 218.51537187702496, 'altitude': 668.1216000000001, 'comment': 'id213D2F0C -118fpm -1.4rot 2.2dB 2e +4.1kHz gps3x4', 'address_type': 1, 'aircraft_type': 8, 'no-tracking': False, 'stealth': False, 'address': '3D2F0C', 'climb_rate': -0.5994400000000001, 'turn_rate': -4.199999999999999, 'signal_quality': 2.2, 'error_count': 2, 'frequency_offset': 4.1, 'gps_quality': {'horizontal': 3, 'vertical': 4}, 'beacon_type': 'flarm'}"
    string = string[2:-1]

    keys = []
    values = []
    dict = {}

    while len(string) > 0:
        x = string.find("'")
        keys.append(string[:x])
        string = string[x + 3:]
        x = string.find("'")

        if x == 0:
            string = string[1:]
            x = string.find("'")
            values.append(string[:x])
            string = string[x + 4:]
        elif x == 1:
            y = string.find("{")
            if y != -1:
                z = string.find("}")
                values.append(string[y:z + 1])
                string = string[z + 4:]
            else:
                raise TypeError
        else:
            values.append(string[:x - 2])
            string = string[x + 1:]

    for i in range(0,len(values)):
        if values[i] == "None": values[i] = None
        elif values[i] == "True": values[i] = True
        elif values[i] == "False": values[i] = False
        elif values[i][:8] == "datetime":
            nums = values[i][18:-1].split(", ")
            for k in range(0, len(nums)):
                nums[k] = int(nums[k])

            if len(nums) == 7: dt = datetime(nums[0], nums[1], nums[2], nums[3], nums[4], nums[5], nums[6])
            else: dt = datetime(nums[0], nums[1], nums[2], nums[3], nums[4], nums[5])
            values[i] = dt

        else:
            if values[i].isnumeric() == True: values[i] = int(values[i])
            else:
                try:
                    values[i] = float(values[i])
                except:
                    pass

        dict[keys[i]] = values[i]
    return dict
