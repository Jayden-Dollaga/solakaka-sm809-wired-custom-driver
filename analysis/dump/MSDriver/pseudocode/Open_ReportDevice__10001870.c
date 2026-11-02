// Program: MSDriver.dll
// Function: Open_ReportDevice
// Entry: 10001870
// Body: 10001870 - 10001880
// Signature: bool Open_ReportDevice(void)


bool Open_ReportDevice(void)

{
  uint uVar1;
  
                    /* 0x1870  7  Open_ReportDevice */
  uVar1 = FUN_10001df0((undefined4 *)0x2);
  return (bool)('\x01' - (uVar1 != 1));
}


