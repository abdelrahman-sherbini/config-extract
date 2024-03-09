import psutil
import re
import os
import tempfile
import winreg
import sys
import win32security
import ntsecuritycon

def remove(path):
    path = path.replace("\\", "/")
    os.remove(path)
    print("File at {} was deleted".format(path))

def deleteRegistry(regKey, regSubkey, malFile):
    try:
        hKey = winreg.OpenKey(regKey, regSubkey, 0, winreg.KEY_ALL_ACCESS)
        i = 0

        while True:
            try:
                x = winreg.EnumValue(hKey, i)
                value = str(x[0])
                data = str(x[1])

                if malFile in data:
                    print("Found Malware registry value")
                    winreg.DeleteValue(hKey, value)
                    print("Deleted Malware registry value")
                    break

                i += 1
            except Exception as e:
                break

    except Exception as e:
        print(f"Error opening registry key: {e}")
    finally:
        winreg.CloseKey(hKey)

def setRegistryPermissions(key, subkey, username, permissions):
    try:
        key_handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
        security_descriptor = win32security.GetSecurityInfo(key_handle, win32security.SE_REGISTRY_KEY, win32security.DACL_SECURITY_INFORMATION)
        dacl = security_descriptor.GetSecurityDescriptorDacl()
        everyone = win32security.LookupAccountName("", "Everyone")[0]

        ace = win32security.ACE(
            win32security.ACL_REVISION,
            permissions,
            0,
            everyone
        )
        dacl.AddAccessAllowedAce(ace)

        win32security.SetSecurityInfo(
            key_handle,
            win32security.SE_REGISTRY_KEY,
            win32security.DACL_SECURITY_INFORMATION,
            None,
            None,
            dacl,
            None
        )

        print(f"Permissions modified for {subkey} key.")

    except Exception as e:
        print(f"Error modifying permissions for {subkey} key: {e}")
    finally:
        winreg.CloseKey(key_handle)

# Your registry paths
regPath1 = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows"
regPath2 = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run"
regPath3 = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Windows"

# Flag to indicate 32 or 64 bits.
is32bit = 1 if sys.maxsize > 2**32 else 0

malFile = ""
malProcess = ""

if is32bit:
    malProcess = "wuauclt.exe"
else:
    malProcess = "svchost.exe"

tempDir = tempfile.gettempdir()

for proc in psutil.pids():
    p = psutil.Process(proc)

    if p.name() == malProcess:
        try:
            files = p.open_files()
        except:
            continue

        for f in files:
            if tempDir in f[0]:
                x = f[0].split('\\')

                if x[-1][0:2] == "ms":
                    malFile = x[-1]
                    print("Malware random name is: {}".format(malFile))

                    try:
                        p.kill()
                        print("Malware Process with PID {} was killed".format(proc))
                    except Exception as e:
                        print("Unable to kill the process")

                    exit(1)

if not malFile:
    exit(0)

remove(os.path.join(tempDir, malFile))
key1 = winreg.HKEY_CURRENT_USER
sub1 = r"Software\Microsoft\Windows NT\CurrentVersion\Windows"

key2 = winreg.HKEY_LOCAL_MACHINE
sub2 = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run"
# Set permissions for the registry keys
setRegistryPermissions(key1, sub1, "Everyone", ntsecuritycon.KEY_ALL_ACCESS)
setRegistryPermissions(key2, sub2, "Everyone", ntsecuritycon.KEY_ALL_ACCESS)
# Delete the registry values
deleteRegistry(key1, sub1, malFile)
deleteRegistry(key2, sub2, malFile)