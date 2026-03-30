Set wshShell = CreateObject("WScript.Shell")
wshShell.Run "cmd /c .\jphs_jjnzzz\jphide\jpseek.exe aligator\f0104520.jpg extracted_gator_real.jpg > out.log"
WScript.Sleep 1000
wshShell.SendKeys "gator{ENTER}"
WScript.Sleep 2000
