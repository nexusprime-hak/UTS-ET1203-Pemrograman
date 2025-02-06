import re
import json
import requests
from bs4 import BeautifulSoup

html_content = """
<!--
Array
(
    [0] => Array
        (
            [name] => TELKOMSAT 113BT
            [sat_id] => 58995
            [int_designator] => 2024-035A
            [magnitude] => 
            [misc] => OK
            [period] => 1436.1
            [launch_date] => 2024-02-20
            [apogee] => 35800.7
            [perigee] => 35788.3
            [inclination] => 20.8
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [1] => Array
        (
            [name] => NUSANTARA TIGA
            [sat_id] => 57045
            [int_designator] => 2023-086A
            [magnitude] => 
            [misc] => OK
            [period] => 1436.1
            [launch_date] => 2023-06-18
            [apogee] => 35812.5
            [perigee] => 35776.2
            [inclination] => 27.88
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [2] => Array
        (
            [name] => NUSANTARA SATU
            [sat_id] => 44048
            [int_designator] => 2019-009A
            [magnitude] => 
            [misc] => OK
            [period] => 1436.1
            [launch_date] => 2019-02-22
            [apogee] => 35809.1
            [perigee] => 35779.6
            [inclination] => 27.55
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [3] => Array
        (
            [name] => TELKOM-4
            [sat_id] => 43587
            [int_designator] => 2018-064A
            [magnitude] => 
            [misc] => OK
            [period] => 1436.1
            [launch_date] => 2018-08-07
            [apogee] => 35799.3
            [perigee] => 35788.3
            [inclination] => 27.06
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [4] => Array
        (
            [name] => TELKOM 3S
            [sat_id] => 41944
            [int_designator] => 2017-007A
            [magnitude] => 
            [misc] => OK
            [period] => 1436.1
            [launch_date] => 2017-02-14
            [apogee] => 35804.7
            [perigee] => 35782.7
            [inclination] => 0.03
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [5] => Array
        (
            [name] => LAPAN A3
            [sat_id] => 41603
            [int_designator] => 2016-040E
            [magnitude] => 0
            [misc] => OK
            [period] => 94.3
            [launch_date] => 2016-06-22
            [apogee] => 498.1
            [perigee] => 484.3
            [inclination] => 97.51
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => true
        )

    [6] => Array
        (
            [name] => BRISAT
            [sat_id] => 41591
            [int_designator] => 2016-039A
            [magnitude] => 
            [misc] => OK
            [period] => 1436.1
            [launch_date] => 2016-06-18
            [apogee] => 35803
            [perigee] => 35785.2
            [inclination] => 5.86
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [7] => Array
        (
            [name] => LAPAN A2 (IO-86)
            [sat_id] => 40931
            [int_designator] => 2015-052B
            [magnitude] => 0
            [misc] => OK
            [period] => 97.4
            [launch_date] => 2015-09-28
            [apogee] => 651.1
            [perigee] => 632.4
            [inclination] => 6
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => true
        )

    [8] => Array
        (
            [name] => PALAPA D
            [sat_id] => 35812
            [int_designator] => 2009-046A
            [magnitude] => 
            [misc] => OK
            [period] => 1458.2
            [launch_date] => 2009-08-31
            [apogee] => 36294.1
            [perigee] => 36158.2
            [inclination] => 0.02
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [9] => Array
        (
            [name] => LAPAN-TUBSAT
            [sat_id] => 29709
            [int_designator] => 2007-001A
            [magnitude] => 9.5
            [misc] => OK
            [period] => 97
            [launch_date] => 2007-01-10
            [apogee] => 629.6
            [perigee] => 614.1
            [inclination] => 97.63
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => true
        )

    [10] => Array
        (
            [name] => TELKOM 2
            [sat_id] => 28902
            [int_designator] => 2005-046A
            [magnitude] => 
            [misc] => OK
            [period] => 1452.4
            [launch_date] => 2005-11-16
            [apogee] => 36144.5
            [perigee] => 36079.5
            [inclination] => 0.03
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [11] => Array
        (
            [name] => GARUDA 1
            [sat_id] => 26089
            [int_designator] => 2000-011A
            [magnitude] => 
            [misc] => OK
            [period] => 1441.1
            [launch_date] => 2000-02-12
            [apogee] => 35915.8
            [perigee] => 35866.9
            [inclination] => 1.22
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [12] => Array
        (
            [name] => TELKOM 1
            [sat_id] => 25880
            [int_designator] => 1999-042A
            [magnitude] => 
            [misc] => OK
            [period] => 1436.1
            [launch_date] => 1999-08-12
            [apogee] => 35859.2
            [perigee] => 35729.1
            [inclination] => 0.03
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [13] => Array
        (
            [name] => INDOSTAR 1
            [sat_id] => 25050
            [int_designator] => 1997-071B
            [magnitude] => 
            [misc] => OK
            [period] => 1435.8
            [launch_date] => 1997-11-11
            [apogee] => 35800
            [perigee] => 35775.7
            [inclination] => 6.83
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [14] => Array
        (
            [name] => PALAPA C2
            [sat_id] => 23864
            [int_designator] => 1996-030A
            [magnitude] => 
            [misc] => OK
            [period] => 1454.6
            [launch_date] => 1996-05-16
            [apogee] => 36186.7
            [perigee] => 36122.1
            [inclination] => 2.75
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [15] => Array
        (
            [name] => PALAPA B4
            [sat_id] => 21964
            [int_designator] => 1992-027A
            [magnitude] => 
            [misc] => OK
            [period] => 1440.8
            [launch_date] => 1992-05-14
            [apogee] => 35889.4
            [perigee] => 35881.1
            [inclination] => 7.51
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [16] => Array
        (
            [name] => PALAPA B1
            [sat_id] => 14134
            [int_designator] => 1983-059C
            [magnitude] => 
            [misc] => OK
            [period] => 1437.2
            [launch_date] => 1983-06-18
            [apogee] => 35827
            [perigee] => 35805.2
            [inclination] => 14.55
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [17] => Array
        (
            [name] => PALAPA 2
            [sat_id] => 9862
            [int_designator] => 1977-018A
            [magnitude] => 
            [misc] => OK
            [period] => 1439.3
            [launch_date] => 1977-03-10
            [apogee] => 35867.4
            [perigee] => 35843.7
            [inclination] => 14.79
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

    [18] => Array
        (
            [name] => PALAPA 1
            [sat_id] => 9009
            [int_designator] => 1976-066A
            [magnitude] => 
            [misc] => OK
            [period] => 1439
            [launch_date] => 1976-07-08
            [apogee] => 35875.7
            [perigee] => 35825.6
            [inclination] => 14.7
            [type] => 
            [isdecayed] => 0
            [geolongitude] => 
            [isleo] => false
        )

)
-->
"""

comment_content = re.search(r'<!--(.*?)-->', html_content, re.DOTALL).group(1)

pattern = r'\[name\] => ([^\n]+)\s+\[sat_id\] => (\d+)'
matches = re.findall(pattern, comment_content)

satellite_data = [{"name": name.strip(), "sat_id": sat_id} for name, sat_id in matches]

with open("satellite_data/satellite_data.json", "w") as file:
    json.dump(satellite_data, file, indent=4)
    