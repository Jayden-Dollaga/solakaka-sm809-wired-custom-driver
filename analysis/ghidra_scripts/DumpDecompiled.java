// Dumps decompiled functions, strings, string xrefs, call edges and symbol inventory.
// Usage: -postScript DumpDecompiled.java <outputDir>
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileOptions;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.listing.Listing;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.program.model.symbol.Symbol;
import ghidra.program.model.symbol.SymbolIterator;
import ghidra.program.model.symbol.SymbolTable;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class DumpDecompiled extends GhidraScript {

    private static String q(String s) {
        if (s == null) {
            return "";
        }
        return "\"" + s.replace("\"", "\"\"").replace("\r", "\\r").replace("\n", "\\n") + "\"";
    }

    private static String safe(String s) {
        String r = s.replaceAll("[^A-Za-z0-9_.@-]", "_");
        if (r.length() > 90) {
            r = r.substring(0, 90);
        }
        return r;
    }

    private static void mkdirs(File f) {
        if (!f.exists()) {
            f.mkdirs();
        }
    }

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        String outRoot = args.length > 0 ? args[0] : ".";
        File root = new File(outRoot);
        mkdirs(root);
        File codeDir = new File(root, "pseudocode");
        mkdirs(codeDir);

        String programName = currentProgram.getName();
        println("DumpDecompiled: " + programName + " -> " + root.getAbsolutePath());

        // Memory map
        try (PrintWriter pw = new PrintWriter(new OutputStreamWriter(
                new FileOutputStream(new File(root, "memory_blocks.csv")), StandardCharsets.UTF_8))) {
            pw.println("name,start,end,size,initialized,read,write,execute,volatile,type");
            for (MemoryBlock b : currentProgram.getMemory().getBlocks()) {
                pw.println(String.join(",",
                        q(b.getName()), q(b.getStart().toString()), q(b.getEnd().toString()),
                        Long.toString(b.getSize()), Boolean.toString(b.isInitialized()),
                        Boolean.toString(b.isRead()), Boolean.toString(b.isWrite()),
                        Boolean.toString(b.isExecute()), Boolean.toString(b.isVolatile()),
                        q(b.getType() == null ? "" : b.getType().toString())));
            }
        }

        // Function index
        List<Function> functions = new ArrayList<>();
        FunctionIterator fit = currentProgram.getFunctionManager().getFunctions(true);
        while (fit.hasNext()) {
            functions.add(fit.next());
        }
        try (PrintWriter pw = new PrintWriter(new OutputStreamWriter(
                new FileOutputStream(new File(root, "functions.csv")), StandardCharsets.UTF_8))) {
            pw.println("entry,name,namespace,size,is_thunk,is_external,param_count,return_type,cc,body_min,body_max,file");
            for (Function f : functions) {
                String file = "";
                if (!f.isExternal() && !f.isThunk()) {
                    file = "pseudocode/" + safe(f.getName()) + "__" + f.getEntryPoint() + ".c";
                }
                pw.println(String.join(",",
                        q(f.getEntryPoint().toString()), q(f.getName()),
                        q(f.getParentNamespace() == null ? "" : f.getParentNamespace().getName(true)),
                        Long.toString(f.getBody().getNumAddresses()),
                        Boolean.toString(f.isThunk()), Boolean.toString(f.isExternal()),
                        Integer.toString(f.getParameterCount()),
                        q(f.getReturnType() == null ? "" : f.getReturnType().getName()),
                        q(f.getCallingConventionName()), q(f.getBody().getMinAddress().toString()),
                        q(f.getBody().getMaxAddress().toString()), q(file)));
            }
        }

        // Decompiled code
        DecompInterface decomp = new DecompInterface();
        DecompileOptions opts = new DecompileOptions();
        decomp.setOptions(opts);
        decomp.toggleCCode(true);
        decomp.toggleSyntaxTree(true);
        if (!decomp.openProgram(currentProgram)) {
            println("WARNING: decompiler did not open program: " + decomp.getLastMessage());
        }
        int ok = 0;
        int fail = 0;
        for (Function f : functions) {
            if (f.isExternal() || f.isThunk()) {
                continue;
            }
            String c;
            try {
                DecompileResults dr = decomp.decompileFunction(f, 120, monitor);
                if (dr.decompileCompleted() && dr.getDecompiledFunction() != null) {
                    c = dr.getDecompiledFunction().getC();
                    ok++;
                } else {
                    c = "// DECOMPILE FAILED: " + dr.getErrorMessage() + "\n";
                    fail++;
                }
            } catch (Exception e) {
                c = "// DECOMPILE EXCEPTION: " + e + "\n";
                fail++;
            }
            File out = new File(codeDir, safe(f.getName()) + "__" + f.getEntryPoint() + ".c");
            try (PrintWriter pw = new PrintWriter(new OutputStreamWriter(
                    new FileOutputStream(out), StandardCharsets.UTF_8))) {
                pw.println("// Program: " + programName);
                pw.println("// Function: " + f.getName());
                pw.println("// Entry: " + f.getEntryPoint());
                pw.println("// Body: " + f.getBody().getMinAddress() + " - " + f.getBody().getMaxAddress());
                pw.println("// Signature: " + f.getPrototypeString(false, false));
                pw.println();
                pw.println(c);
            }
        }
        decomp.dispose();
        println("Decompiled ok=" + ok + " failed=" + fail);

        // Defined strings
        Set<Address> stringAddrs = new LinkedHashSet<>();
        Listing listing = currentProgram.getListing();
        try (PrintWriter pw = new PrintWriter(new OutputStreamWriter(
                new FileOutputStream(new File(root, "strings.csv")), StandardCharsets.UTF_8))) {
            pw.println("address,length,type,value");
            DataIterator dit = listing.getDefinedData(true);
            while (dit.hasNext()) {
                Data d = dit.next();
                if (!d.hasStringValue()) {
                    continue;
                }
                Object v;
                try {
                    v = d.getValue();
                } catch (Exception e) {
                    continue;
                }
                if (v == null) {
                    continue;
                }
                stringAddrs.add(d.getAddress());
                pw.println(String.join(",", q(d.getAddress().toString()), Integer.toString(d.getLength()),
                        q(d.getDataType().getName()), q(v.toString())));
            }
        }
        println("Strings: " + stringAddrs.size());

        // String cross references
        ReferenceIterator dummy = null;
        try (PrintWriter pw = new PrintWriter(new OutputStreamWriter(
                new FileOutputStream(new File(root, "string_xrefs.csv")), StandardCharsets.UTF_8))) {
            pw.println("string_address,string_value,from_address,from_function,ref_type");
            for (Address a : stringAddrs) {
                Data d = listing.getDataAt(a);
                String val = "";
                if (d != null && d.getValue() != null) {
                    val = d.getValue().toString();
                }
                ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(a);
                while (refs.hasNext()) {
                    Reference r = refs.next();
                    Address from = r.getFromAddress();
                    Function cf = currentProgram.getFunctionManager().getFunctionContaining(from);
                    pw.println(String.join(",", q(a.toString()), q(val), q(from.toString()),
                            q(cf == null ? "" : cf.getName()), q(r.getReferenceType().toString())));
                }
            }
        }

        // Symbol inventory
        SymbolTable st = currentProgram.getSymbolTable();
        try (PrintWriter pw = new PrintWriter(new OutputStreamWriter(
                new FileOutputStream(new File(root, "symbols.csv")), StandardCharsets.UTF_8))) {
            pw.println("address,name,full_name,type,source,namespace,is_primary");
            SymbolIterator sit = st.getAllSymbols(true);
            while (sit.hasNext()) {
                Symbol s = sit.next();
                pw.println(String.join(",", q(s.getAddress().toString()), q(s.getName()),
                        q(s.getName(true)), q(s.getSymbolType().toString()), q(s.getSource().toString()),
                        q(s.getParentNamespace() == null ? "" : s.getParentNamespace().getName(true)),
                        Boolean.toString(s.isPrimary())));
            }
        }

        // Call edges from instructions
        try (PrintWriter pw = new PrintWriter(new OutputStreamWriter(
                new FileOutputStream(new File(root, "call_edges.csv")), StandardCharsets.UTF_8))) {
            pw.println("caller_entry,caller_name,site,callee_name,callee_entry,callee_kind,flow_type");
            for (Function f : functions) {
                if (f.isExternal()) {
                    continue;
                }
                InstructionIterator iit = listing.getInstructions(f.getBody(), true);
                while (iit.hasNext()) {
                    Instruction ins = iit.next();
                    if (!ins.getFlowType().isCall()) {
                        continue;
                    }
                    Reference[] refs = ins.getReferencesFrom();
                    boolean any = false;
                    for (Reference r : refs) {
                        Address to = r.getToAddress();
                        Function callee = currentProgram.getFunctionManager().getFunctionAt(to);
                        String cname = callee == null ? "" : callee.getName();
                        String centry = callee == null ? to.toString() : callee.getEntryPoint().toString();
                        String ckind = callee == null ? "unresolved" : (callee.isExternal() ? "external" : (callee.isThunk() ? "thunk" : "local"));
                        pw.println(String.join(",", q(f.getEntryPoint().toString()), q(f.getName()),
                                q(ins.getAddress().toString()), q(cname), q(centry), q(ckind),
                                q(r.getReferenceType().toString())));
                        any = true;
                    }
                    if (!any) {
                        pw.println(String.join(",", q(f.getEntryPoint().toString()), q(f.getName()),
                                q(ins.getAddress().toString()), q(""), q(""), q("unresolved"),
                                q(ins.getFlowType().toString())));
                    }
                }
            }
        }

        // Function -> string summary (only calls/references inside each function)
        println("DumpDecompiled finished.");
    }
}
