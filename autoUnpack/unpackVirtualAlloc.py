import frida
import sys
import time
import argparse

parser = argparse.ArgumentParser(description='Unpacker via frida')
parser.add_argument("-f","--file",required=True)
args = parser.parse_args()

pid = frida.spawn(args.file)
session = frida.attach(pid)
time.sleep(1)

script =  session.create_script("""
    var vaExportAddress = Module.findExportByName("kernel32.dll", "VirtualAlloc");
    var count = 0;
    var vaRet = 0;
    var vaSize = 0;
    if (vaExportAddress != null) {
        console.log("VirtualAlloc found at: " + vaExportAddress);
        Interceptor.attach(vaExportAddress, {
            onEnter: function (args) {

            if (vaRet != 0 ){
            if (vaRet.readAnsiString(2) === "MZ") {
                        console.log("Found PE header at allocated memory");
                        count += 1;
                        var mainP = vaRet.readByteArray(vaSize);
                        var fileName = "Dumped_" + count + ".bin";
                        var file = new File(fileName, "wb");
                        file.write(mainP);
                        file.flush();
                        file.close();
                        console.log("Dumped -> " + fileName);
                    }
                    }
                vaSize = args[1].toInt32();
                console.log("VirtualAlloc called with size: " + vaSize);
            },
            onLeave: function (retval) {
                if (retval.isNull()) {
                    console.log("VirtualAlloc returned NULL");
                } else {

                    vaRet = ptr(retval);


                }
            }
        });
    } else {
        console.error("VirtualAlloc not found in kernel32.dll");
    }
""")
script.load()
frida.resume(pid)
sys.stdin.read()