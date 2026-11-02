// Disassembles/decompiles a VA range for missing function bodies.
// Usage: -postScript DumpRange.java <startHex> <endHex>
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.cmd.disassemble.DisassembleCommand;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;

public class DumpRange extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        long start = Long.parseUnsignedLong(args[0].replace("0x", ""), 16);
        long end = Long.parseUnsignedLong(args[1].replace("0x", ""), 16);
        Address a = toAddr(start);
        Address b = toAddr(end);
        DisassembleCommand cmd = new DisassembleCommand(new AddressSet(a, b), null, true);
        cmd.applyTo(currentProgram, monitor);
        Function f = getFunctionAt(a);
        if (f == null) {
            f = createFunction(a, null);
        }
        println("FUNCTION " + (f == null ? "null" : f.getName() + " @ " + f.getEntryPoint()));
        if (f != null) {
            DecompInterface di = new DecompInterface();
            di.openProgram(currentProgram);
            DecompileResults res = di.decompileFunction(f, 60, monitor);
            println("===== DECOMP =====");
            println(res.getDecompiledFunction() != null ? res.getDecompiledFunction().getC() : res.getErrorMessage());
        }
        println("===== DISASM =====");
        InstructionIterator it = currentProgram.getListing().getInstructions(a, true);
        int n = 0;
        while (it.hasNext() && n < 200) {
            Instruction ins = it.next();
            if (ins.getAddress().getOffset() > end) break;
            println(ins.getAddress() + "  " + ins.toString());
            n++;
        }
    }
}
