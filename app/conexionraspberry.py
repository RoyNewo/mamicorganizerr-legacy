import check_ips_and_ports
from getmac import get_mac_address
from icecream import ic
import json

def main():
    with open("/opt/tachiyomimangaexporter/secrets.json") as json_file2:
        secrets = json.load(json_file2)
    if address := check_ips_and_ports.check_subnet_for_open_port(secrets["rango"], secrets["puerto"]):
        for direccion in address:
            ip_mac = get_mac_address(ip=direccion)
            if ip_mac == secrets["mac"]:
                if direccion != secrets["ip"]:
                    secrets["ip"] = direccion
                    with open("/opt/tachiyomimangaexporter/secrets.json", "w") as outfile:
                        json.dump(secrets, outfile)
                return direccion


if __name__ == "__main__":
    main()
