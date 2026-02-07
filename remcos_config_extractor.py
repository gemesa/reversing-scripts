import sys
import pefile
from Crypto.Cipher import ARC4

CONFIG_FIELDS = {
    0x00: "c2_host_list",
    0x03: "install_mode_enable",
    0x04: "hkcu_run_persistence",
    0x05: "hklm_run_persistence",
    0x08: "hklm_policies_persistence",
    0x09: "install_folder_id",
    0x0A: "install_filename",
    0x0E: "mutex_name",
    0x0F: "keylogger_mode",
    0x10: "keylog_folder_id",
    0x11: "keylog_filename",
    0x14: "screenshot_time_enable",
    0x15: "screenshot_interval_min",
    0x16: "screenshot_window_enable",
    0x18: "screenshot_window_cooldown_sec",
    0x19: "screenshot_folder_id",
    0x1A: "screenshot_subfolder",
    0x23: "audio_enable",
    0x24: "audio_duration_min",
    0x25: "audio_folder_id",
    0x26: "audio_subfolder",
    0x27: "disable_uac",
    0x30: "install_subfolder",
    0x31: "keylog_subfolder",
    0x35: "screenshot_quality",
    0x38: "tls_client_cert",
    0x39: "tls_private_key",
    0x3A: "tls_ca_cert",
}


def extract_resource(pe: pefile.PE, name: str = "SETTINGS") -> bytes | None:
    RT_RCDATA = 10
    for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        if entry.id == RT_RCDATA:
            for resource_type in entry.directory.entries:
                if resource_type.name and resource_type.name.string.decode() == name:
                    for resource_lang in resource_type.directory.entries:
                        data_rva = resource_lang.data.struct.OffsetToData
                        size = resource_lang.data.struct.Size
                        return pe.get_memory_mapped_image()[data_rva : data_rva + size]
    return None


def parse_config(decrypted: bytes) -> list[bytes]:
    delimiter = b"|\x1e\x1e\x1f|"
    fields = decrypted.split(delimiter)
    return [f.strip(b"|").strip(b"\x00") for f in fields]


def extract_config(filepath: str) -> dict | None:
    try:
        pe = pefile.PE(filepath)
    except Exception as e:
        print(f"[!] Failed to parse PE: {e}")
        return None

    blob = extract_resource(pe, "SETTINGS")
    if not blob:
        print("[!] SETTINGS resource not found")
        return None

    key_len = blob[0]
    rc4_key = blob[1 : 1 + key_len]
    encrypted = blob[1 + key_len :]

    cipher = ARC4.new(rc4_key)
    decrypted = cipher.decrypt(encrypted)

    fields = parse_config(decrypted)

    result = {"rc4_key": rc4_key.hex(), "fields": {}}
    for i, value in enumerate(fields):
        if i in CONFIG_FIELDS:
            result["fields"][f"{i:02x}_{CONFIG_FIELDS[i]}"] = value
    return result


def format_value(key: str, raw: bytes) -> str | None:
    if not raw:
        return None

    if "tls_" in key:
        return raw.hex()

    # Single byte.
    if len(raw) == 1:
        byte_val = raw[0]
        # Printable ASCII (0x20-0x7E): show as character.
        if 0x20 <= byte_val <= 0x7E:
            return chr(byte_val)
        # Non-printable (0x00, 0x01, etc.): show as number.
        return str(byte_val)

    # Multi-byte: decode as UTF-8.
    try:
        decoded = raw.decode("utf-8")
        cleaned = (
            decoded.replace("\x00", "").replace("\r", "").replace("\n", " ").strip()
        )
        return cleaned if cleaned else None
    except:
        return raw.hex()


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <remcos.exe>")
        sys.exit(1)

    config = extract_config(sys.argv[1])
    if not config:
        print("[!] Failed to extract config")
        sys.exit(1)

    print(f"[rc4_key]: {config['rc4_key']}")

    for key, raw in config["fields"].items():
        display_val = format_value(key, raw)
        if display_val:
            print(f"[{key}]: {display_val}")


if __name__ == "__main__":
    main()
