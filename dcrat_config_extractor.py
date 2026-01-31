import sys
import os
import json
import base64
import re

from clr_loader import get_coreclr
from pythonnet import set_runtime

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA1

dotnet_root = os.environ.get("DOTNET_ROOT", "/opt/homebrew/opt/dotnet/libexec")
rt = get_coreclr(dotnet_root=dotnet_root)
set_runtime(rt)

# import clr makes System available.
import clr
import System

System.Reflection.Assembly.LoadFrom(
    os.path.join(os.path.dirname(__file__), "dnlib.dll")
)

from dnlib.DotNet import ModuleDefMD


def decrypt(data_b64, key, salt):
    data = base64.b64decode(data_b64)
    dec_key = PBKDF2(key, salt, dkLen=32, count=50000, hmac_hash_module=SHA1)
    cipher = AES.new(dec_key, AES.MODE_CBC, data[32:48])
    pt = cipher.decrypt(data[48:])
    return pt[: -pt[-1]].decode("utf-8")


def get_cctor_strings(type_def):
    """IL walk: extract ldstr --> stsfld pairs from .cctor."""

    """
    $ ilspycmd -il -o dcrat.il dcrat.exe
    $ less dcrat.il
    .class public auto ansi abstract sealed beforefieldinit Client.Settings
        extends [mscorlib]System.Object
    {
        ...
        void .cctor () cil managed 
    {
        ...
        IL_0000: ldstr "Zg9VSZv/vsUnEQBzhfXpKPjYm70KkS5MxCRhZ1CLxaONi86O1tioh7cto+j8y2tHB120cTLyZ51HkueXBxsY1A=="
		IL_0005: stsfld string Client.Settings::Por_ts
		IL_000a: ldstr "7spuqcXBjdCSTbl3vuBaK8FMCIg75RONRRYTlaMK6b/cXzhviyYR/CGoPYLPme8EsZN0q7Er5FLtCE+5wGhnCW03V9p2bGNJ3uo+sagTJh0="
		IL_000f: stsfld string Client.Settings::Hos_ts
        ...
    """

    fields = {}
    for m in type_def.Methods:
        if str(m.Name) != ".cctor" or not m.HasBody:
            continue
        current = None
        for i in m.Body.Instructions:
            if str(i.OpCode) == "ldstr":
                current = str(i.Operand)
            elif str(i.OpCode) == "stsfld" and current:
                fields[str(i.Operand.Name)] = current
                current = None
    return fields


def find_salt(module):
    """Find salt string in Aes256 class .cctor."""

    """
    $ ilspycmd -il -o dcrat.il dcrat.exe
    $ less dcrat.il
    ...
    .class public auto ansi beforefieldinit Client.Algorithm.Aes256
	extends [mscorlib]System.Object
    {
    ...
    		void .cctor () cil managed 
	{
		// Method begins at RVA 0x237e
		// Header size: 1
		// Code size: 21 (0x15)
		.maxstack 8

		IL_0000: call class [mscorlib]System.Text.Encoding [mscorlib]System.Text.Encoding::get_ASCII()
		IL_0005: ldstr "DcRatByqwqdanchun"
    """

    for t in module.Types:
        if "aes" not in str(t.Name).lower():
            continue
        for m in t.Methods:
            if str(m.Name) != ".cctor" or not m.HasBody:
                continue
            for i in m.Body.Instructions:
                if str(i.OpCode) == "ldstr" and i.Operand:
                    return str(i.Operand).encode()
    return None


def main():
    module = ModuleDefMD.Load(sys.argv[1])

    settings = next((t for t in module.Types if str(t.Name) == "Settings"), None)
    if not settings:
        sys.exit("Settings class not found.")

    fields = get_cctor_strings(settings)
    key = base64.b64decode(fields.get("Key", ""))
    salt = find_salt(module)
    if not salt:
        sys.exit("Salt not found.")

    config = {}
    for name, value in fields.items():
        if name == "Key":
            continue
        if re.match(r"^[A-Za-z0-9+/]{20,}={0,2}$", value):
            try:
                config[name] = decrypt(value, key, salt)
            except Exception:
                config[name] = value
        else:
            config[name] = value

    print(json.dumps(config, indent=2))


if __name__ == "__main__":
    main()
