import pymem
import re
import os

def find_offsets(pm, clientModule, patterns):
    addresses = {}
    for name, pattern in patterns.items():
        try:
            match = re.search(pattern, clientModule)
            if match:
                addresses[name] = match.start()
        except Exception as e:
            print(f"Error finding {name} offset: {str(e)}")
    
    return addresses

def main():
    try:
        pm = pymem.Pymem('cs2.exe')
        client = pymem.process.module_from_name(pm.process_handle, 'client.dll')
        clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)

        patterns = {
    "EntityList": rb'\x48\x8B\x0D....\x48\x8B\x01\x48\xFF\x60\x30',
    "LocalPlayerController": rb'\x48\x8B\x05....\x48\x85\xC0\x74\x4F',
    "ViewAngles": rb'\x48\x8B\x0D....\x48\x8B\x01\x48\xFF\x60\x30',
    "ViewMatrix": rb'\x48\x8D\x0D....\x48\xC1\xE0\x06',
    "LocalPlayerPawn": rb'\x48\x8D\x05....\xC3\xCC\xCC\xCC\xCC\xCC\xCC\xCC\x48\x83\xEC\x28\x8B\x0D',
    "GlowObjectManager": rb"\x48\x8D\x05....\x57\x48\x89\xC3\x48\x83\xEC\x20\x48\x8B\x0D....\x48\x85\xC9\x74\x0A",
    "ForceUpdate": rb"\x48\x89\x43\x10\x57\x48\x83\xEC\x20\x48\x8B\x0D....\x48\x85\xC9\x74\x0A",
    "m_hPlayerPawn": rb'\x48\x89\x43\x10\x57\x48\x83\xEC\x20\x48\x8B\x0D....\x48\x85\xC9\x74\x0A'
}

        start_dumping = input("Do you want to start dumping offsets? (y/n) ").strip().lower()
        if start_dumping == "y":
            
            addresses = find_offsets(pm, clientModule, patterns)
            output_path = os.path.join(os.path.expanduser('~/Downloads'), 'offsets.txt')
            
            with open(output_path, "w") as f:
                for name, address in addresses.items():
                    f.write(f"{name}: 0x{client.lpBaseOfDll + address:08X}\n")

            for name, address in addresses.items():
                print(f"{name}: 0x{client.lpBaseOfDll + address:08X}")

            print(f"Offsets saved to: {output_path}")
        else:
            print("Exiting.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
